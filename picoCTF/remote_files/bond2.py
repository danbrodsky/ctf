from pwn import *
import time

curr = "coCTF{@g3nt6_1$"
dump = "pi"
for i in range (16,48):
	for j in range(128):
		print i
		payload = ""
		payload += 'A'*11
		payload += curr
		payload += chr(j)
		payload += 'a'*(48-i)
		nc = remote('2018shell.picoctf.com', 37131 )
		nc.recvuntil("Please enter your situation report: ")
		print payload
		nc.sendline(payload)
		out = nc.recvall()
		for k in range(0,len(out), 32):
			print out[k:k+32]
		if out[128:160] == out[288:320]:
			print "blocks match"
			dump += str(curr[1])
			curr = curr[1:]
			curr += chr(j)
			print curr
			break
		nc.close()
		print dump + curr
		time.sleep(0.05)
