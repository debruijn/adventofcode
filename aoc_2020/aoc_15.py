from typing import Union
from util.util import ProcessInput, run_day
from collections import defaultdict

debug = False


def func_game_opt(data, num_iter):

    result = []
    for row in data:

        N_low = num_iter
        low_num_map = [-1] * N_low
        for i, num in enumerate(row):
            low_num_map[num] = i+1
        num_map = {}
        num = row[-1]

        if N_low < num_iter:
            for i in range(len(row), num_iter):
                if num < N_low:
                    low_num_map[num], num = i, i - low_num_map[num] if low_num_map[num] >= 0 else 0
                else:
                    num_map[num], num = i, i - num_map.get(num, i)  # Use default argument of get in case num is not in num_map
        else:
            for i in range(len(row), num_iter):
                low_num_map[num], num = i, i - low_num_map[num] if low_num_map[num] >= 0 else 0

        result.append(num)

    return result


def func_game(data, num_iter):

    result = []
    for row in data:

        num_map = {num: i+1 for i, num in enumerate(row)}
        num = row[-1]

        for i in range(len(row), num_iter):
            num_map[num], num = i, i - num_map.get(num, i)  # Use default argument of get in case num is not in num_map

        result.append(num)

    return result


def func_game_old(data, num_iter):

    result = []
    for row in data:
        numbers = defaultdict(lambda: (-1, 0))
        last_num = -1
        for i in range(num_iter):
            if i < len(row):
                numbers[row[i]] = (i, numbers[row[i]][0])
                last_num = row[i]
            else:
                last_num = numbers[last_num][0] - numbers[last_num][1]
                if last_num >= i:
                    numbers[0] = (i, numbers[0][0])
                    last_num = 0
                else:
                    numbers[last_num] = (i, numbers[last_num][0])
            if debug:
                print(f"{i+1}:  {last_num}, {numbers}")
        result.append(last_num)

    return result


def run_all(example_run: Union[int, bool]):

    data = ProcessInput(example_run=example_run, day=15, year=2020).as_list_of_ints(',').data

    result_part1 = func_game_opt(data, 2020)
    result_part2 = func_game_opt(data, 30000000)

    extra_out = {'Number of rows in input': len(data),
                 'Maximum number in input': max([max(row) for row in data])}  # TODO: create dict of additional things to have them printed

    return result_part1, result_part2, extra_out


if __name__ == "__main__":
    run_day(run_all, [1, ])  # [1, 2] but 2 is very slow
