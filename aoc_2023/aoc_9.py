from typing import Union
from util.util import ProcessInput, run_day

debug = False


def get_next(row):
    if len(set(row)) == 1:
        return row + [row[0]]
    else:
        diff_row = [row[i] - row[i-1] for i in range(1, len(row))]
        diff_row = get_next(diff_row)
        return row + [row[-1] + diff_row[-1]]


def get_prev(row):
    if len(set(row)) == 1:
        return [row[0]] + row
    else:
        diff_row = [row[i] - row[i-1] for i in range(1, len(row))]
        diff_row = get_prev(diff_row)
        return [row[0] - diff_row[0]] + row


def run_all(example_run: Union[int, bool]):

    data = ProcessInput(example_run=example_run, day=9, year=2023).as_list_of_ints().data

    result_part1 = sum([get_next(row)[-1] for row in data])
    result_part2 = sum([get_prev(row)[0] for row in data])

    extra_out = {'Number of rows in input': len(data)}

    return result_part1, result_part2, extra_out


if __name__ == "__main__":
    run_day(run_all, [1])
