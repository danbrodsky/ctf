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

break printf_positional if $rbx == 0xffff
break printf_positional

# set {ulong} 0x13371337 = 0xdeadbeef

# idabridge 0.0.0.0:2305

# call (void*) memset(start_addr, char, size)
# call (void*) mprotect(start_addr, size, X|W|R)

# set {unsigned long} memory_address = new_value

start
continue
finish
si
context

kill

pi hex(0xdb90 + 264)

tel $rsp
tel 0x7fffffffdc08
tel 0x7fffffffdb30
x/10i 0x7fffffffdb90
b *0x7fffffffdc98
disas main
delete 1
p main
grep 0x90

vmmap
