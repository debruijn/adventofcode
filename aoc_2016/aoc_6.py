from typing import Union
from util.util import ProcessInput, run_day
from collections import Counter


def run_all(example_run: Union[int, bool]):

    data = ProcessInput(example_run=example_run, day=6, year=2016).data

    len_message = len(data[0])
    message = ""
    actual_message = ""
    for i in range(len_message):
        this_counter = Counter([row[i] for row in data])
        message += this_counter.most_common(1)[0][0]
        actual_message += this_counter.most_common()[-1][0]

    result_part1 = message
    result_part2 = actual_message

    extra_out = {'Number of corrupted messages': len(data),
                 'Length of message': len_message}

    return result_part1, result_part2, extra_out


if __name__ == "__main__":
    run_day(run_all, [1])
