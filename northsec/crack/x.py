from z3 import *

v = BitVec("v0", 64)

S = Solver()

v2 = (v & 1) + 2
v3 = v + 0x21a3937

S.add(v1 << v2 == v3)

if S.check() == sat:
    print(S.model())

