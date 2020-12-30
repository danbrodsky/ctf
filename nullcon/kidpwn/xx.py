import angr
import claripy
import logging
import hashlib
from IPython import embed
import binascii
import sys

LITTLE_ENDIAN = 'Iend_LE'

log = logging.getLogger("x")
log.setLevel(logging.DEBUG)

proj = angr.Project("./flaggybird/lib/x86/library.so")

# Start of the nativeCheck function
state = proj.factory.blank_state(addr=0x4008f0)

key = claripy.BVS("key", 0x20*8)
key_len = claripy.BVV(0x20, 4*8)
key_addr = 0x402f00

# Store the symbolic key somewhere in RW memory
state.memory.store(key_addr, key)

for i in range(0, 32, 2):
    k = state.memory.load(key_addr + i, size=1)
    state.add_constraints(k == 0)

@proj.hook(0x400925, length=6)
def jniGetArrayLength(state):
    state.regs.eax = key_len

@proj.hook(0x400940, length=6)
def jniGetByteArrayElements(state):
    state.regs.eax = key_addr

sm = proj.factory.simulation_manager(state)

# Stop a few instructions into M
sm.explore(find=0x4005f0)
s = sm.one_found

# Second argument should be 0x10 for the key length
assert s.mem[s.regs.esp + 8].int.concrete == 0x10

key_scrambled_ptr = s.memory.load(s.regs.esp + 4, size=4, endness=LITTLE_ENDIAN)
for i in range(0x10):
    byte = s.memory.load(key_scrambled_ptr + i, size=1)
    s.add_constraints(byte < 0x10)

sm.move(from_stash="found", to_stash="active")

avoid = 0x400729 # Set c=0
find = 0x400b5f # After ret4 is set

sm.explore(avoid=avoid, find=find)

assert len(sm.found) == 1
assert len(sm.active) == 0

s = sm.one_found

r = s.solver.eval_upto(key, cast_to=bytes, n=2)
assert len(r) == 1
r = r[0]

numbers = []
for i in range(0, 32, 2):
    numbers.append(r[i] + r[i+1])

log.info("Here are the numbers to choose from: %s" % numbers)

attempts = 0

def blah(string="", depth=0):
    global attempts

    if depth == 16:
        attempts += 1
        h = hashlib.sha256(string.encode("ascii")).digest()
        log.info("Attempt #%d Hash: %s" % (attempts, binascii.hexlify(h)))
        if h == expected_hash:
            log.info("Found the key: %s" % string)
            embed()
        return

    n = numbers[depth]
    string1 = string + "\x00" + chr(n)
    string2 = string + chr(n) + "\x00"
    blah(string1, depth+1)
    blah(string2, depth+1)

expected_hash = b'.2\\\x91\xc9\x14x\xb3\\.\x0c\xb6[xQ\xc6\xfa\x98\x85Zw\xc3\xbf\xd3\xf0\x08@\xbc\x99\xac\xe2k'
log.info("Expected hash: %s" % binascii.hexlify(expected_hash))

blah()

embed()
