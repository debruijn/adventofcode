import functools
from typing import Union
from util.util import ProcessInput, run_day


@functools.cache
def get_len(num, blinks):
    # Fast implementation: dynamic programming with cache, go from "number and blinks" to "next number(s) and blink-1"
    if blinks==0:
        return 1
    if num == 0:
        return get_len(1, blinks-1)
    str_num = str(num)
    if len(str_num) % 2 == 0:
        num1, num2 = int(str_num[0:(len(str_num)//2)]), int(str_num[(len(str_num)//2):])
        return get_len(num1, blinks-1) + get_len(num2, blinks-1)
    return get_len(num * 2024, blinks-1)


def get_numbers_len(data, blinks):
    # Naive implementation: keep track of full list of numbers at each blink.
    for i in range(blinks):
        ind = 0
        while ind < len(data):
            if data[ind] == 0:
                data[ind] = 1
                ind += 1
                continue
            str_data = str(data[ind])
            if len(str_data) % 2 == 0:
                data[ind], new = int(str_data[0:(len(str_data)//2)]), int(str_data[(len(str_data)//2):])
                data.insert(ind+1, new)
                ind += 2
                continue
            data[ind] *= 2024
            ind += 1

    return len(data)


def run_all(example_run: Union[int, bool]):

    data = ProcessInput(example_run=example_run, day=11, year=2024).as_list_of_ints().data[0]
    run_fast = True

    if run_fast:
        result_part1 = sum(get_len(x, 25) for x in data)  # Faster solution by caching and dynamic programming
    else:
        result_part1 = get_numbers_len(data, 25)  # Solution for part 1 -> naive implementation
    result_part2 = sum(get_len(x, 75) for x in data)

    extra_out = {'Number of numbers in starting arrangement': len(data)}

    return result_part1, result_part2, extra_out


if __name__ == "__main__":
    run_day(run_all, [1, 2])
