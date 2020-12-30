#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>

typedef unsigned int uint;

char* itoa(int val) {
	int length = snprintf( NULL, 0, "%d", val );
	char* str = malloc(length + 1);
	snprintf(str, length + 1, "%d", val);
	return str;
}

char* concat(char* a, char* b) {
	char* c = malloc(strlen(a) + strlen(b) + 1);
	strcpy(c, a);
	strcat(c, b);
	return c;
}

bool checkFlag(char* A_0, int A_1)
	{
		char* text = itoa(2023103744);
        char* string_builder;
		int num = 0;
		int num2 = 0;
		while(true)
		{
			IL_15:
			num2 = 169177363;
			while(true)
			{
				uint num3;
				num3 = (num2 ^ 200344158U);
				printf("%d\n", num3 % 6);
				switch (num3 % 6U)
				{
				case 0U:
					goto IL_15;
				case 1U:
					num2 = (num3 * 1049313381U ^ 1849965166U);
					continue;
				case 2U:
				{
					int num4 = (int)(A_0[num] * '*');
					num2 = 708881281U;
					continue;
				}
				case 3U:
					num2 = ((num < strlen(A_0)) ? 1292729362U : 1878786418U);
					continue;
				case 5U:
				{
					int num4;
					int num5 = ((num4 >> 6) + (num4 >> 5) & 127) ^ (num4 + (int)text[num] & 127) ^ (int)text[strlen(A_0) - num - 1];
					char* num5_ch = itoa(num5);
					string_builder = concat(string_builder, num5_ch);

					num++;
					num2 = (num3 * 506734605U ^ 1767636828U);
					continue;
				}
				}
				goto Block_1;
			}
		}
		Block_1:
		return string_builder;
    }

int main() {

    printf("%d\n", checkFlag("tttttest", 69));

    return 0;
}
