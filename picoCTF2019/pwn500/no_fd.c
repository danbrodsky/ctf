#include <stdlib.h>

int main() {
    int size1 = 0x118;
    int size2 = 0x80;

    void* a1 = malloc(size1);
    void* a2 = malloc(size1);
    void* a3 = malloc(size1);
    void* a4 = malloc(size1);
    void* a5 = malloc(size1);
    void* a6 = malloc(size1);
    void* a7 = malloc(size1);
    void* a8 = malloc(size1);
    void* az = malloc(size1);

    void* aq = malloc(size2);
    void* aw = malloc(size2);
    void* ae = malloc(size2);
    void* ar = malloc(size2);
    void* at = malloc(size2);
    void* ay = malloc(size2);
    void* au = malloc(size2);
    void* ai = malloc(size2);
    void* ao = malloc(size2);

    free(a1);
    free(a2);
    free(a3);
    free(a4);
    free(a5);
    free(a6);
    free(a7);
    free(a8);

    free(aq);
    free(aw);
    free(ae);
    free(ar);
    free(at);
    free(ay);
    free(au);
    free(ai);

    __asm__("int3");
    void* aa = malloc(size1);
    void* as = malloc(size1);
    void* ad = malloc(size1);
    void* af = malloc(size1);
    void* ag = malloc(size1);
    void* aj = malloc(size1);
    void* ak = malloc(size1);

    void* bq = malloc(size2);
    void* bw = malloc(size2);
    void* be = malloc(size2);
    void* br = malloc(size2);
    void* bt = malloc(size2);
    void* by = malloc(size2);
    void* bu = malloc(size2);
    __asm__("int3");
    void* al = malloc(size1);
    void* bi = malloc(size2);
}
