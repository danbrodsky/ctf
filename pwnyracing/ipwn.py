from pwn import *
from IPython import embed
import sys

p = process(sys.argv[1])

embed()
