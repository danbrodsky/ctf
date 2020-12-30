symbols = ["00000068 __exit",
"00001038 _strcat",
"000000ca _geta4",
"00000ef0 _bzero",
"00000430 _decrypt_flag__FPc",
"00001190 __etext",
"00000e94 _rand",
"00000348 _retry_flag__Fv",
"00000ed4 ___umodsi3",
"00000ec8 _srand",
"00000e74 ___divsi3",
"00000e74 _ldiv",
"00000bd4 ___initcommandline",
"00001128 ___main",
"00000104 _start_timer__FP11timerequesti",
"00000258 _check_flag__Fv",
"00000182 _set_text__FPCc",
"000010b8 ___initlibraries",
"00000f58 _bcopy",
"000010f8 ___exitlibraries",
"00000e84 _strcpy",
"00000000 __stext",
"00000e68 ___modsi3",
"00000ee0 ___udivsi3",
"00000e74 _div",
"00000de0 ___exitcommandline",
"0000104c ___mulsi3",
"000004de _main",
"00001134 ___request"
]

f = open("symbols.ghidra", "a")
for s in symbols:
    addr, name = s.split(" ")
    addr = hex(int(addr,16) + 2224128)
    f.write(f"{name} {addr} f\n")
