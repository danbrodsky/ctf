#!/usr/bin/env python3

# dba = digit_box_array
# _digit_box_array[0] == 0x4
# (dba[1] ^ 0x36) & 0xff == 0x35
# dba[2] & 0xff == 0x9

# dba[4]
#
# dba[3] & 0xff << dba[4] & 0x1f == 8


from z3 import *

S = Solver()

a = BitVec("a", 8)
b = BitVec("b", 8)

S.add(a >= 0)
S.add(b >= 0)
S.add(a <= 9)
S.add(b <= 9)

S.add(a & 0xff << (b & 0x1f) == 8)

if S.check() == sat:
    print(S.model())
else:
    print("No model")
