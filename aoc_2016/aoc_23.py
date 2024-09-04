import math
from typing import Union
from util.util import ProcessInput, run_day, isnumeric


run_fast = True  # True runs a direct calculation, False does the program "naively" which takes about 6 mins on my pc.


def run_instructions(data, register):
    curr_instr = 0

    while 0 <= curr_instr < len(data):
        row = data[curr_instr]
        if row.startswith('cpy'):
            val_from, val_to = row.split()[1], row.split()[2]
            register[val_to] = int(val_from) if isnumeric(val_from) else register[val_from]
        elif row.startswith('inc'):
            register[row.split()[1]] += 1
        elif row.startswith('dec'):
            register[row.split()[1]] -= 1
        elif row.startswith('jnz'):
            check_val = row.split()[1]
            check_val = int(check_val) if isnumeric(check_val) else register[check_val]
            if check_val != 0:
                curr_instr += (int(row.split()[2]) if isnumeric(row.split()[2]) else register[row.split()[2]]) - 1
        elif row.startswith('tgl'):
            tgl_instr = curr_instr + (int(row.split()[1]) if isnumeric(row.split()[1]) else register[row.split()[1]])
            if tgl_instr >= len(data) or tgl_instr < 0:
                pass
            else:
                if data[tgl_instr].startswith('inc'):
                    data[tgl_instr] = 'dec' + data[tgl_instr][3:]
                elif data[tgl_instr].startswith('dec') or data[tgl_instr].startswith('tgl'):
                    data[tgl_instr] = 'inc' + data[tgl_instr][3:]
                elif data[tgl_instr].startswith('jnz'):
                    data[tgl_instr] = 'cpy' + data[tgl_instr][3:]
                elif data[tgl_instr].startswith('cpy'):
                    data[tgl_instr] = 'jnz' + data[tgl_instr][3:]

        curr_instr += 1
    return register


def run_all(example_run: Union[int, bool]):

    data = ProcessInput(example_run=example_run, day=23, year=2016).data

    # Part 1: initialize registry with 7000.
    register = {k: 0 for k in "abcd"}
    register['a'] = 7 if not example_run else 0
    register = run_instructions(data.copy(), register)
    result_part1 = register['a']

    # Part 2: use 12 as input instead of 7. See comments below for how to get to `run_fast` version.
    if not run_fast or example_run:
        register = {k: 0 for k in "abcd"}
        register['a'] = 12 if not example_run else 0
        register = run_instructions(data.copy(), register)
        result_part2 = register['a']
    else:
        result_part2 = math.factorial(12) + int(data[19].split()[1]) * int(data[20].split()[1])

    # Print out the changes that are made by 'tgl'. Those happen relatively early in the execution. Investigate the
    # resulting program -> in my case two "inc"s have become "dec"s.
    # Then the program can be optimized into the run_fast version:

    # First part: look at first half.
    # - a initialized by 12, b by 12-1, c and d get initialized by b and a, and a is set to 0
    # - for the values of c and d, a is increased by 1, in the loop like explained by itself for the Second part below
    #   (I figured this part out first) -> resulting in a=(12-1)*12
    # - then b is decreased by 1 (so 12-2), and then c and d are set to (12-2) and (12-1)*12, and the above is repeated
    # - this continues down, so you get 12! (12x11x10x...x2x1).

    # Second part: look at final 7 lines. As long as c and d are above 0, a is increased by 1. c goes from nr in line 19
    # to 0 once, and each time, d goes from nr in line 20 to 0. So in total, a is increased by nr_19 * nr_20.

    extra_out = {'Number of instructions in input': len(data)}

    return result_part1, result_part2, extra_out


if __name__ == "__main__":
    run_day(run_all, [1])
