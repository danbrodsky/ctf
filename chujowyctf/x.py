from pwn import *

for i in range(100):
    r = remote("insanity1.chujowyc.tf",4004)

    r.recvuntil(":")
    r.sendline("4")
    print(r.clean())
    r.recvuntil("100")
    r.sendline(str(i))
    print(i)
    print(r.clean(1))
    r.close()
