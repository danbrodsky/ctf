#!/usr/bin/python2 -u
from pwn import *


curr = "picoCTF{"
for c in range(1,14):	
	print("........................................................",c)
	nc = remote('2018shell1.picoctf.com', 37131)
	nc.recvuntil("Please enter your situation report: ")
	payload2 = "A"*11+"B"*(25-c)
	nc.sendline(payload2)
	cipher = nc.recv(1024).decode('hex')
	nc.close()
	
	for i in range(32,128):
		nc2 = remote('2018shell1.picoctf.com', 37131)
		nc2.recvuntil("Please enter your situation report: ")
		payload = "A"*11 + "B"*(14-c) + curr + chr(i)

		nc2.sendline(payload)
		cipher2 = nc2.recv(1024).decode('hex')
		nc2.close()
		if cipher2[80:96] == cipher[128:144]:
			curr += chr(i)
			break
		time.sleep(0.05)
	c += 1
	if c > len(curr):
		print("trash")
		time.sleep(100)
print "deciphered text is: " + curr
	
