from z3 import *

pbParm1 = [BitVec("char_%d" % i, 8) for i in range(16)]

S = Solver()

S.add(pbParm1[0] == 0x76 ,  pbParm1[1] ^ pbParm1[0] == 0x4e ,  pbParm1[2] ^ pbParm1[1] == 0x1e ,  pbParm1[3] ^ pbParm1[2] == 0x15 ,  pbParm1[4] ^ pbParm1[3] == 0x5e ,  pbParm1[5] ^ pbParm1[4] == 0x1c ,  pbParm1[6] ^ pbParm1[5] == 0x21 ,  pbParm1[7] ^ pbParm1[6] == 1 ,  pbParm1[8] ^ pbParm1[7] == 0x34 ,  pbParm1[9] ^ pbParm1[8] == 7 ,  pbParm1[10] ^ pbParm1[9] == 0x35 ,  pbParm1[0xb] ^ pbParm1[10] == 0x11 ,  pbParm1[0xc] ^ pbParm1[0xb] == 0x37 ,  pbParm1[0xd] ^ pbParm1[0xc] == 0x3c , pbParm1[0xe] ^ pbParm1[0xd] == 0x72 ,  pbParm1[0xf] ^ pbParm1[0xe] == 0x47)

S.check()

print(  S.model() )


sol = {"14": 63,
 "11": 70,
 "8": 101,
 "10": 87,
 "13": 77,
 "15": 120,
 "6": 80,
 "2": 38,
 "7": 81,
 "1": 56,
 "9": 98,
 "4": 109,
 "3": 51,
 "5": 113,
 "12": 113,
 "0": 118}

out = [""] * 16
for i in sol.keys():
    out[int(i)] = chr(sol[i])
print(''.join(out))
