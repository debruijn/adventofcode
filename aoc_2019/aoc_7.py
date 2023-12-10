from itertools import permutations
from typing import Union
from util.util import ProcessInput, run_day

debug = False


def num2decimals(num):
    decimals = [int(x) for x in str(num)]
    return [0]*(5-len(decimals)) + decimals


def args_to_nums(args, data, modes):
    nums = args.copy()
    for i, num in enumerate(nums):
        nums[i] = data[num] if modes[i] == 0 else num
    return nums

def get_output(data, input_vals, curr_pos):
    output = None
    pos = curr_pos
    while pos >= 0:
        modes_opcode = num2decimals(data[pos])
        opcode = 10 * modes_opcode[-2] + modes_opcode[-1]
        modes = (modes_opcode[2], modes_opcode[1], modes_opcode[0])

        if opcode == 99:
            return output, pos
        elif opcode == 1:
            args = args_to_nums(data[pos + 1:pos + 3], data, modes)
            data[data[pos + 3]] = args[0] + args[1]
            pos += 4
        elif opcode == 2:
            args = args_to_nums(data[pos + 1:pos + 3], data, modes)
            data[data[pos + 3]] = args[0] * args[1]
            pos += 4
        elif opcode == 3:
            data[data[pos + 1]] = input_vals[0]
            input_vals.pop(0)
            pos += 2
        elif opcode == 4:
            args = args_to_nums(data[pos + 1:pos + 2], data, modes)
            output = args[0]
            pos += 2
            return output, pos
        elif opcode == 5:
            args = args_to_nums(data[pos + 1:pos + 3], data, modes)
            if args[0] != 0:
                pos = args[1]
            else:
                pos += 3
        elif opcode == 6:
            args = args_to_nums(data[pos + 1:pos + 3], data, modes)
            if args[0] == 0:
                pos = args[1]
            else:
                pos += 3
        elif opcode == 7:
            args = args_to_nums(data[pos + 1:pos + 3], data, modes)
            data[data[pos + 3]] = 1 if args[0] < args[1] else 0
            pos += 4
        elif opcode == 8:
            args = args_to_nums(data[pos + 1:pos + 3], data, modes)
            data[data[pos + 3]] = 1 if args[0] == args[1] else 0
            pos += 4
        else:
            raise ValueError(f"Wrong value for current position: {data[pos]} at {pos}")

    return output, pos


def run_all(example_run: Union[int, bool]):

    data = ProcessInput(example_run=example_run, day=7, year=2019).as_list_of_ints(pattern=',').data

    # Part 1
    curr_max = 0
    phases = (0, 1, 2, 3, 4)
    for sequence in permutations(phases, len(phases)):
        curr_val = 0
        for phase_setting in sequence:
            curr_val, _ = get_output(data[0].copy(), [phase_setting, curr_val], 0)
        curr_max = curr_val if curr_val > curr_max else curr_max
    result_part1 = curr_max

    # Part 2
    curr_max = 0
    phases = (5, 6, 7, 8, 9)
    for sequence in permutations(phases, len(phases)):
        inputs = [[sequence[i]] for i in range(len(phases))]
        inputs[0].append(0)
        curr_pos = [0] * len(phases)
        this_out, new_val = (0, 0)
        stop = False
        data_seq = data[0].copy()  # Actually, should have a persistent copy per amplifier; doesn't matter in this case
        while not stop:
            for i, _ in enumerate(sequence):
                new_val, new_pos = get_output(data_seq.copy(), inputs[i], curr_pos[i])
                if new_val is None:
                    stop = True
                    break
                curr_pos[i] = new_pos
                inputs[(i+1) % len(phases)].append(new_val)
            this_out = new_val if not stop else this_out
        curr_max = this_out if this_out > curr_max else curr_max
    result_part2 = curr_max

    extra_out = {'Number of numbers in program': len(data[0])}

    return result_part1, result_part2, extra_out


if __name__ == "__main__":
    run_day(run_all, [])
