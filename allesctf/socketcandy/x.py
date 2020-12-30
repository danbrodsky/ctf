from IPython import embed
from collections import defaultdict
from binascii import unhexlify

data = open("dump.txt").read()

data = data.splitlines()

# embed()

data = map(lambda d: d.split(" "), data)

msgs = defaultdict(list)
for d in data:
    if len(d) > 4:
        split_hex = [d[4][i:i+2] for i in range(0,len(d[4]), 2)]
        while len(split_hex) != 8:
            split_hex.append('00')
        split_hex = ''.join(split_hex)
        if split_hex not in msgs[d[2]]:
            msgs[d[2]].append(split_hex)

out = []
for can_id, filters in sorted(msgs.items()):
    # out.append(bytes(f"{can_id}\n".encode('latin-1')))
    for f in filters:
        out.append(unhexlify(f))

# out = []
# for can_id, filters in msgs.items():
#     curr = f"< muxfilter 0 0 {can_id} {len(filters)+1} 00 00 00 00 00 00 00 00 "
#     for f in filters:
#         curr += f"{f} "
#     curr += ">"
#     out.append(curr)

open("data.txt", 'wb').write(b'\n'.join(out))

# out = []
# for d in data:
#     if len(d) > 4 and d[2] == '156':
#         if unhexlify(d[4]) not in out:
#             out.append(unhexlify(d[4]))

# data = out

# open("secret.txt", 'wb').write(b''.join(data))
