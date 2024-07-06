from typing import Union
from util.util import ProcessInput, run_day


def addr(input, instruction):
    output = input.copy()
    output[instruction[3]] = output[instruction[1]] + output[instruction[2]]
    return output


def addi(input, instruction):
    output = input.copy()
    output[instruction[3]] = output[instruction[1]] + instruction[2]
    return output


def mulr(input, instruction):
    output = input.copy()
    output[instruction[3]] = output[instruction[1]] * output[instruction[2]]
    return output


def muli(input, instruction):
    output = input.copy()
    output[instruction[3]] = output[instruction[1]] * instruction[2]
    return output


def banr(input, instruction):
    output = input.copy()
    output[instruction[3]] = output[instruction[1]] & output[instruction[2]]
    return output


def bani(input, instruction):
    output = input.copy()
    output[instruction[3]] = output[instruction[1]] & instruction[2]
    return output


def borr(input, instruction):
    output = input.copy()
    output[instruction[3]] = output[instruction[1]] | output[instruction[2]]
    return output


def bori(input, instruction):
    output = input.copy()
    output[instruction[3]] = output[instruction[1]] | instruction[2]
    return output


def setr(input, instruction):
    output = input.copy()
    output[instruction[3]] = output[instruction[1]]
    return output


def seti(input, instruction):
    output = input.copy()
    output[instruction[3]] = instruction[1]
    return output


def gtir(input, instruction):
    output = input.copy()
    output[instruction[3]] = 1 if instruction[1] > output[instruction[2]] else 0
    return output


def gtri(input, instruction):
    output = input.copy()
    output[instruction[3]] = 1 if output[instruction[1]] > instruction[2] else 0
    return output


def gtrr(input, instruction):
    output = input.copy()
    output[instruction[3]] = 1 if output[instruction[1]] > output[instruction[2]] else 0
    return output


def eqir(input, instruction):
    output = input.copy()
    output[instruction[3]] = 1 if instruction[1] == output[instruction[2]] else 0
    return output


def eqri(input, instruction):
    output = input.copy()
    output[instruction[3]] = 1 if output[instruction[1]] == instruction[2] else 0
    return output


def eqrr(input, instruction):
    output = input.copy()
    output[instruction[3]] = 1 if output[instruction[1]] == output[instruction[2]] else 0
    return output


def check(input, instruction, output, func):
    return func(input, instruction) == output


def check_all(input, instruction, output, k=3):
    return sum(check(input, instruction, output, func) for func in list_of_func) >= k


list_of_func = [addr, addi, mulr, muli, banr, bani, borr, bori, setr, seti, gtir, gtri, gtrr, eqir, eqri, eqrr]


def run_all(example_run: Union[int, bool]):

    data = ProcessInput(example_run=example_run, day=16, year=2018).as_list_of_strings_per_block().data

    # Part 1: count how many instructions could be 3 or more operations.
    count_threevalid = 0
    options = {x: list_of_func.copy() for x in range(16)}  # For part 2: construct which instr could be which op

    for case in data if example_run else data[:-3]:
        # Part 1: processing puzzle input
        input, instruction, output = tuple(case)
        input = [int(x) for x in input.replace('Before: [', '').replace(']', '').split(', ')]
        instruction = [int(x) for x in instruction.split(' ')]
        output = [int(x) for x in output.replace('After:  [', '').replace(']', '').split(', ')]

        if check_all(input, instruction, output):
            count_threevalid += 1  # Part 1 answer

        # For part 2: remove failed operation as option for instruction number
        if not example_run:
            curr_func = options[instruction[0]].copy()
            for func in curr_func:
                if not check(input, instruction, output, func):
                    options[instruction[0]].remove(func)

    registry = [0, 0, 0, 0]
    if not example_run:

        mapped_operation = [lambda x, y: x] * 16  # Placeholder function

        # Part 2: process remaining options: if len(options[a]) = 1, then remove that one from all other values.
        # Iterate until all instructions/operations uniquely mapped.
        while len(options) > 0:
            unique_mapping = {x: v[0] for x, v in options.items() if len(v) == 1}
            for x, v in options.items():
                [options[x].remove(y) for y in unique_mapping.values() if y in options[x]]
            for x, v in unique_mapping.items():
                mapped_operation[x] = v
                del options[x]

        # Part 2: apply mapped operations to update instruction.
        for instruction in data[-1]:
            instruction = [int(x) for x in instruction.split(' ')]
            registry = mapped_operation[instruction[0]](registry, instruction)

    result_part1 = count_threevalid
    result_part2 = registry[0]

    extra_out = {'Number of cases to test': len(data if example_run else data[:-3]),
                 'Number of instructions to apply in phase 2': len(data[-1]) if not example_run else 0}

    return result_part1, result_part2, extra_out


if __name__ == "__main__":
    run_day(run_all, [1])
