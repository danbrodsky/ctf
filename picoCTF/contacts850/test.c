#include <stdio.h>

struct contact {
    char *name;
    char *bio;
};

int main (){
    struct contact a = {};
    printf("%ul", sizeof(a));
}
