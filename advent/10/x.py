#!/home/esc/python2env/bin/python2.7

# from pwn import *
import sys
from threading import Thread
import time
import re
from binascii import unhexlify

# class PausableThread(threading.Thread):

#     def __init__(self, group=None, target=None, name=None, args=(), kwargs={}):
#         self._event = threading.Event()
#         if target:
#             args = ((lambda: self._event.wait()),) + args
#         super(PausableThread, self).__init__(group, target, name, args, kwargs)

#     def pause(self):
#         self._event.clear()

#     def resume(self):
#         self._event.set()

# def write(cmd):
#     p.send_raw(cmd)
#     return p.recvuntil("gef\xe2")

# def read():
#     while True:
#         print p.recv()

# def flush():
#     print p.recv()

# def gdb_ret(cmd):
#     out = write(cmd)
#     return re.search("uint128 = (.*)\n", out).group(1)

# p = process(argv=['gdb']+sys.argv[1:])
# # t = Thread(target=read, args=(), kwargs={})
# # t._event = threading.Event()
# # pt = PausableThread(t)

# # t.daemon = True
# # t.start()

# write("b *0x400730\n") # break on complete loop
# write("r\n")
# p.recvuntil("gef\xe2")


# seen = {}

# while True:
#     v4 = hex(int(gdb_ret("info registers xmm3\n"), 16))[2:].rjust(32,'0')
#     v5 = hex(int(gdb_ret("info registers xmm2\n"), 16))[2:].rjust(32,'0')
#     v6 = hex(int(gdb_ret("info registers xmm1\n"), 16))[2:].rjust(32,'0')
#     v7 = hex(int(gdb_ret("info registers xmm0\n"), 16))[2:].rjust(32,'0')

    # print v4

# v4 = "5ba4ffb453f7410f4c49826a449bc3c5"
# v4 = "0289eb306a53c241b61d995301e770644c"
# v4 =   "1dd8a1822f4a4abf958061f4"
# v4 = "0c706842545b455e960d21d6"
v4 = "6f171706c91ddf6cfbc1b811d6"
# v4 = "47f8067189a4b68790f6fe22a30723b000"
    # curr = bytearray(v4.strip().decode('hex') + v5.strip().decode('hex') + v6.strip().decode('hex') + v7.strip().decode('hex'))
# curr = v4.decode('hex')

flag = "\xFC\x14\xEB\x09\xBC\xAE\xE7\x47"
flag = bytearray("FC14EB09BCAEE7474FE37CC152A5028E8971C88D9623016D71405AEAFD461D23".decode("hex"))
curr = "\x6f\x17\x17\x06\xc9\x1d\xdf\x6c\xfb\xc1\xb8\x11\xd6"
curr = "\x73\xb1\xa2\x8c\xb3\x88\xd8\xcf\x18\x3b\xd0\xd4\x01"
curr = "\x4b\xd8\x43\x9e\x43\x95\x2c\x74\x90\x73\x7f"
#curr = bytearray("008be8af00079461000412d0007a8b7f".decode("hex"))
#curr = "\x86\x4c\xc0\x00\x30\x4a\x33\x00\x55\x97\xe0\x00\x69\x31\xd6"
curr = bytearray('864cc000304a33005597e0006931d6'.decode("hex"))
curr = bytearray('008401df0089b1ef0084d4f10017ed29'.decode("hex"))
# out = [0]*16
out = bytearray()
for j in range(0,8,2):
    out.append(flag[j] ^ curr[2*j])
    out.append(flag[j+1] ^ curr[2*j+1])

print(out)


def xor(a, b):
    a = bytearray(a)
    b = bytearray(b)
    out = bytearray()
    for j in range(0,8,2):
        out.append(a[j] ^ b[2*j])
        out.append(a[j+1] ^ b[2*j+1])
    return bytes(out)

flag = "FC14EB09BCAEE7474FE37CC152A5028E8971C88D9623016D71405AEAFD461D23".decode("hex")
curr = '008401df0089b1ef0084d4f10017ed29'.decode("hex")
print(xor(flag, curr))

#print(list(map(lambda x: chr(x), out)))
    # dflag = str(flag)
    # # print(dflag)
    # if dflag not in seen.keys():
    #     seen[dflag] = 1
    # else:
    #     seen[dflag] += 1
    #     print "flag seen twice: " + dflag
    # write("c\n")

