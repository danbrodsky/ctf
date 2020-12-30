#!/usr/bin/env python3

import angr
import sys
import claripy
from IPython import embed
import logging
import os


import signal

# logging.getLogger("angr.sim_manager").setLevel("DEBUG")

def kys():
    os.system("kill %d" % os.getpid())


def sigint_handler(signum, frame):
    print("Stopping Execution for Debug. If you want to kill the programm issue: kys()")
    embed()


signal.signal(signal.SIGINT, sigint_handler)

argv0 = "/home/esc/ctf/plaidctf2020/reee/reee"

proj = angr.Project(
    "/home/esc/ctf/plaidctf2020/reee/reee", support_selfmodifying_code=True, load_options={"auto_load_libs": False})
proj.hook_symbol(
    "__libc_start_main", angr.SIM_PROCEDURES["glibc"]["__libc_start_main"]()
)
proj.hook_symbol(
    "ptrace", angr.SIM_PROCEDURES["stubs"]["ReturnUnconstrained"](return_value=0)
)
# proj.hook(0x40071a, angr.SIM_PROCEDURES['stubs']['ReturnUnconstrained'](return_value=0))

flag = claripy.BVS("flag", 8 * 34)  # no clue how big the flag should be

argv = [argv0, flag]

init_state = proj.factory.full_init_state(add_options=angr.options.unicorn, args=argv)
init_state.options.add(angr.sim_options.UNICORN_AGGRESSIVE_CONCRETIZATION)

flag_bytes = flag.chop(bits=8)
init_state.solver.add(
    flag_bytes[0] == b"p",
    flag_bytes[1] == b"c",
    flag_bytes[2] == b"t",
    flag_bytes[3] == b"f",
    flag_bytes[4] == b"{",
    flag_bytes[-2] == b"}",
    flag_bytes[-1] == 0,
)

for c in flag_bytes[5:-2]:
    init_state.solver.add( c > 0x20 , c < 0x7f)


sim = proj.factory.simgr(init_state, stashes={"active": [init_state], "found": [],})

sim.use_technique(angr.exploration_techniques.DFS())


# def debug_getAddr(state):
#     print("Last address", state.regs.rip)


# init_state.inspect.b("return", action=debug_getAddr)


# sim.explore(find=0x40064E).unstash(from_stash="found", to_stash="unpacked")
# sim.drop(stash="active")
# sim.stash(from_stash="unpacked", to_stash="active")


outer_counter = 0
inner_counter = 0
def debug_whileloop(state):
    global inner_counter, outer_counter
    inner_counter = 0
    outer_counter += 1
    print(f"Top of while loop {outer_counter}/1337 sim: {sim}")

def debug_xor(state):
    global inner_counter
    inner_counter += 1
    print(f"Xoring {inner_counter}\r", end="")

XORING = 0x004006be
WHILE_LOOP = 0x004006cb

init_state.inspect.b('instruction', when=angr.BP_AFTER, instruction=WHILE_LOOP,
        action=debug_whileloop)

# init_state.inspect.b('instruction', when=angr.BP_AFTER, instruction=XORING,
#         action=debug_xor)

init_state.inspect.b('instruction', when=angr.BP_AFTER, instruction=0x4006e5,
                     action=lambda x : print(f"finished unpacking, sim: {sim}"))

def check_correct(state):
    stdout = state.posix.dumps(sys.stdout.fileno())
    return "Correct" in stdout.decode()


def check_wrong(state):
    stdout = state.posix.dumps(sys.stdout.fileno())
    return "Wrong" in stdout.decode()


# sim.explore(find=check_correct, avoid=check_wrong)
# sim.use_technique(angr.exploration_techniques.Explorer())
sim.explore(find=check_correct, avoid=check_wrong)


if sim.found:
    solution_state = sim.found[0]
    embed()

    # for char in flag.chop(bits=8):
    #     solution_state.add_constraints(char >= 0x20, char <= 0x80)

    #     solution_state.add_constraints(flag.get_bytes(0, 5) == "pctf{")

    # solution = solution_state.solver.eval(flag, cast_to=bytes).decode()

    # print(solution)
