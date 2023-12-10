from typing import Union
from util.util import ProcessInput, run_day

debug = False


def get_output(data, noun, verb):
    data[1] = noun
    data[2] = verb

    for pos in range(0, len(data), 4):
        if debug:
            print(f"{noun}/{verb}: Pre: {data[pos:pos + 4]};")
        if data[pos] == 99:
            return data[0]
        elif data[pos] == 1:
            data[data[pos + 3]] = data[data[pos + 1]] + data[data[pos + 2]]
        elif data[pos] == 2:
            data[data[pos + 3]] = data[data[pos + 1]] * data[data[pos + 2]]
        else:
            raise ValueError(f"Wrong value for current position: {data[pos]} at {pos}")
        if debug:
            print(f"{noun}/{verb}: Post: {data[pos:pos + 4]}")

    return data[0]


def complete_gravity_assist(data):

    for noun in range(0, min(100, len(data[0]))):
        for verb in range(0, min(100, len(data[0]))):
            if get_output(data[0].copy(), noun, verb) == 19690720:
                return 100 * noun + verb


def run_all(example_run: Union[int, bool]):

    data = ProcessInput(example_run=example_run, day=2, year=2019).as_list_of_ints(pattern=',').data

    result_part1 = get_output(data[0].copy(), 12, 2)
    result_part2 = complete_gravity_assist(data)

    extra_out = {'Number of numbers in input': len(data[0])}

    return result_part1, result_part2, extra_out


if __name__ == "__main__":
    run_day(run_all, [1])
