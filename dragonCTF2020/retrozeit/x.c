#include "stdio.h"
#include "string.h"

typedef union { unsigned int i; float f; } fu;
unsigned int ___umodsi3 (unsigned int a, unsigned int b);
unsigned int
___umodsi3 (unsigned int a, unsigned int b)
{
  unsigned int d, t, s0, s1, s2, r0, r1;
  fu u0, u1, u2,  u1b, u2b;
  if (b > a)
    return a;
  /* Compute difference in number of bits in S0.  */
  u0.i = 0x40000000;
  u1b.i = u2b.i = u0.i;
  u1.i = a;
  u2.i = b;
  u1.i = a | u0.i;
  t = 0x4b800000 | ((a >> 23) & 0xffff);
  if (a >> 23)
    {
      u1.i = t;
      u1b.i = 0x4b800000;
    }
  u2.i = b | u0.i;
  t = 0x4b800000 | ((b >> 23) & 0xffff);
  if (b >> 23)
    {
      u2.i = t;
      u2b.i = 0x4b800000;
    }
  u1.f = u1.f - u1b.f;
  u2.f = u2.f - u2b.f;
  s1 = u1.i >> 23;
  s2 = u2.i >> 23;
  s0 = s1 - s2;
#define STEP(n) case n: d = b << n; t = a - d; if (t <= a) a = t;
  switch (s0)
    {
    STEP (31)
    STEP (30)
    STEP (29)
    STEP (28)
    STEP (27)
    STEP (26)
    STEP (25)
    STEP (24)
    STEP (23)
    STEP (22)
    STEP (21)
    STEP (20)
    STEP (19)
    STEP (18)
    STEP (17)
    STEP (16)
    STEP (15)
    STEP (14)
    STEP (13)
    STEP (12)
    STEP (11)
    STEP (10)
    STEP (9)
    STEP (8)
    STEP (7)
    STEP (6)
    STEP (5)
    STEP (4)
    STEP (3)
    STEP (2)
    STEP (1)
    STEP (0)
    }
  return a;
}

unsigned int ___mulsi3 (unsigned int a, unsigned int b)
{
  unsigned int r = 0;
  while (a)
    {
      if (a & 1)
        r += b;
      a >>= 1;
      b <<= 1;
    }
  return r;
}

int seed = 1;
int _rand()

{
    int iVar1;

    iVar1 = ___mulsi3(seed,0x41c64e6d);
    seed = iVar1 + 0x3039;
    iVar1 = ___umodsi3(seed,0x7fffffff);
    return iVar1;
}

/* char _end_ch[] = { */
/*          0x8B, 0x84, 0x9A, 0x9B, */
/*          0x9A, 0xB1, 0xD6, 0xAF, */
/*          0x93, 0xB2, 0x81, 0x8C, */
/*          0x84, 0xAB, 0x9D, 0x9C, */
/*          0x8E, 0xB9, 0xB0, 0xD9, */
/*          0xA8, 0xA4, 0x9C, 0x81, */
/*          0x85, 0xA0, 0xA6, 0xB4, */
/*          0x87, 0x9A, 0xBB, 0x92, */
/*          0x96, 0xAD, 0x8C, 0xD7, */
/*          0xB0, 0x8D, 0x97 }; */

/* char _end_ch[] = {164, 140, 180, 146, 150, 129, 176, 214, 133, 175, 151, 129, 132, 157, 147, 156, 156, 166, 142, 154, 140, 160, 139, 155, 132, 177, 176, 141, 154, 135, 217, 185, 215, 171, 168, 178, 154, 173, 187}; */
/* char _end_ch[] = {164, 173, 180, 178, 150, 171, 176, 185, 133, 135, 151, 141, 132, 177, 147, 155, 156, 160, 142, 154, 140, 166, 139, 156, 132, 157, 176, 129, 154, 175, 217, 214, 215, 129, 168, 146, 154, 140, 187}; */
char _end_ch[] = {187, 140, 154, 146, 168, 129, 215, 214, 217, 175, 154, 129, 176, 157, 132, 156, 139, 166, 140, 154, 142, 160, 156, 155, 147, 177, 132, 141, 151, 135, 133, 185, 176, 171, 150, 178, 180, 173, 164};

