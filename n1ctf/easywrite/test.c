#include <stdlib.h>
#include <stdio.h>
#include <unistd.h>

struct malloc_chunk {

    unsigned long      mchunk_prev_size;  /* Size of previous chunk (if free).  */
    unsigned long      mchunk_size;       /* Size in bytes, including overhead. */

    struct malloc_chunk* fd;         /* double links -- used only if free. */
    struct malloc_chunk* bk;

    /* Only used for large blocks: pointer to next larger size.  */
    struct malloc_chunk* fd_nextsize; /* double links -- used only if free. */
    struct malloc_chunk* bk_nextsize;
};

struct malloc_chunk fake_ptr;
struct malloc_chunk fast_bin_chunk;

int main() {

    printf("%p\n", &fake_ptr);
    printf("%p\n", &fast_bin_chunk);
    fake_ptr.fd = &fast_bin_chunk;
    fake_ptr.bk = &fast_bin_chunk;
    fake_ptr.mchunk_size = 0x10;
    fake_ptr.fd_nextsize = 0x30;
    /* fast_bin_chunk.fd = &fake_ptr; */
    /* fast_bin_chunk.bk = &fake_ptr; */
    fast_bin_chunk.mchunk_size = 0x30;
    write(1,"wtf",3);
    void* r = malloc(0x300);
    read(0, r, 0x299);;
    void* q = malloc(0x30);
    void* w = malloc(0x30);
    void* e = malloc(0x30);
    void* t = malloc(0x30);
    void* y = malloc(0x30);
    void* u = malloc(0x30);
    void* i = malloc(0x30);
    return 0;
}
