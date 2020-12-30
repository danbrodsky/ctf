from z3 import *
import string


flag_len = 29
text = "3cD1Z84acsdf1caEBbfgMeAF0bObA"
alphanum = string.ascii_lowercase + string.ascii_uppercase + string.digits


def find_all_solutions(s, bva):
    while s.check() == sat:
        model = s.model()
        block = []
        out = ""
        for i in range(flag_len):
            c = bva[i]
            out += chr(model[c].as_long())
            block.append(c != model[c])
        s.add(Or(block))
        print(out)


key = [BitVec("v%d" % i, 32) for i in range(flag_len)]
# key = [BitVec(f"v{i:d}", 32) for i in range(flag_len)]
s = Solver()
k = 0

sep = [4, 9, 14, 19, 24]

k = 0
for i in range(flag_len):
    if i in sep:
        s.add(key[i] == ord("-"))
    else:
        s.add(Or([key[i] == ord(c) for c in alphanum]))
    k ^= key[i]
s.add(k == 41)


k = 0
for i in range(flag_len):
    n = key[i] * ord("*")
    v = (
        ((n >> 6) + (n >> 5) & 127)
        ^ (n + ord(text[i]) & 127)
        ^ ord(text[flag_len - i - 1])
    )
    k ^= v
s.add(k == 74)

find_all_solutions(s, key)
