from typing import Union
from util.util import ProcessInput, run_day


def run_all(example_run: Union[int, bool]):

    data = ProcessInput(example_run=example_run, day=1, year=2017).data[0]

    result_part1 = (sum([int(x) for i, x in enumerate(data[:-1]) if x == data[i + 1]]) +
                    (int(data[-1]) if data[-1] == data[0] else 0))

    skip = len(data) // 2
    result_part2 = (sum([int(x) for i, x in enumerate(data[:-skip]) if x == data[i + skip]]) +
                    sum([int(x) for i, x in enumerate(data[skip:]) if x == data[i]]))

    extra_out = {'Number of digits in input': len(data)}

    return result_part1, result_part2, extra_out


if __name__ == "__main__":
    run_day(run_all, [1, 2, 3, 4])
