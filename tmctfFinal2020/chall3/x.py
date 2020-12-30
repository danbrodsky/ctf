def l(s):
    r = ""
    for i in range(1,len(s)):
        k = s[i]
        if k >= 33 and k <= 126:
            r = r + chr(33+((k+14)%94))
        else:
            r = r + chr(k)
    print(r)
    open('stage4.b64', 'w').write(r)

BASE62 = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
def decode(string, alphabet=BASE62):
    """Decode a Base X encoded string into the number

    Arguments:
    - `string`: The encoded string
    - `alphabet`: The alphabet to use for decoding
    """
    base = len(alphabet)
    strlen = len(string)
    num = 0

    idx = 0
    for char in string:
        power = (strlen - (idx + 1))
        num += alphabet.index(char) * (base ** power)
        idx += 1

    return num
