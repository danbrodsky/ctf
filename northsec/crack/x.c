#include <string.h>
#include <stdlib.h>
#include <stdio.h>


int main() {

    char cStack[0x11];

    memset(&cStack, 0x41, 0x11);

    cStack[0] = (char)cStack[0] + 0x05;
    cStack[1] = (char)cStack[1] + 0x0b;
    cStack[3]= (char)cStack[3] + 0x06;
    cStack[4]= (char)cStack[4] + -0x14;
    cStack[5]=(char) cStack[5] + 0xc;
    cStack[6]=(char) cStack[6] + 0x8;
    cStack[7]=(char) cStack[7] + 0x0f;
    cStack[8]=(char) cStack[8] + 0x12;
    cStack[9]=(char) cStack[9] + 0x28;
    cStack[10]=(char) cStack[10] + 0x32;
    cStack[11]=(char) cStack[11] + 0x06;
    cStack[12]=(char) cStack[12] + 0x11;
    cStack[13]=(char) cStack[13] + 0x04;

    cStack[15]= (char) cStack[15] + 0x13;
    cStack[16]=(char) cStack[16] + -0x20;
    puts(cStack);
    return 0;
}
