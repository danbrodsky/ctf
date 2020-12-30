#include <unistd.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>

int main(void) {
  char buf[0x20];
  puts("Welcome to Pwn Warmup!");
  scanf("%s", buf);
  fclose(stdout);
  fclose(stderr);
  /* fopen("/dev/tty", "O_WRONLY"); */
  /* puts("test"); */
  /* fopen("flag.txt", "r+"); */
  /* fopen("flag.txt", "r+"); */
  /* fopen("flag.txt", "r+"); */
  /* fopen("flag.txt", "r+"); */
  /* int fd = open("flag.txt", 1); */
  /* sprintf(buf, "%d", fd); */
  /* fopen("flag.txt", "r+"); */
  /* freopen ("flag.txt", "r", stdout); */
  /* register int    syscall_no  asm("rax") = 1; */
  /* register int    arg1        asm("rdi") = 1; */
  /* register char*  arg2        asm("rsi") = "hello, world!\n"; */
  /* register int    arg3        asm("rdx") = 14; */
  /* asm("syscall"); */
  /* open("/dev/stdout", 1); */
  fclose(stdout);
  dup2(0,1);
  write(1, "test", 4);
  /* puts(buf); */
  /* write(1, buf, 32); */
}

__attribute__((constructor))
void setup(void) {
  setvbuf(stdin, NULL, _IONBF, 0);
  setvbuf(stdout, NULL, _IONBF, 0);
  setvbuf(stderr, NULL, _IONBF, 0);
  alarm(60);
}
