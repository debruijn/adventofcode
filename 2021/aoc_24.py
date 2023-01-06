# Note: in the end finished this on paper
# Still included my code setup that I was planning down below, totally unfinished


import numpy as np

with open('aoc_24_data') as f:
    data_raw = f.readlines()


def add(a, b):
    return a + b


def mul(a, b):
    return a * b


def div(a, b):
    return a // b


def mod(a, b):
    return a % b


def eql(a, b):
    return 1 if a == b else 0


def inp(state):
    state.append
    return


def process_tasks(string_input):
    # Convert tasks to functions that need to be called
    f = []
    for s in string_input():
        if s.startswith('add'):
            f.append(add)
        elif s.startswith('mul'):
            f.append(mul)
        elif s.startswith('div'):
            f.append(div)
        elif s.startswith('mod'):
            f.append(mod)
        elif s.startswith('eql'):
            f.append(eql)
        elif s.startswith('inp'):
            f.append(inp)


def check_model_nr(model_number):
    state = {'x': 0, 'y': 0, 'z': 0}

    # Splits long model number into digits
    # Applies them in context of tasks
    # Checks that z=0 and return True, outcome of x,y,z


number = 99999999999999
check = False
while not check:
    # Add check for number not having 0s
    check = check_model_nr(number)
    if not check:
        number -= 1

print(number)
