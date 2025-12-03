from typing import Union
from util.util import ProcessInput, run_day


def run_for_length(data, len_voltage=2):
    total_joltage = 0
    for row in data:
        nums = []
        curr_ind = -1
        for i in range(len_voltage):
            left = len_voltage - i - 1  # Amount of digits to reserve for next steps
            if left != 0:
                nums += [max(x for x in row[curr_ind + 1:-left])]
            else:
                nums += [max(x for x in row[curr_ind + 1:])]
            curr_ind = row.find(nums[-1], curr_ind + 1)
        this_joltage = int("".join(x for x in nums))
        total_joltage += this_joltage

    return total_joltage

def run_all(example_run: Union[int, bool]):

    data = ProcessInput(example_run=example_run, day=3, year=2025).data

    result_part1 = run_for_length(data, 2)
    result_part2 = run_for_length(data, 12)

    extra_out = {'Number of banks in input': len(data),
                 'Length of a bank': len(data[0])}

    return result_part1, result_part2, extra_out


if __name__ == "__main__":
    run_day(run_all, [1])
