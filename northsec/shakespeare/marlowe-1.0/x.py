#!/usr/bin/env python3

from pwn import *
import random

flag = "FLAG-S3v3" + "X"*23

best = 0

FOUND = "Popping Romeo, getting the value"

chars = "0123456789abcdefghijklmnopqrstuvwxyz-_ABCDEFGHIJKLMNOPQRSTUVWXYZ"
once = 0
for i in range(9,32):
    for c in chars:
        r = process("./source")
        payload = list(flag)
        payload[i] = c
        r.sendline(''.join(payload))

        out = r.recvuntil("Wrong! You suck!!11")
        count = str(out).count(FOUND)
        print(count)
        if best  < count:
            print(count)
            best = count
            if not once:
                once = 1
                continue
            flag = list(flag)
            flag[i] = c
            flag = ''.join(flag)
            print(flag)
            break
        r.close()
