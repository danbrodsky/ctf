# from pwn import *

# r = remote("0.0.0.0", 9998)

import logging
import angr as a
import claripy as c
from IPython import embed

logging.getLogger("angr.sim_manager").setLevel("DEBUG")


def run():
    p = a.Project("angrmanagement", load_options={"auto_load_libs": False})

    # hook statically linked functions to use angr versions
    # program dynamically linked so don't need
    # p.hook()

    # @p.hook(0x401244)
    # def input_length(state):
    #     state.regs.rax = 32

    password = c.BVS("pass", 32 * 8)
    payload = c.Concat(password, c.BVV(0, 8))

    state = p.factory.entry_state(
        args=["angrmanagement"],
        # add_options={"BYPASS_UNSUPPORTED_SYSCALL"},
        stdin=payload,
    )

    for b in password.chop(8):
        state.add_constraints(b >= 0x21, b <= 0x7E)

    def debug_getAddr(state):
        print("Last address", state.regs.rip)

    state.inspect.b("return", action=debug_getAddr)

    sm = p.factory.simulation_manager(state)
    sm.explore(find=0x402360, avoid=[0x4023B9])

    # for out in sm.deadended:
    #     candidate = out.posix.dumps(1)
    print(sm.found[0].solver.eval(password, cast_to=bytes))
    embed()


run()
