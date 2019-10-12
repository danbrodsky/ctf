// int calc(unsigned int edi) {
//     unsigned int val_24 = edi;
//     if (val_24 > 0x4){
//         unsigned int eax = val_24;
//         eax--;
//         edi = eax;
//         eax = calc(edi); //recurse on edi -1
//         unsigned int ebx = eax;
//         eax = val_24;
//         eax -= 2;
//         edi = eax;
//         eax = calc(edi); // recurse on edi -2
//         ebx -= eax; // calc(edi-1) - calc(edi-2)
//         eax = val_24;
//         eax -= 3;
//         edi = eax;
//         eax = calc(edi); // recurse on edi -3
//         unsigned int r12d = eax; // stored calc(edi-3)
//         eax = val_24;
//         eax -= 4;
//         edi = eax;
//         eax = calc(edi); // recurse on edi -4
//         r12d -= eax; // calc(edi-3) - calc(edi-4)
//         eax = r12d;
//         ebx += eax; // ((calc(edi-1) - calc(edi-2)) + (calc(edi-3) - calc(edi-4)))
//         eax = val_24;
//         eax -= 5;
//         edi = eax;
//         eax = calc(edi);
//         eax *= 0x1234; // 0x1234*calc(edi-5)
//         eax += ebx; // 0x1234*calc(edi-5) + ((calc(edi-1) - calc(edi-2)) + (calc(edi-3) - calc(edi-4)))
//         unsigned int val_14 = eax;
//         eax = val_14;
//         return eax;
//     } else {
//         unsigned int eax = val_24;
//         eax *= val_24;
//         eax += 0x2345;
//         unsigned int val_14 = eax;
//         eax = val_14;
//         return eax;
//         // not greater than 4, multiply acc so far by itself
//         // add 0x2345 to it
//         // return
//     }
// }
// 
// unsigned int edi = 0x19965;
// calc(edi);
#include <stdio.h>

unsigned int sol[104810];
int main() {
sol[0] = 9029;
sol[1] = 9030;
sol[2] = 9033;
sol[3] = 9038;
sol[4] = 9045;
for (unsigned int i = 5; i <= 104805; ++i) {
    sol[i] = 4660*sol[i-5] + ((sol[i-1] - sol[i-2]) + (sol[i-3] - sol[i-4]));
}

printf("%x\n", (unsigned int)sol[104805]);
}
