from typing import Union
from util.util import ProcessInput, run_day
from itertools import combinations

debug = False


def check_numbers(data, preamble=25):
    for idnum, num in enumerate(data[preamble:]):
        if not any([sum(x) == num for x in combinations(data[idnum:idnum+preamble], 2)]):
            return num, idnum+preamble


def find_contiguous_set(data, idnum):
    num = data[idnum]
    for k in range(2, idnum):
        for inds in range(0, idnum-k):
            nums = data[inds:inds+k]
            if sum(nums) == num:
                return min(nums) + max(nums), inds, k


def run_all(example_run: Union[int, bool]):

    data = ProcessInput(example_run=example_run, day=9).as_int().data

    result_part1, idnum = check_numbers(data, 5 if example_run else 25)
    result_part2, inds, k = find_contiguous_set(data, idnum)

    extra_out = {"Length of XMAS output": len(data),
                 "First number of contiguous set": inds,
                 "Length of continguous set": k}

    return result_part1, result_part2, extra_out


if __name__ == "__main__":
    run_day(run_all, [1])
