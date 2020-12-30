#!/usr/bin/env python3

from pwn import *
from z3 import *
from claripy import *
import angr
# =>

proj = angr.Project(
    "/home/esc/ctf/tmctf/reversing200/much_ado_about_nothing",
    load_options={"main_opts": {"base_addr": 0x0}},
)
# => WARNING | 2020-06-03 18:41:15,730 | cle.loader | much_ado_about_nothing: base_addr was specified but the object is not PIC. specify force_rebase=True to override
#    <Project /home/esc/ctf/tmctf/reversing200/much_ado_about_nothing>

# autopopulates project.kb.functions
# cfg = project.analyses.CFGEmulated(keep_state=True)
# functions = [(addr, fn_name) for addr, fn_name in project.kb.functions.items()]

# set initial state
init_state = proj.factory.blank_state(addr=0x401e18)
# => <SimState @ 0x401e18>

proj.loader.main_object.sections
# cfg = project.analyses.CFGEmulated(keep_state=True)
# idfer = proj.analyses.Identifier()

bss = proj.loader.main_object.sections_map[".bss"]
# => <.bss | offset 0xbc350, vaddr 0x4bd360, size 0x1898>

c = BVS("char", 8)
# => <BV8 char_140088_8>

init_state.regs.rbp = bss.vaddr
# => <BV64 0x4bd360>
init_state.memory.store(bss.vaddr-0x18, c)
# =>

# init_state.mem[bss.vaddr]

sim = proj.factory.simgr(init_state)
# => <SimulationManager with 1 active>

# set end state
sim.explore(find=0x401f0c, avoid=0x401f00)
# => <SimulationManager with 4 active, 2 found, 3 avoid>

sol = sim.found[0]
# => <SimState @ 0x401f0c>

sol.solver.eval_upto(c, 50, cast_to=bytes)
# => [b'I', b'l', b'L', b'i', b'o', b'O', b'K', b'h', b'H', b'N', b'k', b'n', b'j', b'J', b'm', b'M']


# Improvement:
# replace logic with constraint object
# introduce a "guessed" heuristic constraint that lets user set constraints that can be loosened if no solution is found

# Manual steps:
# Set starting point and end point
# fill in all constrained variables
# receive a constraint object for that area of code
# add a guessed constraint to the object
# set new starting point and constraint obj as input for mem or reg

# Benefits:
# Can overcome state explosion from out of order constraints
# enables user to debug angr easily

# Issues:
# large binary means doing by hand is time-consuming
# user has to specify guessed constraint
# loosening constraints automatically may lead to errors


# TODO: way to know all vars currently unconstrained

# Improvement:
# - Understanding how a var affects the output
#

# Goals:
# - give user better understanding of variable or function effect
# - improved guidance for angr execution to avoid state explosion

# Technique:
# - break up area with state explosion before occurrence
# - compute the constraint for several branching conditions
# - convert to a valid input set of n inputs
# - patch the model and continue as normal

# Goals:
# - understand how a variable in used in every context in a way that is understood to the user
