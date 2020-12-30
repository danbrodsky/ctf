from pwn import *

r = remote("intro2.satellitesabove.me", 5001)

ticket = "ticket{delta67312papa:GMQZXBxCErmf_YlW6lO9ij02Wa34DgqiZj7bkPGuRRE0VlzNumu9VNKT_GSbW0QJyQ}"

r.recvuntil("Ticket please:\n")
r.sendline(ticket)

comp = r.recvuntil(b" = ?")[:-4].split(b" + ")

r.sendline(f"{int(comp[0]) + int(comp[1])}")

r.interactive()
