#!/usr/bin/env python3
from z3 import *


S = Solver()
# password = [BitVec("pass_%s" % i, 8) for i in range(10)]
# chunk1 = [BitVec("ch1_%s" % i, 8) for i in range(256)]
# chunk2 = [BitVec("ch2_%s" % i, 8) for i in range(256)]
(P0, P1, P2, P3, P4, P5, P6, P7, P8, P9) = BitVecs(
    "P0, P1, P2, P3, P4, P5, P6, P7, P8, P9", 8,
)


password = Array("pass", BitVecSort(8), BitVecSort(8))
password = Store(password, 0, P0)
password = Store(password, 1, P1)
password = Store(password, 2, P2)
password = Store(password, 3, P3)
password = Store(password, 4, P4)
password = Store(password, 5, P5)
password = Store(password, 6, P6)
password = Store(password, 7, P7)
password = Store(password, 8, P8)
password = Store(password, 9, P9)


(CO0, CO1, CO2, CO3, CO4, CO5, CO6, CO7, CO8, CO9) = BitVecs(
    "CO0, CO1, CO2, CO3, CO4, CO5, CO6, CO7, CO8, CO9", 8,
)
(CT0, CT1, CT2, CT3, CT4, CT5, CT6, CT7, CT8, CT9) = BitVecs(
    "CT0, CT1, CT2, CT3, CT4, CT5, CT6, CT7, CT8, CT9", 8,
)
chunk1 = Array("pass", BitVecSort(8), BitVecSort(8))
chunk1 = Store(chunk1, 0, CO0)
chunk1 = Store(chunk1, 1, CO1)
chunk1 = Store(chunk1, 2, CO2)
chunk1 = Store(chunk1, 3, CO3)
chunk1 = Store(chunk1, 4, CO4)
chunk1 = Store(chunk1, 5, CO5)
chunk1 = Store(chunk1, 6, CO6)
chunk1 = Store(chunk1, 7, CO7)
chunk1 = Store(chunk1, 8, CO8)
chunk1 = Store(chunk1, 9, CO9)
chunk2 = Array("pass", BitVecSort(8), BitVecSort(8))
chunk2 = Store(chunk2, 0, CT0)
chunk2 = Store(chunk2, 1, CT1)
chunk2 = Store(chunk2, 2, CT2)
chunk2 = Store(chunk2, 3, CT3)
chunk2 = Store(chunk2, 4, CT4)
chunk2 = Store(chunk2, 5, CT5)
chunk2 = Store(chunk2, 6, CT6)
chunk2 = Store(chunk2, 7, CT7)
chunk2 = Store(chunk2, 8, CT8)
chunk2 = Store(chunk2, 9, CT9)
# for i in range(256):
#     chunk1 = Store(chunk1, i, 0)
#     chunk2 = Store(chunk2, i, 0)


# for i in range(128):
#     S.add(password[i] >= 20)
#     S.add(password[i] <= 128)

# for i in range(128):
#     S.add(chunk1[i] >= 0)
#     S.add(chunk1[i] <= 255)

#     S.add(chunk2[i] >= 0)
#     S.add(chunk2[i] <= 255)

# A = [BitVec("char_%s" % i, 8) for i in range(20)]
# B = [BitVec("char_%s" % i, 8) for i in range(20)]
# C = [BitVec("char_%s" % i, 8) for i in range(20)]
# D = [BitVec("char_%s" % i, 8) for i in range(20)]
# E = [BitVec("char_%s" % i, 8) for i in range(20)]
# PC = [BitVec("char_%s" % i, 8) for i in range(20)]

(
    A0,
    A1,
    A2,
    A3,
    A4,
    A5,
    A6,
    A7,
    A8,
    A9,
    A10,
    A11,
    A12,
    A13,
    A14,
    A15,
    A16,
    A17,
    A18,
    A19,
    A20,
) = BitVecs(
    "A0, A1, A2, A3, A4, A5, A6, A7, A8, A9, A10, A11, A12, A13, A14, A15, A16, A17, A18, A19, A20",
    8,
)

(
    B0,
    B1,
    B2,
    B3,
    B4,
    B5,
    B6,
    B7,
    B8,
    B9,
    B10,
    B11,
    B12,
    B13,
    B14,
    B15,
    B16,
    B17,
    B18,
    B19,
    B20,
) = BitVecs(
    "B0, B1, B2, B3, B4, B5, B6, B7, B8, B9, B10, B11, B12, B13, B14, B15, B16, B17, B18, B19, B20",
    8,
)

(
    C0,
    C1,
    C2,
    C3,
    C4,
    C5,
    C6,
    C7,
    C8,
    C9,
    C10,
    C11,
    C12,
    C13,
    C14,
    C15,
    C16,
    C17,
    C18,
    C19,
    C20,
) = BitVecs(
    "C0, C1, C2, C3, C4, C5, C6, C7, C8, C9, C10, C11, C12, C13, C14, C15, C16, C17, C18, C19, C20",
    8,
)

(
    D0,
    D1,
    D2,
    D3,
    D4,
    D5,
    D6,
    D7,
    D8,
    D9,
    D10,
    D11,
    D12,
    D13,
    D14,
    D15,
    D16,
    D17,
    D18,
    D19,
    D20,
) = BitVecs(
    "D0, D1, D2, D3, D4, D5, D6, D7, D8, D9, D10, D11, D12, D13, D14, D15, D16, D17, D18, D19, D20",
    8,
)

