#!/usr/bin/env python

from pwn import *
import itertools
from hashlib import sha256

r = remote("106.53.114.216", 9999)

r.recvuntil("\"")
chal = int(r.recvline().strip(b"\"\n"), 16)
print(chal)
for i, sol in enumerate(itertools.permutations(range(0x20, 0x7f), 3)):
    sol = bytes(sol)
    if sha256(chal + sol).digest().startswith(b'\0\0\0'):
        break

r.send(sol)
r.interactive()
