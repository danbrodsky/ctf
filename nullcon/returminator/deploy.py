import subprocess
from pwn import *
import string

o = [
    296,
    272,
    272,
    272,
    296,
    360,
    272,
    424,
    272,
    208,
    120,
    120,
    120,
    96,
    120,
    120,
    120,
    120,
    120,
    120,
    120,
    208,
    120,
    120,
    208,
    208,
    208,
    208,
    208,
    272,
    120,
    208,
    208,
]
r = [
    208,
    225,
    237,
    20,
    214,
    183,
    79,
    105,
    207,
    217,
    125,
    66,
    123,
    104,
    97,
    99,
    107,
    105,
    109,
    50,
    48,
    202,
    111,
    111,
    29,
    63,
    223,
    36,
    0,
    124,
    100,
    219,
    32,
]

cmd = ["./main"]
rets = []

out = [" "] * 35
for _ in range(1):
    # for c in string.printable:
    for c in "a":
        rets = []

        with open("flag", "w") as flag:
            # p = "".join(out).replace(" ", c)
            flag.write(c * 35)
            flag.close()
        with open("blob", "rb") as f:
            for offset in o:
                data = f.read(offset)
                print(disasm(data.replace("\x41", "\x90")))
                p = subprocess.Popen(cmd, stdin=subprocess.PIPE)
                p.stdin.write(data)
                p.communicate()
                rets.append(p.returncode)

        # if all([rets[i] == r[i] for i in range(len(r))]):
        #     print('Yes!')
        for i in range(len(r)):
            if rets[i] == r[i]:
                # print("Yes!")
                # print(i)
                # print(c)
                out[i] = c
                # print(out)
            # else:
            # print("No!")

print("".join(out))
