from typing import Union
from util.util import ProcessInput, run_day


def run_all(example_run: Union[int, bool]):

    data = ProcessInput(example_run=example_run, day=1, year=2018).data
    if len(data) > 1:
        data = [", ".join(data)]

    data = [int(x) for x in data[0].replace('+', '').split(', ')]

    # Part 1
    result_part1 = sum(data)

    # Part 2
    # This is the ugly but quick-to-write approach
    # Nicer would be a yield function that automatically reloops
    stop = False
    curr_freq = 0
    curr_ind = 0
    dict_of_freqs = {curr_freq}
    nr_iter = 0
    while not stop:
        curr_freq += data[curr_ind]
        if curr_ind + 1 < len(data):
            curr_ind += 1
        else:
            curr_ind = 0
            nr_iter += 1
        if curr_freq in dict_of_freqs:
            stop = True
        else:
            dict_of_freqs.add(curr_freq)

    result_part2 = curr_freq

    extra_out = {'Number of frequency shifts to process': len(data),
                 'Number of iterations through the process for part 2': nr_iter}

    return result_part1, result_part2, extra_out


if __name__ == "__main__":
    run_day(run_all, [1])
