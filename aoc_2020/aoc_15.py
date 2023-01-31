from typing import Union
from util.util import ProcessInput, run_day
from collections import defaultdict

debug = False


def run_all(example_run: Union[int, bool]):

    data = ProcessInput(example_run=example_run, day=15).as_list_of_ints(',').data

    result_part1 = []
    for row in data:
        numbers = defaultdict(lambda: (-1, 0))
        last_num = -1
        for i in range(2020):
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
        result_part1.append(last_num)
    result_part2 = "TODO"

    extra_out = {'Number of rows in input': len(data)}  # TODO: create dict of additional things to have them printed

    return result_part1, result_part2, extra_out


if __name__ == "__main__":
    run_day(run_all, [1, 2])
