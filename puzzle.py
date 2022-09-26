import random

puzzle = []

for n in range(1, 17):
    randomvalue = random.randint(0, 15)
    if n == 1:
        puzzle.append(randomvalue)
    if n > 1:
        if puzzle.count(randomvalue) != 0:
            while puzzle.count(randomvalue) != 0:
                randomvalue = random.randint(0, 15)
        puzzle.append(randomvalue)