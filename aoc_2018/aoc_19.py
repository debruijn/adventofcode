from math import prod
from typing import Union
from util.util import ProcessInput, run_day, isdigit
import aoc_16

debug = False


def prime_factors(n):
    i = 2
    factors = []
    while i * i <= n:
        if n % i:
            i += 1
        else:
            n //= i
            factors.append(i)
    if n > 1:
        factors.append(n)
    return factors


def run_all(example_run: Union[int, bool]):

    data = ProcessInput(example_run=example_run, day=19, year=2018).data
    bound_register = int(data[0].split(' ')[-1])
    data = [[int(x) if isdigit(x) else x for x in row.split(' ')] for row in data[1:]]

    # Part 1: just do it
    instruction_pointer = 0
    register = [0] * 6
    while instruction_pointer < len(data):
        register[bound_register] = instruction_pointer
        instruction = data[instruction_pointer]
        register = getattr(aoc_16, instruction[0])(register, instruction)
        instruction_pointer = register[bound_register]
        instruction_pointer += 1
    result_part1 = register[0]

    # Part 2: first, just do it naively
    instruction_pointer = 0
    register = [0] * 6
    register[0] = 1
    stop = False
    answer = "TODO"
    while instruction_pointer < len(data) and not stop:
        register[bound_register] = instruction_pointer
        instruction = data[instruction_pointer]
        register = getattr(aoc_16, instruction[0])(register, instruction)
        instruction_pointer = register[bound_register]
        instruction_pointer += 1

        if debug:  # Running it in full would take ages (literally?). Reverse-engineer patterns in the printed debug!
            print(instruction_pointer, register)

        if register[4] > 10550400:  # Namely, reg[4] resets after getting bigger than this stored 10550400
            # It does that based on factors, so is it looping after all factors, and adding them together? (Answer: Yes)
            # Note that 1 is also a factor, so is added on.
            factors = prime_factors(register[4])
            answer = 1 + sum(factors) + prod(factors)  # This can also just be "sum(factors)" if factors includes 1 & N
            stop = True
            # Note that this can be wrong in case your number might have more than 2 factors (outside 1 and N), I don't
            # know how this code generalizes (there are multiple options).

    result_part2 = answer

    extra_out = {'Number of commands in input': len(data),
                 'Prime factors of entry 4 in final register': prime_factors(register[4])}

    return result_part1, result_part2, extra_out


if __name__ == "__main__":
    run_day(run_all, [1])
