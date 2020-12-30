from z3 import *
import string
key = '3cD1Z84acsdf1caEBbfgMeAF0bObA'
alp = string.ascii_lowercase + string.ascii_uppercase + string.digits
flag_len = 29


def find_all_posible_solutions(s):
    while s.check() == sat:
        model = s.model()
        block = []
        out = ''
        for i in range(flag_len):
            c = globals()['b%i' % i]
            out += chr(model[c].as_long())
            block.append(c != model[c])
        s.add(Or(block))
        print(out) 

def main():
    s = Solver()
    k = 0
    for i in range(flag_len):
        globals()['b%d' % i] = BitVec('b%d' % i, 32)
        c = globals()['b%d' % i]
        
        if (i + 1) % 5 == 0:
            s.add(c == ord('-'))
        else:
            s.add(Or([c == ord(i) for i in alp]))
        k ^= c

    s.add(k == 41)
    k = 0
    for i in range(flag_len):
        c = globals()['b%d' % i]
        n = c * ord('*')
        v = ((n >> 6) + (n >> 5) & 127) ^ (n + ord(key[i]) & 127) ^ ord(key[flag_len - i - 1])
        k ^= v

    s.add(k == 74)
    find_all_posible_solutions(s)    



    
if __name__ == "__main__":
    sys.exit(main())
