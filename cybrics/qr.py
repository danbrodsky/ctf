# with open('qrshell.txt','r') as f:
#     data = f.read()


with open('qrcode.txt','r') as f:
    data = f.read()

out = bytes()

data = data.encode('utf-8')
#print(bytes(data))

for b in data:
    if b == ' ':
        out += b' '
    if b == '\n':
        out += '\n'
    if b != ' ':
        out += b'\xe2\x96\x88'

print(out.decode('utf-8'))
