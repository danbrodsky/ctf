from pwn import *



target = 'ZXFWtmKgDZCyrmC5B+CiVfsyXUCQVfsyZRFzDU4yX2YCD/F5Ih8='

targets = [target[i:i+4] for i in range(0,len(target),4)]

validChars = "abcdefgh;: ijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890-+=_,.<>/?{[]}|\\`~""''()!@#$%^&*"
j = 2
b = 10
curr = "MCA{Th15_wUz_EaZy_Pe@Zy_L3m0n_SqUe3zy}"
best = "MCA{Th15_-ez-e!-i_de@-i_-cmdn_-aU-cz}"
alt = "--------------a--------------------*--"
currEnd = ""
found = 0
nope = '5UEu'
nope = ''
while 4*b < len(target):
	for i in validChars:
		time.sleep(0.05)
		tmp = list(curr)
		if best[3*b+j-1] == i or i in nope:
			continue
		tmp[3*b+j-1] = i
		payload = ''.join(tmp)
		log.info(payload)
		re = process(['REbase-fix', payload])
		info = re.recvuntil('ZXFWtmKgDZCyrmC5B+CiVfsyXUCQVfsyZRFzDU4yX2YCD/F5Ih8=')
		re.close()
		log.info(info)
		val = info.split("\n")[1]
		log.info(val)
		log.info(targets[b][j])
		log.info(val[4*b+j])
		if j == 1:
			r = val[4*b+j-1]
			t = targets[b][j-1]
		else:
			r = val[4*b+j]
			t = targets[b][j]
		if r == t:
			log.info(payload)
			curr = ''.join(tmp)
			b += 1
			found = 1
			break
	if not found:
		b += 1
	found = 0
