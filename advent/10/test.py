import numpy as np

modexp = np.frompyfunc(pow, 3, 1)
print(np.flip(modexp(np.array([[1,2,3,4], [5,6,7,8], [9,10,11,12], [13,14,15,16]]), 1234567890123456789, 0x96433d).astype(int), axis=1))
