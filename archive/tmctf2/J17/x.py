from z3 import *

variables = [BitVec("char_%d" % i, 64) for i in range(16)]
v5 = Real('v5')
res_code = Real('res_code')

S = Solver()
key = "X"*16

total = 0
for c in variables:
    total += ~(c >> 6);

S.add( v5 == ~(variables[0] >> 6) +
        ~(variables[1] >> 6) +
        ~(variables[2] >> 6) +
        ~(variables[3] >> 6) +
        ~(variables[4] >> 6) +
        ~(variables[5] >> 6) +
        ~(variables[6] >> 6) +
        ~(variables[7] >> 6) +
        ~(variables[8] >> 6) +
        ~(variables[9] >> 6) +
        ~(variables[10] >> 6) +
        ~(variables[11] >> 6) +
        ~(variables[12] >> 6) +
        ~(variables[13] >> 6) +
        ~(variables[14] >> 6) +
        ~(variables[15] >> 6))

S.add(res_code == 2048 & 0xFFFFFF80 | 16 & 0x7F | ((v5 & 0x3FFF) << 32) | ((v5 & 0x7FFF) << 46))

S.add(res_code != 4)

print(S.check())
print(S.model())

# v6 = []
# for i in range(0,(res_code >> 7) & 0x1ffffff):
#     result = i
#     flag_byte = key[i]

#     v6.append((((flag_byte >> 5) & 1) << 15) | ((((flag_byte >> 5) & 1) << 14) | ((((flag_byte >> 5) & 1) << 13) | ((((flag_byte >> 5) & 1) << 10) | ((((flag_byte >> 4) & 1) << 9) | ((((flag_byte >> 3) & 1) << 8) | (((flag_byte >> 5) & 1) << 7) | ((((flag_byte >> 5) & 1) << 6) | ((32 * ((flag_byte >> 5) & 1)) | ((4 * ((flag_byte >> 2) & 1)) | ((2 * ((flag_byte >> 1) & 1)) | flag_byte & 1) & 0xFB) & 0xDF) & 0xBF) & 0x7F) & 0xFDFF) & 0xFBFF) & 0xDFFF) & 0xBFFF) & 0x7FFF)

#     dword_4045E0 = []
#     if flag_byte >> 7 == 0:
#         dword_4045E0.append(1)
#     else:
#         dword_4045E0.append(0)

#     qword_4043D0.append(~v6[i])

# def fun_404280(a1=-4834600866076456343, a2=5409625251193285689):
#     v4 = []
#     for i in range(0x20):
#         v4.append(i * (a2 - 1) * (a1 - 1))

# def fun_404280(a1=-4834600866076456343, a2=5409625251193285689):
#     for i in range(0x1F):
#         if ( (a2 + 1) * (a1 + 1) % (i + 1) or i <= 0 ):
#             v4[i - 1] *= (a2 + 1) * (a1 + 1);
#         else:
#             v4[i] = (a2 + 1) * (a1 + 1);
#     qword_4042E8  = 0xc92ff83c700eb140
#     qword_4042F0  = 0xc92ff83c700eb140 + 0x215ec8a2
