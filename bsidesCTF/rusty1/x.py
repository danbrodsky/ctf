from pwn import *

r = remote("rusty1-080e45dc.challenges.bsidessf.net", 8832)


def rot1(arg):
    return "".join(map(lambda c: chr(ord(c) + 1), list(arg)))


while True:
    cmd_arg = raw_input().rstrip()

    rot_arg = rot1(cmd_arg)
    print rot_arg

    r.sendline(rot_arg)
    res = r.clean()

    print(rot1(res))
