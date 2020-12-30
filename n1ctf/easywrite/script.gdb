# catch syscall read
# catch syscall lseek
# disable 1 2

# commands 1 (if read syscall then do this)
#  disable 1 2
#  continue
# end

# commands 2 (if lseek syscall then do this)
#  if $rdi == 31
#   enable 1 2
#   continue
#  else
#   continue
#  end
# end

# set {ulong} 0x13371337 = 0xdeadbeef

# idabridge 0.0.0.0:2305

# call (void*) memset(start_addr, char, size)
# call (void*) mprotect(start_addr, size, X|W|R)

# set {unsigned long} memory_address = new_value

start
continue

kill

rwatch *0x00007ffff7f7bcd0

b *0x55555555532d
b write
b malloc

set {unsigned long} 0x7ffff7f78a40 = 0x4141414141414141

call (void*) strcpy(0x7ffff7f78a40, "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA")

heap chunks
heap bins
grep 0x5555555595a0

x/8g 0x5555555595a0
