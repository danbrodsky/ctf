    BITS 64
    mov rsi, 0x602140
    mov al, [rsi+0x22]
    shr al, 0x44
    test al, 1
    jnz yes
    int3
yes:
    mov rax, 0x0
    jmp rax