char _enc_idx[] = { 0x16,  0xC, 0x24, 0x17,
         0x13, 0x19,  0x7,  0x9,
          0xE, 0x23,  0x5,  0x1,
         0x18, 0x21,  0xD, 0x10,
         0x12, 0x1F, 0x1A, 0x1E,
         0x22,  0x0,  0xF,  0xB,
          0x8, 0x15, 0x11,  0x2,
         0x1D, 0x1C, 0x26,  0x3,
          0x4, 0x25, 0x14, 0x20,
          0x6, 0x1B,  0xA,  0x0 };


void _retry_flag__Fv(void)

{
    char bVar1;
    char bVar2;
    int iVar3;
    char bVar4;
    char bVar5;
    int local_a;

    local_a = 0;
    while (local_a < 0x32) {
         iVar3 = _rand();
         bVar4 = ___umodsi3(iVar3,0x27);
         iVar3 = _rand();
         bVar5 = ___umodsi3(iVar3,0x27);
         if (bVar4 != bVar5) {
             // swaps positions of char at idx bVar4 and bVar5
             bVar1 = _enc_idx[bVar4];
             bVar2 = _end_ch[bVar4];
             _enc_idx[bVar4] = _enc_idx[bVar5];
             _end_ch[bVar4] = _end_ch[bVar5];
             _enc_idx[bVar5] = bVar1;
             _end_ch[bVar5] = bVar2;
         }
         local_a = local_a + 1;
    }
    return;

}

unsigned int _check_flag__Fv(void)

{
    unsigned int in_D0 = 0;
    unsigned int uVar1 = 0;
    unsigned int local_e = 0;
    unsigned int local_a = 0;
    char local_5;

    local_5 = _enc_idx[0];
    uVar1 = in_D0 & 0xffffff00;
    if ((_enc_idx[0] & 1) == 0) {
         uVar1 = 0;
         local_a = 2;
         while (local_a < 0x27) {
                      // no char[i-2] < byte[i]
             if (local_5 <= _enc_idx[local_a]) {
                  return local_a & 0xffffff00;
             }
             local_5 = _enc_idx[local_a];
             uVar1 = local_a & 0xffffff00;
                      // every even char's lowest bit must be 0
             if ((local_5 & 1) != 0) {
                  return uVar1;
             }
             local_a = local_a + 2;
         }
         local_5 = _enc_idx[1];
                      // every odd char lowest bit must be 1
         if (((_enc_idx[1] ^ 1) & 1) == 0) {
             local_e = 3;
             while (local_e < 0x27) {
                      // no char[i+2] < byte[i]
                  if (_enc_idx[local_e] <= local_5) {
                      return local_e & 0xffffff00;
                  }
                  local_5 = _enc_idx[local_e];
                  if (((local_5 ^ 1) & 1) != 0) {
                      return local_e & 0xffffff00;
                  }
                  local_e = local_e + 2;
             }
             uVar1 = 1;
         }
    }
    return uVar1;
}


void _decrypt_flag__FPc(char out[40])

{
    int local_6c;
    char abStack104 [40];

    memset(abStack104, 0, sizeof(abStack104));

    local_6c = 0;
    while (local_6c < 0x27) {
         abStack104[local_6c] = ~_end_ch[local_6c] ^ local_6c;
         local_6c = local_6c + 1;
    }
    memcpy(out, abStack104, 39);
    return;
}

int main() {
    /* while( _check_flag__Fv() == 0) { */
    /*     _retry_flag__Fv(); */
    /* } */

    char sol[40];

    _decrypt_flag__FPc(sol);

    sol[39] = '\0';


    printf("%s\n", sol);
}
