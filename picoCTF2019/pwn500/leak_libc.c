#include <stdio.h>
#include <stdlib.h>


int main() {
    void * a0 = malloc(0x100);
    void * a1 = malloc(0x100);
    void * a2 = malloc(0x100);
    void * a3 = malloc(0x100);
    void * a4 = malloc(0x100);
    void * a5 = malloc(0x100);
    void * a6 = malloc(0x100);
    void * a7 = malloc(0x100);
    void * a8 = malloc(0x100); // chunk to prevent a7 consolidating with top chunk
    __asm__("int3");

    free(a0); // a0 to a6 written to tcache bins
    free(a1); // prev_inuse bits not changed since tcache does not update prev_inuse
    free(a2);
    free(a3);
    free(a4);
    free(a5);
    free(a6);
    free(a7); // a7 written to unsorted bin, a8 prev_inuse set to true
    __asm__("int3");

    void * b0 = malloc(0x100); // a6 used from tcache bin
    __asm__("int3");

    void * b1 = malloc(0x100); // a5
    void * b2 = malloc(0x100); // a4
    void * b3 = malloc(0x100); // a3
    void * b4 = malloc(0x100); // a2
    void * b5 = malloc(0x100); // a1
    void * b6 = malloc(0x100); // a0
    __asm__("int3");

    void * a9 = malloc(0x100); // a7 from unsorted bin
    __asm__("int3");
/*
+------------------------------+------------------------------+
|     a7 free chunk header     |  a9 allocated chunk header   |
+==============================+==============================+
|         a7.prev_size         |         a9.prev_size         |
+------------------------------+------------------------------+
|           a7.size            |           a9.size            |
+------------------------------+------------------------------+
|            a7.fd             |        a9.data_start         |
+------------------------------+                              + // a9.data_start readable section leaks libc
|     a7.bk (libc address)     |                              |
+------------------------------+------------------------------+
*/
    printf("%lx\n", *(long *)a9);
    printf("%lx\n", *(long *)(a9+8)); // a7.bk pointer ==> main_arena+(some offset based on libc version)
    __asm__("int3");

    return 0;
}
