# catch syscall read
# catch syscall lseek
# disable 1 2

# commands 2 (if read syscall then do this)
#  disable 1 2
#  continue
# end

# commands 3 (if lseek syscall then do this)
#  if $rdi == 31
#   enable 1 2
#   continue
#  else
#   continue
#  end
# end

# set {ulong} 0x13371337 = 0xdeadbeef

# idabridge 0.0.0.0:2305

handle SIGSEGV nostop pass
handle SIGFPE nostop pass
# handle SIGTRAP nostop pass
handle SIGALRM nostop pass
handle SIGILL nostop pass
handle all pass nostop
b *0x400de0

signal SIGTRAP

display/b 0x6021e4
display/b 0x6021e5
display/b 0x6021e6
display/b 0x6021e7
display/b 0x6021e8
display/b 0x602468

file signal_of_hope

start
continue
run

kill
