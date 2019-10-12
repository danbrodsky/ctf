#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <signal.h>
#include <stdint.h>

#define BUFSIZE 20
#define true 1

struct s1 {
    char *buf;
    uint32_t sz;
};

struct s1 sbuf[BUFSIZE];

void badread(char *b, uint32_t s)
{
    uint32_t sz_ = 0;
    char bb;

    if (s == 0)
        return;

    while (sz_ != s) {
        if (read(0, &bb, 1) != 1) {
            puts("read error");
            exit(-1);
        }

        if (bb == '\n') {
            break;
        }

        b[sz_++] = bb;
    }

    b[sz_] = '\0';
    return;
}

void h_alloc(void)
{
    uint32_t idx = 0;
    for (idx = 0; idx < BUFSIZE; idx += 1) {
        if (!sbuf[idx].buf) {
            break;
        }
    }

    if (idx == BUFSIZE) {
        printf("Buy new book\n");
        return;
    }

    uint32_t sz;
    puts("1. Write on one side?");
    puts("2. Write on both sides?");
    while (true) {
        printf("> ");
        int choice;
        scanf("%d", &choice);
        switch(choice) {
            case 1:
                printf("size: ");
                scanf("%d", &sz);
                if (sz > 0xf0) {
                    printf("too big to fit in a page\n");
                    continue;
                }
                break;
            case 2:
                printf("size: ");
                scanf("%d", &sz);
                if (sz < 0x110) {
                    puts("don't waste pages -_-");
                    continue;
                } else if (sz > 0x1e0) {
                    puts("can you not write that much?");
                    continue;
                }
                break;
            default:
                return;
        }

        break;
    }

    sbuf[idx].buf = malloc(sz);
    if (!sbuf[idx].buf) {
        puts("oh noooooooo!! :(");
        return;
    }

    sbuf[idx].sz = sz;
    printf("page #%d\n", idx);
}

void h_write(void)
{
    uint32_t idx;

    printf("Page: ");
    scanf("%d", &idx);
    printf("Content: ");
    if (idx < BUFSIZE && sbuf[idx].buf) {
        badread(sbuf[idx].buf, sbuf[idx].sz);
    }
}

void h_read(void)
{
    uint32_t idx;

    printf("Page: ");
    scanf("%d", &idx);
    printf("Content: ");
    if (idx < BUFSIZE && sbuf[idx].buf) {
        printf("%s\n", sbuf[idx].buf);
    }
}

void h_free(void)
{
    uint32_t idx;

    printf("Page: ");
    scanf("%d", &idx);
    if (idx < BUFSIZE && sbuf[idx].buf) {
        free(sbuf[idx].buf);
        sbuf[idx].buf = NULL;
    }
}

void pmenu(void)
{
    puts("1. New page in diary");
    puts("2. Talk with ghost");
    puts("3. Listen to ghost");
    puts("4. Burn the page");
    puts("5. Go to sleep");
    printf("> ");
}

void die(int d)
{
    exit(-1);
}

int main ()
{
    setvbuf(stdin, 0, _IONBF, 0);
    setvbuf(stdout, 0, _IONBF, 0);
    setvbuf(stderr, 0, _IONBF, 0);
    alarm(60);
    signal(SIGALRM, die);

    printf("-=-=-=[[Ghost Diary]]=-=-=-\n");
    while (true) {
        pmenu();
        uint32_t choice;
        scanf("%d", &choice);
        while (getchar() != '\n');
        switch (choice) {
            case 1:
                h_alloc();
                break;
            case 2:
                h_write();
                break;
            case 3:
                h_read();
                break;
            case 4:
                h_free();
                break;
            case 5:
                puts("bye human!");
                return 0;
            default:
                printf("Invalid choice\n");
                break;
        }
    }
}
