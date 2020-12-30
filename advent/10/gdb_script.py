#!/home/esc/python2env/bin/python2.7
from pwn import *
import sys

context.terminal = ['tmux', 'splitw', '-v']

# Change as needed
# note: ida-interact requires ida_gef.py (retsync might be better)
GDB_SCRIPT = """
entry-break
b *0x
"""

# Useful commands (--help for info):
# +------------------------------+------------------------------+
# |pccustom                      |dt (strust inspect) for gdb   |
# +------------------------------+------------------------------+
# |grep                          |search in mem                 |
# +------------------------------+------------------------------+
# |trace-run                     |all instructions up to point  |
# +------------------------------+------------------------------+
# |vmmap                         |display virtual memory        |
# +------------------------------+------------------------------+
# |pi __                         |run python command            |
# +------------------------------+------------------------------+
# |set $<name> = val             |set convenience var           |
# +------------------------------+------------------------------+
# |cc                            |while sync, cont to IDA cursor|
# +------------------------------+------------------------------+



p = process(sys.argv[1])

gdb.attach(p, GDB_SCRIPT)