(
    E0,
    E1,
    E2,
    E3,
    E4,
    E5,
    E6,
    E7,
    E8,
    E9,
    E10,
    E11,
    E12,
    E13,
    E14,
    E15,
    E16,
    E17,
    E18,
    E19,
    E20,
) = BitVecs(
    "E0, E1, E2, E3, E4, E5, E6, E7, E8, E9, E10, E11, E12, E13, E14, E15, E16, E17, E18, E19, E20",
    8,
)

# A = [Int("a_%s" % i) for i in range(20)]
# B = [Int("b_%s" % i) for i in range(20)]
# C = [Int("c_%s" % i) for i in range(20)]
# D = [Int("d_%s" % i) for i in range(20)]
# E = [Int("e_%s" % i) for i in range(20)]
# PC = [Int("pc_%s" % i) for i in range(20)]


S.add(A0 == 0, B0 == 0, C0 == 0, D0 == 0, E0 == 0)

# for i in range(20):
#     S.add(A[i] >= 0, B[i] >= 0, C[i] >= 0, D[i] >= 0, E[i] >= 0, PC[i] >= 0)
#     S.add(A[i] <= 255, B[i] <= 255, C[i] <= 255, D[i] <= 255, E[i] <= 255, PC[i] <= 255)


# S.add(B1 == Select(password, BV2Int(E0)) - 0x46)
S.add(B1 == password[E0] - 0x46)

S.add(chunk1[D0] == B1, D2 == D0 + 1)
S.add(chunk2[C0] == B1, C2 == C0 + 1)
S.add(A1 == 0x04)

S.add(B2 == A1)
S.add(E1 == E0 + B2)
S.add(B3 == password[E1] - 0x46)
S.add(chunk1[D2] == B3, D3 == D2 + 1)
S.add(chunk2[C2] == B3, C3 == C2 + 1)
# # 69
# S.add(A2 == 0x02)
# S.add(A3 == 0x1B)
S.add(E2 == E1 + B3)
S.add(A4 == 0x00)
S.add(B4 == chunk1[D4], D4 == D3 - 1)
S.add(B5 == A4, A5 == B4)
S.add(B6 == Select(password, E1) - 0x46)
S.add(B6 == A5)
S.add(B8 == A5, A6 == B6)
S.add(B9 == chunk1[D5], D5 == D4 - 1)
S.add(B10 == B9 + A6)
# 69
S.add(A7 == 0x06)
S.add(B10 == A7)
S.add(B11 == chunk2[C4], C4 == C3 - 1)
S.add(A8 == B11)
S.add(B12 == Select(password, E1) - 0x46)
S.add(B13 == B12 * A8)
S.add(A9 == B13)
S.add(B14 == chunk2[C5], C5 == C4 - 1)
S.add(B15 == B14 * A9)
# 69
S.add(A10 == 6)
# S.add(B15 == A10)
# 69
S.add(A11 == 0xFB)
S.add(B17 == A11, A12 == B15)
S.add(B18 == A12)
S.add(E3 == E2 + B18)
# 8e
# 76
S.add(B19 == password[E3] - 0x46)  # E wrong here maybe
S.add(A13 == 0x1B)
S.add(B19 == A13)
S.check()
m = S.model()
print(sorted([(d, m[d]) for d in m], key=lambda x: str(x[0])))

# 77
# 69
# S.add(A14 == 0x01)
# S.add(B21 == A14)
# S.add(E[n + 1] == E[n] + B[n])
# 5c
# S.add(B[n] == password[E[n]] - 0x46)
# S.add(A[n] == 0xfd)
# S.add(B[n] != A[n])
# # 69
# S.add(chunk1[D[n]] == B[n], D[n] == D[n] + 1)
# S.add(A[n] == 0x03)
# S.add(B[n] == A[n])
# S.add(E[n+1] == E[n] + B[n])
# 4f
# S.add(B[n] == password[E[n]] - 0x46)
# S.add(A[n] == 0x00)
# S.add(B[n+1] == A[n], A[n+1] == B[n])
# S.add(B[n] == chunk1[D[n]], D[n+1] == D[n] + 1)
# S.add(B[n+1] == A[n])
# S.add(chunk1[D[n]] == B[n], D[n] == D[n] + 1)
# # 69
# S.add(A[n] == 0x02)
# S.add(B[n] == A[n])
# 8e
# 1b
# S.add(B[n] == password[E[n]] - 0x46)
# S.add(A[n] == 0xd2)
# S.add(B[n] != A[n])
# 6a
# # 69
# S.add(A[n] == 0xS.add(chunk2[C[n]] == B[n], C[n+1] == C[n] + 1))
# S.add(B[n] == A[n])
# # 87
# # 69
# S.add(B[n] == password[E[n]] - 0x46)
# S.add(chunk2[C[n]] == B[n], C[n+1] == C[n] + 1)
# S.add(A[n] == 0x0e)
# S.add(B[n] != A[n])
# 4f
# S.add(A[n] == 0x05)
# S.add(B[n] == A[n])
# S.add(E[n+1] == E[n] + B[n])
# S.add(B[n] == password[E[n]] - 0x46)
# S.add(A[n] == B[n])
# S.add(B[n] == chunk2[C[n]], C[n+1] == C[n] - 1)
# f4
# S.add(A[n] == B[n])
# S.add(B[n] == chunk1[D[n]], D[n+1] == D[n] + 1)
# S.add(B[n] != A[n])
# S.add(chunk1[D[n]] == B[n], D[n] == D[n] + 1)
# # 76
# S.add(A[n] == 0x01)
# S.add(B[n] == A[n])
# S.add(E[n+1] == E[n] + B[n])
# S.add(B[n] == password[E[n]] - 0x46)
# S.add(A[n] == B[n])
# S.add(chunk1[D[n]] == B[n], D[n] == D[n] + 1)
# S.add(B[n] != A[n])
# 5c
