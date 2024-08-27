from typing import Union
from util.util import ProcessInput, run_day, isnumeric


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
                curr_instr += int(row.split()[2]) - 1
        curr_instr += 1
    return register


def run_all(example_run: Union[int, bool]):
    data = ProcessInput(example_run=example_run, day=12, year=2016).data

    # Fortunately, no smart tricks needed.. yet. Both parts can just run doing the instructions "naively". Of course,
    # some speedup can be gained by interpreting the instructions and converting a loop into a single command (e.g.
    # the last 7 lines in my input basically say "increase a by 17*18" which is faster as a single calculation than
    # doing the 2 + 5*17 + 3*17*18 instructions manually) - but again: it's not needed now, and I will probably have to
    # do this later in the year anyway.

    # Alternatively, one could gain a smaller speed increase by interpreting the instructions beforehand, such that the
    # string-splitting etc. needn't happen anymore. You could construct lambda functions and store them under the same
    # index as the instruction. These lambda functions take the registry as input, and then return the registry and the
    # new instruction pointer ("curr_instr") as output.

    # Part 1: initialize registry with 4 zeros.
    register = {k: 0 for k in "abcd"}
    register = run_instructions(data, register)
    result_part1 = register['a']

    # Part 2: overwrite c at the start with 1
    register = {k: 0 for k in "abcd"}
    register['c'] = 1
    register = run_instructions(data, register)
    result_part2 = register['a']

    extra_out = {'Number of instructions in input': len(data),
                 'Final registry in part 2': register}

    return result_part1, result_part2, extra_out


if __name__ == "__main__":
    run_day(run_all, [1])
