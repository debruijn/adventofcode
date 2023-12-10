from typing import Union
from util.util import ProcessInput, run_day

debug = False


def run_all(example_run: Union[int, bool]):

    data = ProcessInput(example_run=example_run, day=1, year=2023).data

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

    extra_out = {'Number of calibration values': len(data)}

    return result_part1, result_part2, extra_out


if __name__ == "__main__":
    run_day(run_all, [1])
