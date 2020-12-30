#include <string.h>
#include <stdio.h>

int * j_4(int *flag)

{
  flag[0] = flag[0] ^ 0x44d3e8d9;
  flag[1] = flag[1] ^ 0x47592c79;
  flag[2] = flag[2] ^ 0xeebcd1c8;
  flag[3] = flag[3] ^ 0xf4c4e2f8;
  return flag;
}

int* j_3(int *flag)

{
  flag[0] = flag[0] + 0x426c4e9;
  flag[1] = flag[1] + 0x58918fcd;
  flag[2] = flag[2] + -0x5792e89;
  flag[3] = flag[3] + 0x6d320fed;
  return flag;
}


int* j_2(int *flag)

{
  int flag_copy[4];

  flag_copy[0] = flag[0] + flag[0] % flag[1];
  flag_copy[1] = flag[1] + flag[1] % flag[2];
  flag_copy[2] = flag[2] + flag[2] % flag[3];
  flag_copy[3] = flag[3] + flag[3] % flag[0];
  memcpy(flag, flag_copy,0x10);
  return flag;
}

int* j_1(int *flag)

{
  flag[0] = flag[0] + -0x1113f624;
  flag[1] = flag[1] + 0x3774ed1;
  flag[2] = flag[2] + 0xc443fff;
  flag[3] = flag[3] + -0x605703a9;
  return flag;
}

int* j_0(int *flag)

{
    int flag_copy[4];

    flag_copy[0] = (flag[1] + 1) * flag[0];
    flag_copy[1] = (flag[2] + 1) * flag[1];
    flag_copy[2] = (flag[3] + 1) * flag[2];
    flag_copy[3] = (flag[0] + 1) * flag[3];
    memcpy(flag, flag_copy, 0x10);
    return flag;
}

int main() {

    char flag_in[16];

    fgets(flag_in, 16, stdin);

    int flag[4];

    memcpy(flag, flag_in, 16);

    int i = 0;
    while (i < 4) {
        j_0(flag);
        j_1(flag);
        j_2(flag);
        j_3(flag);
        j_4(flag);
        i += 1;
    }

    if ((((flag[0] == 0x5935f1de) && (flag[1] == -0x49c8da19)) &&
         (flag[2] == -0x205eff97)) && (flag[3] == 0x4e556f64)) {
        printf("CORRECT");
    }

    return 0;
}
