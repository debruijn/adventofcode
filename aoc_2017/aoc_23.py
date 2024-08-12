from typing import Union
from util.util import ProcessInput, run_day, isnumeric

debug = False


def run_all(example_run: Union[int, bool]):

    data = ProcessInput(example_run=example_run, day=23, year=2017).data

    # Part 1: naive implementation
    # Note: the answer here could be deduced from input as well like for part 2. It is (X0 - 2) ** 2, with X0 defined
    # as below
    register = {k: 0 for k in "abcdefgh"}
    curr_instr = 0
    n_mul = 0
    while 0 <= curr_instr < len(data):
        row = data[curr_instr].split(' ')
        if row[0].startswith('set'):
            register[row[1]] = int(row[2]) if isnumeric(row[2]) else register[row[2]]
            curr_instr += 1
        elif row[0] == 'sub':
            register[row[1]] -= int(row[2]) if isnumeric(row[2]) else register[row[2]]
            curr_instr += 1
        elif row[0] == 'mul':
            register[row[1]] *= int(row[2]) if isnumeric(row[2]) else register[row[2]]
            curr_instr += 1
            n_mul += 1
        elif row[0] == 'jnz':
            curr_instr += int(row[2]) if (int(row[1]) if isnumeric(row[1]) else register[row[1]]) != 0 else 1
    result_part1 = n_mul

    # Part 2: using debugging and looking at raw instructions, deduce that b and c are set to (with X0=num in 1st line):
    # b = 100000 + X0*100
    # c = b + X7
    # Then, h is increased everytime f==0 in instr 24. f is zero after d reaches b (instrs 21/22/23), after starting at
    # 2 (instr 9), and being increased in a loop (instr 20 to increase, instr 23 to jump back), if in the meantime
    # d * e - b == 0 (e is in another loop, starting at 2, incr by 1, jump instr 19), with b increasing by X30 until it
    # reaches c (instr 26, 27, 28, 30).
    # In other words: count all numbers [b, b+X30, b+2*X30, ..., c] that are divisible by an integer (not itself or 1).

    start = 100000 + 100 * int(data[0].split(' ')[2])
    stop = start - int(data[7].split(' ')[2])  # Negative number -> subtract
    step = -int(data[30].split(' ')[2])  # Negative number -> negate
    if debug:
        print(start, stop, step)  # -> Should print numbers that you can see using print statements in a naive run

    count_divisible = 0
    for x in range(start, stop+1, step):
        for i in range(2, x):
            if x % i == 0:
                count_divisible += 1
                break

    result_part2 = count_divisible

    extra_out = {'Number of instructions in input': len(data),
                 'Loop specifics': f"From {start} to {stop} with stepsize {step}"}

    return result_part1, result_part2, extra_out


if __name__ == "__main__":
    run_day(run_all, [])
