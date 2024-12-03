from typing import Union
from util.util import ProcessInput, run_day
import re


def run_all(example_run: Union[int, bool]):
    # Read input and turn into one long string
    data = ProcessInput(example_run=example_run, day=3, year=2024).data
    data = "".join(data)

    # Part 1; only apply to actual data or example 1. Use Regex to find all matches with 1-3 times a number, twice.
    if not example_run or example_run == 1:
        total_sum = 0
        for i_match in re.findall(r'mul\([0-9]{1,3},[0-9]{1,3}\)', data):
            nums = i_match.replace('mul(', '').replace(')', '').split(',')
            total_sum += int(nums[0]) * int(nums[1])
        result_part1 = total_sum
    else:
        result_part1 = "N/A"

    # Part 2; only apply to actual data or example 2. Find next do or don't, and apply part 1 approach on substring.
    if not example_run or example_run == 2:
        enabled, ind, total_sum = True, 0, 0  # Is do() last; current index in full string; current sum of mul()'s
        while ind != -1:  # If str.find(sub) can't find anything, it returns -1; so then we stop.
            if enabled:
                new_ind = data.find('don\'t()', ind)
                for i_match in re.findall(r'mul\([0-9]{1,3},[0-9]{1,3}\)', data[ind:new_ind]):
                    nums = i_match.replace('mul(', '').replace(')', '').split(',')
                    total_sum += int(nums[0]) * int(nums[1])
                enabled = False
                ind = new_ind
            else:
                ind = data.find('do()', ind)
                enabled = True
        result_part2 = total_sum
    else:
        result_part2 = "N/A"

    extra_out = {'Number of characters in input': len(data)}

    return result_part1, result_part2, extra_out


if __name__ == "__main__":
    run_day(run_all, [1, 2])
