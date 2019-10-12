from pwn import *
import sys
from threading import Thread

def write(cmd):
    p.send_raw(cmd)

def read():
    while True:
        print(p.recv())

p = process(argv=['gdb']+sys.argv[1:])
t = Thread(target=read, args=(), kwargs={})
t.daemon = True
t.start()

while True:
    cmd = str(raw_input(": "))
    try:
        cmd = eval(cmd) + '\n'
    except:
        pass
    write(str(cmd))

