solved_base = """
9 1 2 8 7 3 6 4 5\n
3 8 6 4 5 9 7 1 2\n
5 4 7 1 6 2 8 3 9\n
2 6 8 9 4 5 1 7 3\n
7 3 1 2 8 6 5 9 4\n
4 9 5 3 1 7 2 6 8\n
6 2 4 7 3 8 9 5 1\n
1 5 9 6 2 4 3 8 7\n
8 7 3 5 9 1 4 2 6\n
"""

num_mapping = [
0,
386813690,
2714038447,
3218142131,
3557617843,
3947517376,
134514585,
1073741719,
1073741719,
1073741719
]

for i, v in enumerate(num_mapping):
    if not i:
        continue
    solved_base = solved_base.replace(" %i " % i, " %i " % v)
    solved_base = solved_base.replace(" %i\n" % i, " %i\n" % v)
    solved_base = solved_base.replace("\n%i " % i, "\n%i " % v)

print(solved_base)


