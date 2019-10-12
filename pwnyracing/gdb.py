from pwn import *
from IPython import embed

context.terminal= ['tmux', 'splitw', '-h']

p = process('gdb')

# gdb_script = """
# c
# """

# gdb.attach(p)
#p.interactive()
embed()
