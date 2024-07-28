from typing import Union
from util.util import ProcessInput, run_day


def run_all(example_run: Union[int, bool]):

    data = ProcessInput(example_run=example_run, day=6, year=2017).replace_substrings('\t').data
    mem_bank = [int(x) for x in data[0].split(' ')]

    hist1 = []
    hist2 = []
    while True:
        max_ind = mem_bank.index(max(mem_bank))
        max_val = max(mem_bank)
        mem_bank[max_ind] = 0
        this_ind = (max_ind + 1) % len(mem_bank)
        while max_val > 0:
            mem_bank[this_ind] += 1
            this_ind = (this_ind + 1) % len(mem_bank)
            max_val -= 1
        tuple_mem_bank = tuple(mem_bank)
        if tuple_mem_bank in hist1:
            if tuple_mem_bank not in hist2:
                hist2.append(tuple_mem_bank)
            else:
                break
        else:
            hist1.append(tuple_mem_bank)

    result_part1 = len(hist1) + 1
    result_part2 = len(hist2)

    extra_out = {'Number of elements in memory bank': len(mem_bank)}

    return result_part1, result_part2, extra_out


if __name__ == "__main__":
    run_day(run_all, [1])
