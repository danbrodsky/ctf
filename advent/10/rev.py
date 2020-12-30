pshufd

val1 = 0x96433D0000000000000001
v3 = val1
v4 =


constants: v9, v10, v12, v14, v21, v22

((sh(v9, 0xFF) * v7) + (sh(v9, 0xAA) * v6)) + ((sh(v9, 0x55) * v5) + (sh(v9, 0) * v4))



1000 loop:
    x = v4
    y = max(v21, v4)
    x - ((y+v22)*v21)



0xaa # repeat highest 4 bytes
0x0 # repeat lowest 4 bytes

1 10 420 15080 546320

no3 = 4321
no0 = 10fed
no1 = cba9
no2 = 8765
xmm3 = 4*xmm0 | 3*xmm1 | 2*xmm2 | 1*xmm0
xmm2 = 8*10 | 7*b | 6*6 | 5*1
xmm1 = c*10 | b*b | a*6 | 9*1
xmm0 = 10*10 | f*b | e*6 | d*1





n - c | n - d | n - e | n - f
n - 8 | n - 9 | n - a | n - b
n - 4 | n - 5 | n - 6 | n - 7
n - 0 | n - 1 | n - 2 | n - 3

4 ^ 1234567890123456789 * xmm0 | ...
xmm1 * 3 ^ 1234567890123456789 mod 2^32 | ...

4*(10 f e d)
3*(c b a 9)
2*(8 7 6 5)
1*(4 3 2 )


xmm3_1 = 4 * xmm0_0 + 3 * xmm1_0 + 2 * xmm2_0 + 1 * xmm3_0

4*4 + 8*4 + 12*4


    flag = bytearray("FC14EB09BCAEE7474FE37CC152A5028E8971C88D9623016D71405AEAFD461D23".decode("hex)"))
    for j in range(0,32,2):
        flag[j] ^= curr[2*j]
        flag[j+1] ^= curr[2*j+1]

