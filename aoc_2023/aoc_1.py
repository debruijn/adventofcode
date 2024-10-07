from functools import partial
from typing import Union
import re
from util.util import ProcessInput, run_day

debug = False


def regex_dig(x):
    this = re.findall(r'(\d)', x)
    if this is None:
        return 0
    return int(this[0] + this[-1])


def regex_dig_text(x):
    replace_dict = {'one': '1', 'two': '2', 'three': '3', 'four': '4', 'five': '5', 'six': '6', 'seven': '7',
                    'eight': '8', 'nine': '9', 'zero': '0'}
    textnums = "|".join(replace_dict.keys())
    this = re.findall(f'.*?(?=({textnums}|\d)).*?', x)
    if this is None:
        return 0
    return int((this[0] if this[0].isnumeric() else replace_dict[this[0]]) +
               (this[1] if this[1].isnumeric() else replace_dict[this[1]]))


def do_with_regex(data):
    result_part1 = sum(regex_dig(x) for x in data)
    result_part2 = sum(regex_dig_text(x) for x in data)
    return result_part1, result_part2

def do_without_regex(data):

    result_part1 = sum([int([y for y in x if y.isnumeric()][0] + [y for y in x if y.isnumeric()][-1]) for x in data])

    replace_dict = {'one': '1', 'two': '2', 'three': '3', 'four': '4', 'five': '5', 'six': '6', 'seven': '7',
                    'eight': '8', 'nine': '9', 'zero': '0'}

    calibration_values = []
    for row in data:
        first = None
        for index in range(len(row)):
            if first:
                break
            if row[index].isnumeric():
                first = row[index]
                break
            else:
                for num, val in replace_dict.items():
                    if row[index:].startswith(num):
                        first = val
                        break

        last = None
        for index in range(len(row)):
            this_index = len(row) - index - 1
            if last:
                break
            if row[this_index].isnumeric():
                last = row[this_index]
                break
            else:
                for num, val in replace_dict.items():
                    if row[:this_index+1].endswith(num):
                        last = val
                        break

        calibration_values.append(first + last)

    result_part2 = sum([int(x) for x in calibration_values])

    return result_part1, result_part2


def run_all(example_run: Union[int, bool], use_regex=False):

    data = ProcessInput(example_run=example_run, day=1, year=2023).data

    if use_regex:
        result_part1, result_part2 = do_with_regex(data)
    else:
        result_part1, result_part2 = do_without_regex(data)

    extra_out = {'Number of calibration values': len(data)}

    return result_part1, result_part2, extra_out


if __name__ == "__main__":
    run_day(partial(run_all, use_regex=False), [1])
    run_day(partial(run_all, use_regex=True), [1])
