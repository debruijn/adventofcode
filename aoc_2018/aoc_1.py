from typing import Union
from util.util import ProcessInput, run_day
from aoc_rust import get_frequency_shifts_raw_input


use_rust = True


def run_all(example_run: Union[int, bool]):

    data = ProcessInput(example_run=example_run, day=1, year=2018).data
    if len(data) > 1:
        data = [", ".join(data)]
    data_bu = data[0]
    data = [int(x) for x in data[0].replace('+', '').split(', ')]

    # Part 1
    result_part1 = sum(data)

    # Part 2
    # This is the ugly but quick-to-write approach
    # Nicer would be a yield function that automatically reloops
    if not use_rust:
        curr_freq, curr_ind = 0, 0
        dict_of_freqs = {curr_freq}
        while True:
            curr_freq += data[curr_ind]
            curr_ind = curr_ind + 1 if curr_ind < len(data) - 1 else 0
            if curr_freq in dict_of_freqs:
                break
            else:
                dict_of_freqs.add(curr_freq)
    else:
        # curr_freq = get_frequency_shifts(data)  # Slower implementation due to copying over of variables
        curr_freq = get_frequency_shifts_raw_input(data_bu.replace('+', ''))

    result_part2 = curr_freq

    extra_out = {'Number of frequency shifts to process': len(data)}

    return result_part1, result_part2, extra_out


if __name__ == "__main__":
    run_day(run_all, [1])
