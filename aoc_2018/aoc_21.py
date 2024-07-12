from typing import Union
from util.util import ProcessInput, run_day, isdigit
import aoc_16

debug = False


def run_all(example_run: Union[int, bool]):

    data = ProcessInput(example_run=example_run, day=21, year=2018).data
    bound_register = int(data[0].split(' ')[-1])
    data = [[int(x) if isdigit(x) else x for x in row.split(' ')] for row in data[1:]]

    instruction_pointer = 0
    register = [0] * 6
    register[0] = 0

    # Understanding the instructions for part 1:
    # - Need to end up at instr 29 with register[5]==1
    # - For that, register[1] needs to be register[0] at instr 28
    # - To run that, we need to run instr 16 (set register[4] to 27)
    # - To run that, register[2] needs to be smaller than 256 (instr 13 -> 14 -> 16)
    # - When running with starting register = [0 0 0 0 0 0], we can see that check first happening
    #   at iteration 1844 and register[1] == 6483199
    # - Basically, register[2] starts at 65536, and is /=256 twice to get to 1 at that point (and 1 < 256)

    # For part 2:
    # - To stop, we need to avoid a loop.
    # - What happens after the above if register[1] != register[0] at instr 28 is that register[2] is instead large
    # - It is replaced by what is register[1] plus 65536 (instr 6)
    # - Register[1] instead is reset to 7902108 and increased by register[2] % 256.
    # - Then it is updated "remainder after /=16777215 -> times 65899 -> remainder after //16777215"
    # - After that, this number goes through the same dance (R2-> R2//256, and R1 as above)
    # - The first time we repeat register[1] when register[2]<256 gives us the previous one as the last one we could use
    #   to avoid the loop.
    # - Running this "hard coded" takes 90 seconds to run.
    # - But you could do this quicker in direct calculations, which I might do later.

    i = 0
    first_time_first_part = False
    hist = []
    while instruction_pointer < len(data):
        register[bound_register] = instruction_pointer
        old_pointer = instruction_pointer
        instruction = data[instruction_pointer]
        register = getattr(aoc_16, instruction[0])(register, instruction)
        instruction_pointer = register[bound_register]
        instruction_pointer += 1
        if old_pointer == 28 and not first_time_first_part:
            if debug:
                print('Answer part 1:', register[1])
            first_time_first_part = register[1]
        if old_pointer == 28:
            if register[1] not in hist:
                hist.append(register[1])
                if debug:
                    print('Match nr', len(hist), 'namely', register[1])
            else:
                if debug:
                    print('Answer part 2:', hist[-1])
                break
        i += 1

    result_part1 = first_time_first_part
    result_part2 = hist[-1]

    extra_out = {'Number of instructions in input': len(data),
                 'Number of solutions': len(hist)}

    return result_part1, result_part2, extra_out


if __name__ == "__main__":
    run_day(run_all, [])
