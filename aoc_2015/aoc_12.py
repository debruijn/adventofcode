from typing import Union
from util.util import ProcessInput, run_day, isnumeric
import json


def get_nums(data, skip='red'):

    if type(data) == int:
        return data
    if type(data) == str:
        return int(data) if isnumeric(data) else 0
    if type(data) == list:
        return sum(get_nums(x, skip=skip) for x in data)
    if skip in data.values():
        return 0
    return sum(get_nums(x, skip=skip) for x in data.values())


def run_all(example_run: Union[int, bool]):

    data = ProcessInput(example_run=example_run, day=12, year=2015).data

    # Part 1: adjusting raw string to be "splittable" and then convert numbers to ints and add them up.
    raw_string = data[0]
    raw_string = (raw_string.replace(',', ' ').replace(':', ' ').replace('[', ' ').replace(']', ' ').replace('{', ' ').
     replace('}', ' ').replace('(', ' ').replace(')', ' '))
    result_part1 = sum(int(x) for x in raw_string.split() if isnumeric(x))
    # Can also get part 1 with `get_nums(actual_data, skip=None)` - see below

    # Part 2: actually loading the json data, and then processing it following the given rules.
    actual_data = json.loads(data[0])
    result_part2 =  get_nums(actual_data)

    extra_out = {'Number of characters in input': len(data[0])}

    return result_part1, result_part2, extra_out


if __name__ == "__main__":
    run_day(run_all, [1, 2, 3, 4, 5, 6, 7, 8])
