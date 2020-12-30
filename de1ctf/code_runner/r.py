#!/usr/bin/env python

from pwn import *
from capstone import *
from IPython import embed
from ipdb import set_trace

import re
import gzip
import time
import itertools
from hashlib import sha256

from lib import *
from z3lib import *


md = Cs(CS_ARCH_MIPS, CS_MODE_MIPS32)
end_func_bytes = bytes.fromhex("f8ffbd270400beaf25f0a0030800c4af01c0023cbeba423425e8c0030400be8f0800bd270800e00300000000")
r = None
t0 = None

def ru(s):
    res = r.recvuntil(s)
    if DEBUG:
        print(res.decode("ascii"), end="s")
    return res


def rl():
    res = r.recvline()
    if DEBUG:
        print(res.decode("ascii"), end="")
    return res


def start_timer():
    global t0
    if t0 is None:
        t0 = time.time()


def end_timer():
    t1 = time.time()
    print(f"That took {t1 - t0} seconds")


def get_binary():
    global r
    r = remote("106.53.114.216", 9999)

    ru("hexdigest() == ")
    hexhash = rl().strip(b"\n\"").decode("ascii")

    for s in [bytes(x) for x in itertools.permutations(range(0, 256), 3)]:
        if sha256(s).hexdigest() == hexhash:
            break
    else:
        assert 0

    r.sendline(s)

    start_timer()

    ru("Binary Dump:\n")
    ru("======\n")
    hexcode = rl().strip(b"\n")

    gzipcode = b64d(hexcode)

    code = gzip.decompress(gzipcode)

    if DEBUG:
        with open("code", "wb") as f:
            f.write(code)

    return code


# Get binary for remote
# elf = get_binary()

filename = "code.0"
with open(filename, "rb") as f:
    elf = f.read()
r = process(f"qemu-mipsel -strace ./{filename}", shell=True)
# r = process(f"qemu-mipsel -g 5000 ./{filename}", shell=True)

start_timer()

m = re.search(end_func_bytes, elf)
assert m
# Start of the first intesting func in BYTE ORDER not exec order
start = m.span()[1]

assert start == 0xb5c

insts = md.disasm_lite(elf[start:start+ALL_FUNCS_LEN], 0)
funcs = []
for _ in range(16):
    funcs.append(Func(insts))

results = []
for f in funcs:
    results.append(f.solve())

payload = b"".join(reversed(results))

r.send(payload)

end_timer()

# ru("Name")
# r.send("A")

# embed(colors="linux")
r.interactive()
