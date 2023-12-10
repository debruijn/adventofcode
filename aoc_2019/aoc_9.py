from typing import Union
from util.util import ProcessInput, run_day

debug = False


def num2decimals(num):
    decimals = [int(x) for x in str(num)]
    return [0]*(5-len(decimals)) + decimals

def get_output(data, input_vals, curr_pos):
    output = []
    pos = curr_pos
    rel_base = 0
    data_extra = dict()

    def args_to_nums(args, modes):
        nums = args.copy()
        for i, num in enumerate(nums):
            nums[i] = read_val(num) if modes[i] == 0 else read_val(num + rel_base) if modes[i] == 2 else num
        return nums

    def read_val(loc):
        return data[loc] if loc <= len(data) else data_extra[loc] if loc in data_extra else 0

    def write_val(val, loc, mode=0):
        if mode == 2:
            loc += rel_base

        if loc > len(data):
            data_extra.update({loc: val})
        else:
            data[loc] = val

    while pos >= 0:
        modes_opcode = num2decimals(data[pos])
        opcode = 10 * modes_opcode[-2] + modes_opcode[-1]
        modes = (modes_opcode[2], modes_opcode[1], modes_opcode[0])

        if opcode == 99:
            return output, pos, data_extra
        elif opcode == 1:
            args = args_to_nums(data[pos + 1:pos + 3], modes)
            write_val(args[0] + args[1], data[pos + 3], modes[2])
            pos += 4
        elif opcode == 2:
            args = args_to_nums(data[pos + 1:pos + 3], modes)
            write_val(args[0] * args[1], data[pos + 3], modes[2])
            pos += 4
        elif opcode == 3:
            write_val(input_vals[0], data[pos+1], modes[0])
            input_vals.pop(0)
            pos += 2
        elif opcode == 4:
            args = args_to_nums(data[pos + 1:pos + 2], modes)
            output.append(args[0])
            pos += 2
        elif opcode == 5:
            args = args_to_nums(data[pos + 1:pos + 3], modes)
            if args[0] != 0:
                pos = args[1]
            else:
                pos += 3
        elif opcode == 6:
            args = args_to_nums(data[pos + 1:pos + 3], modes)
            if args[0] == 0:
                pos = args[1]
            else:
                pos += 3
        elif opcode == 7:
            args = args_to_nums(data[pos + 1:pos + 3], modes)
            write_val(1 if args[0] < args[1] else 0, data[pos + 3], modes[2])
            pos += 4
        elif opcode == 8:
            args = args_to_nums(data[pos + 1:pos + 3], modes)
            write_val(1 if args[0] == args[1] else 0, data[pos + 3], modes[2])
            pos += 4
        elif opcode == 9:
            args = args_to_nums(data[pos + 1:pos + 2], modes)
            rel_base += args[0]
            pos += 2
        else:
            raise ValueError(f"Wrong value for current position: {data[pos]} at {pos}")

    return output, pos, data_extra


def run_all(example_run: Union[int, bool]):

    data = ProcessInput(example_run=example_run, day=9, year=2019).as_list_of_ints(pattern=',').data[0]

    output_part1 = get_output(data, [1], 0)
    result_part1 = output_part1[0][0]
    output_part2 = get_output(data, [2], 0)
    result_part2 = output_part2[0][0]

    extra_out = {'Number of values in input': len(data),
                 'Number of elements outside original data size, part 1': len(output_part1[2]),
                 'Maximum size of program, part 1': max(list(output_part1[2].keys()) + [len(data)]),
                 'Number of elements outside original data size, part 2': len(output_part2[2]),
                 'Maximum size of program, part 2': max(list(output_part2[2].keys()) + [len(data)])}

    return result_part1, result_part2, extra_out


if __name__ == "__main__":
    run_day(run_all, [1, 2, 3])
