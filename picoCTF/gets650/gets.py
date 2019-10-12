from pwn import *

p = process('./gets')

p.recvuntil('GIVE ME YOUR NAME!')

rop = flat([

    ])

payload = 'a' * 23

