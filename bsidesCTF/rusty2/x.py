from pwn import *

r = remote("0.0.0.0", 9998)

r.sendline("DDDD")
