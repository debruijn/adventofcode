from collections import defaultdict
from typing import Union
from util.util import ProcessInput, run_day

debug = False


def num2decimals(num):
    decimals = [int(x) for x in str(num)]
    return [0]*(5-len(decimals)) + decimals


def get_output(data, input_vals, curr_pos, data_extra=None):
    output = []
    pos = curr_pos
    rel_base = 0
    data_extra = dict() if data_extra is None else data_extra

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
            return output, -1, data, data_extra
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
            return output, pos, data, data_extra
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

    return output, -1, data, data_extra


def run_all(example_run: Union[int, bool]):

    data = ProcessInput(example_run=example_run, day=11, year=2019).as_list_of_ints(pattern=',').data[0]

    field = defaultdict(lambda: 0)
    loc = 0 + 0j
    dir = 0 + 1j
    pos = 0
    data_extra = dict()
    next_out_is_dir = False
    while pos >=0:
        out, pos, data, data_extra = get_output(data, [field[loc]], pos, data_extra)
        if len(out) > 0:
            if next_out_is_dir:
                dir *= -1j if out[0] == 1 else 1j
                loc += dir
                print(loc, pos, field[loc], dir, sum(field.values()), len(field))
            else:
                field[loc] = out[0]
            next_out_is_dir = not next_out_is_dir
        else:
            pos = -1

    result_part1 = len(field)
    result_part2 = sum(field.values())

    extra_out = {'Number of rows in input': len(data)}  # TODO: create dict of additional things to have them printed

    return result_part1, result_part2, extra_out


if __name__ == "__main__":
    run_day(run_all, [])
