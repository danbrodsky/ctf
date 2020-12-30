
# start
# rwatch *0x5555555be9b0
# delete 1

c
context
# pi hex(ord('D'))
# bt
# tel
#dis 0x000055555573a82
#disassemble *0x0000555555573a82
# x/40i 0x0000555555573a82
# vmmap
# finish
ni


b *0x555555573F90
b *0x55555557406a
b *0x555555574014
xref 0x5555555c4d50
watch *0x00005555555c4d50

x/40g 0x5555555a65b7
