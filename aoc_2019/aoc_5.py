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

def get_output(data, input):
    output = -9999

    pos = 0
    nr_tests = 0
    while pos >= 0:
        modes_opcode = num2decimals(data[pos])
        opcode = 10 * modes_opcode[-2] + modes_opcode[-1]
        modes = (modes_opcode[2], modes_opcode[1], modes_opcode[0])

        if opcode == 99:
            return output, nr_tests - 1
        elif opcode == 1:
            args = args_to_nums(data[pos + 1:pos + 3], data, modes)
            data[data[pos + 3]] = args[0] + args[1]
            pos += 4
        elif opcode == 2:
            args = args_to_nums(data[pos + 1:pos + 3], data, modes)
            data[data[pos + 3]] = args[0] * args[1]
            pos += 4
        elif opcode == 3:
            args = args_to_nums(data[pos + 1:pos + 2], data, modes)
            data[data[pos + 1]] = input
            pos += 2
        elif opcode == 4:
            args = args_to_nums(data[pos + 1:pos + 2], data, modes)
            output = args[0]
            pos += 2
            nr_tests += 1
            if debug:
                print(f'Output {nr_tests}: {output}')
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

    return output, nr_tests - 1


def run_all(example_run: Union[int, bool]):

    data = ProcessInput(example_run=example_run, day=5, year=2019).as_list_of_ints(pattern=',').data

    if debug:
        print(get_output([3, 9, 8, 9, 10, 9, 4, 9, 99, -1, 8], 8))
        print(get_output([3, 9, 8, 9, 10, 9, 4, 9, 99, -1, 8], 7))

        data_test = [3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,
                    1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104,
                    999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99]
        print(get_output(data_test.copy(), 7))
        print(get_output(data_test.copy(), 8))
        print(get_output(data_test.copy(), 9))

    result_part1, nr_tests = get_output(data[0].copy(), 1)
    result_part2, _ = get_output(data[0].copy(), 5)  #  complete_gravity_assist(data)

    extra_out = {'Number of numbers in input': len(data[0]),
                 'Number of tests run in part 1': nr_tests}

    return result_part1, result_part2, extra_out  # <1998926, <1142868


if __name__ == "__main__":
    run_day(run_all, [])
