from typing import Union
from util.util import ProcessInput, run_day

debug = False


def run_all(example_run: Union[int, bool]):

    data = ProcessInput(example_run=example_run, day=3, year=2023).data

    # Numbers have start and end -> find them
    # Loop around those indices to see if there is a symbol
    numbers = []
    for i, row in enumerate(data):
        curr_num = ""
        curr_j = False
        for j, num in enumerate(row):
            if num.isnumeric():
                curr_num += num
                if curr_j is False:
                    curr_j = j
            elif curr_j is not False:
                numbers.append((int(curr_num), i, curr_j, len(curr_num)))
                curr_num = ""
                curr_j = False
        if curr_j is not False:
            numbers.append((int(curr_num), i, curr_j, len(curr_num)))

    part_number_sum = 0
    for num in numbers:
        check = False
        for i in range(max(num[1]-1, 0), min(num[1]+2, len(data))):
            for j in range(max(num[2]-1, 0), min(num[2]+num[3]+1, len(data[i]))):
                if not data[i][j].isnumeric() and not data[i][j] == '.':
                    check = True
        if check:
            part_number_sum += num[0]

    result_part1 = part_number_sum

    gear_ratio_sum = 0
    count_gears = 0
    count_valid_gears = 0
    # Find gear, then find how many numbers are adjacent
    for i, row in enumerate(data):
        for j, val in enumerate(row):
            if val == "*":
                count_adj_nums = 0
                nums = 1
                count_gears += 1
                for num in numbers:
                    if i in range(num[1]-1, num[1]+2) and j in range(num[2]-1, num[2]+num[3]+1):
                        count_adj_nums += 1
                        nums *= num[0]
                if count_adj_nums == 2:
                    gear_ratio_sum += nums
                    count_valid_gears += 1

    result_part2 = gear_ratio_sum

    extra_out = {'Number of rows in input': len(data),
                 'Number of numbers in data:': len(numbers),
                 'Number of gears': count_gears,
                 'Number of gears with two neighbours': count_valid_gears}

    return result_part1, result_part2, extra_out


if __name__ == "__main__":
    run_day(run_all, [1, 2])
