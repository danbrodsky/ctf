from pwn import *

p = process('./Vcheck')

p.sendline(b"U?^Kq6y\x04")
p.interactive()
