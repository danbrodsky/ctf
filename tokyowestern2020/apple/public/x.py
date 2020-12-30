from claripy import *
from IPython import embed
import angr

p = angr.Project("./x")
i = BVS("i", 16*8)

def get_addr(state):
    print(hex(state.addr))


s = p.factory.entry_state(stdin=i)
s.inspect.b('irsb', when=angr.BP_AFTER, action=get_addr)

for byte in i.chop(bits=8):
    s.add_constraints(
        And(
            byte <= 0x7e,
            byte >= 0x21
        )
    )


sm = p.factory.simulation_manager(s)

sm.explore(find=0x4014c4)

embed()
