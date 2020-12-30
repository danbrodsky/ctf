from pwn import *

r = remote("7b0000002c087461509b18f0.challenges.broker1.allesctf.net", 1337, ssl=True)
r.interactive()

data = open("dump.txt").read()

while True:
    i = input("~: ")
    r.sendline(i)
    out = str(r.clean(1))
    d = ">"
    print(out)
    # out = [e+d for e in out.split(d) if e]
    # for o in out:
    #     if o not in data:
    #         print(o)







