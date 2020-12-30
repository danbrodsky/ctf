#include <stdlib.h>
#include <stdio.h>

int main() {
    while(1) {
        char buf[50];
        gets(buf);
        printf(buf);
    }
    return 0;
}
