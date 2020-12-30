#include <sys/prctl.h>
#include <sys/socket.h>
#include <sys/syscall.h>
#include <sys/types.h>

#include <linux/audit.h>
#include <linux/filter.h>
#include <linux/seccomp.h>

#define Allow(syscall)                                                         \
  BPF_JUMP(BPF_JMP + BPF_JEQ + BPF_K, SYS_##syscall, 0, 1),                    \
      BPF_STMT(BPF_RET + BPF_K, SECCOMP_RET_ALLOW)

/*
struct sock_filter {	 Filter block
        __u16	code;    Actual filter code
        __u8	jt;	 Jump true
        __u8	jf;	 Jump false
        __u32	k;       Generic multiuse field
};
*/

struct sock_filter filter[] = {
    /* list of allowed syscalls */
    Allow(exit_group), /* exits a processs */
    Allow(brk),        /* for malloc(), inside libc */
    Allow(mmap),       /* also for malloc() */
    Allow(munmap),     /* for free(), inside libc */
    Allow(write),      /* called by printf */
    Allow(fstat),      /* called by printf */
};
struct sock_fprog filterprog = {.len = sizeof(filter) / sizeof(filter[0]),
                                .filter = filter};
