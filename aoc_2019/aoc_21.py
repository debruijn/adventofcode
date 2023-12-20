from typing import Union
from util.util import ProcessInput, run_day
from aoc_2019.intcode_pc import IntCodePC


debug = False


def run_all(example_run: Union[int, bool]):

    data = ProcessInput(example_run=example_run, day=21, year=2019).as_list_of_ints(',').data[0]

    # Part 1 idea: if there is a gap in A, B or C, and you can land on D, jump.
    txt = ["NOT A J", "NOT B T", "OR T J", "NOT C T", "OR T J", "AND D J", "WALK"]
    input_val = [[ord(x) for x in cmd] + [10] for cmd in txt]
    pc = IntCodePC(data)
    for cmd in input_val:
        pc.add_input(cmd)
    out = pc.run_until_end()
    if debug:
        print(out[1], "\n", "".join([chr(x) for x in out[0] if x < 256]))

    result_part1 = [x for x in out[0] if x >= 256][0]

    # Part 2 idea: if there is a gap in A, B or C, AND you can land on D, AND you can then go to either H or E->I, jump.
    # Also jump anyway if there is a gap at A.
    txt = ["NOT A J", "NOT B T", "OR T J", "NOT C T", "OR T J", "AND D J", "OR D T", "AND E T", "AND I T", "OR H T",
           "AND T J", "NOT A T", "OR T J", "RUN"]
    input_val = [[ord(x) for x in cmd] + [10] for cmd in txt]
    pc = IntCodePC(data)
    for cmd in input_val:
        pc.add_input(cmd)
    out = pc.run_until_end()
    if debug:
        print(out[1], "\n", "".join([chr(x) for x in out[0] if x < 256]))

    result_part2 = [x for x in out[0] if x >= 256][0]

    extra_out = {'Length of program': len(data)}

    return result_part1, result_part2, extra_out


if __name__ == "__main__":
    run_day(run_all, [])
