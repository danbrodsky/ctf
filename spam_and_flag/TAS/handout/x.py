import random

choices = []
for i in range(32):
    choices.append(bin(i)[2:].rjust(5, "0") + "\n")


with open("replay.txt", "a") as f:
    for i in range(10000):
        c = random.randrange(0, 31)
        f.write(choices[c])
