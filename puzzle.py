import random

H=4
W=4
casas = H * W
state = []

def create_random_valid_state():
    for n in range(1, casas+1):
        randomvalue = random.randint(0, casas-1)
        if n == 1:
            state.append(randomvalue)
        if n > 1:
            if state.count(randomvalue) != 0:
                while state.count(randomvalue) != 0:
                    randomvalue = random.randint(0, casas-1)
            state.append(randomvalue)


def show_state(matrix):
    for i in range(casas):
        if i % 4 == 0 and i > 0:
            print("")
        print(str(matrix[i]) + " ", end = "")


create_random_valid_state()
show_state(state)


