import string


def orv(alpha):
    return ord(alpha) - 97



def freq(data):
    ss = data.lower().split(' ')

    print(ss)

    count1 = [0] * 26
    count2 = [0] * (26*26)

    for s in ss:
        for i in range(0, len(s), 2):
            chunk = s[i:i+2]


            print(chunk)
            if len(chunk) == 2:  ## if it's a bigram
                if chunk[0] not in string.ascii_letters or chunk[1] not in string.ascii_letters:
                    continue
                count2[ orv(chunk[0])*26 + orv(chunk[1]) ] += 1
            elif len(chunk) == 1:  ## if it's last odd character
                if chunk[0] not in string.ascii_letters:
                    continue
                count1[orv(chunk[0])] += 1
    print( count1)
    return count2

with open('flag.enc', 'r') as file:
    data = file.read()

f = freq(data)


with open('book.enc', 'r') as file:
    data = file.read()

b = freq(data)

c= 0
for i, bi in enumerate(f):
    if f[i] > 0 and not b[i] > 100:
        c += 1
        print(b[i])

print(c)

