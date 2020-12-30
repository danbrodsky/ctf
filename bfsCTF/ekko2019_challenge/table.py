from pwn import *
start = 0x488B01C3C3C3C3

context.arch='amd64'
p64b = make_packer(64, endian='big', sign='unsigned')

instr = []
for i in range(256):
    print disasm(p64b(( i << 56 ) + start))
