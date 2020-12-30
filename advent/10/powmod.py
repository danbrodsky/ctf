from numpy.core.numeric import identity, dot
import numpy as np
from pwn import *

M = np.array([[1,2,3,4],
              [5,6,7,8],
              [9,0xa,0xb,0xc],
              [0xd,0xe,0xf,0x10]], np.uint64)
n = 1234567890123456789
mod_val = 0x96433d
def matrix_powmod(M, n, mod_val):
    if n==0:
        M = M.copy()
        M[:] = identity(M.shape[0])
        return M

    if n % 2 == 1:
        return dot(M, matrix_powmod(M, n - 1, mod_val)) % mod_val

    D = matrix_powmod(M, n / 2, mod_val)
    return dot(D,D) % mod_val

ans = matrix_powmod(M,n,mod_val)

ans = np.flip(ans, axis=1)

print(ans)

out = []
for row in ans:
    full = ""
    block = hex(row[0])[2:].replace("L", "").rjust(8, "0")
    full += "".join(reversed([block[i:i+2] for i in range(0,8,2)]))
    block = hex(row[1])[2:].replace("L", "").rjust(8, "0")
    full += "".join(reversed([block[i:i+2] for i in range(0,8,2)]))
    block = hex(row[2])[2:].replace("L", "").rjust(8, "0")
    full += "".join(reversed([block[i:i+2] for i in range(0,8,2)]))
    block = hex(row[3])[2:].replace("L", "").rjust(8, "0")
    full += "".join(reversed([block[i:i+2] for i in range(0,8,2)]))
    out.append("".join(reversed([full[i:i+8] for i in range(0,32,8)])))
out = ''.join(out)
print(out)

def xor(a, b):
    a = bytearray(a)
    b = bytearray(b)
    c = bytearray()
    for j in range(0,32,2):
        # print(b[2*j])
        # print(a[j])
        # pause()
        c.append(a[j] ^ b[2*j])
        c.append(a[j+1] ^ b[2*j+1])
    return bytes(c)

flag = "FC14EB09BCAEE7474FE37CC152A5028E8971C88D9623016D71405AEAFD461D23".decode("hex")
out = out.decode("hex")
# out = "\x00\x8e\x15\x60\x00\x06\xfd\x88\x00\x6f\xbe\x96\x00\x7e\xe9\xfb\x00\x3c\xb3\xd8\x00\x0b\x55\xc2\x00\x09\x2c\xc7\x00\x6e\x11\xee\x00\x81\x95\x8d\x00\x0f\xad\xfc\x00\x38\xde\x35\x00\x5d\x39\xe1\x00\x30\x34\x05\x00\x14\x06\x36\x00\x68\x8f\xa3\x00\x4c\x61\xd4"
print(xor(flag, out))

    # binary decompositon to reduce the number of matrix
    # multiplications for n > 3
    # beta = binary_repr(n)
    # Z, q, t = M, 0, len(beta)
    # print(beta)
    # print(len(beta))
    # while beta[t-q-1] == '0':
    #     Z = dot(Z, Z) % mod_val
    #     q += 1
    # result = Z
    # for k in range(q+1, t):
    #     Z = dot(Z, Z) % mod_val
    #     if beta[t-k-1] == '1':
    #         result = dot(result, Z) % mod_val
    # return result % mod_val


# function Matrix_ModExp(Matrix A, int b, int c) is
#     if b == 0 then
#         return I  // The identity matrix
#     if (b mod 2 == 1) then
#         return (A * Matrix_ModExp(A, b - 1, c)) mod c
#     Matrix D := Matrix_ModExp(A, b / 2, c)
#     return (D * D) mod c
