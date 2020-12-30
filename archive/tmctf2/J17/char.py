allowed = []
for i in range(255):
    v = bin(i)[2:]
    v = v.rjust(8,'0')
    print(v)
    if v[-5:] != '00000' and v[-8] != '1' and not ( v[-5:] == '11011'):
        allowed.append(i)
print(''.join(map(lambda x: chr(x), allowed)))
