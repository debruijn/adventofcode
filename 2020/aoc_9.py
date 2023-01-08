from typing import Union
from util.util import timing
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


@timing
def run_all(example_run: Union[int, bool]):

    file = f'aoc_9_exampledata{example_run}' if example_run else 'aoc_9_data'
    with open(file) as f:
        data = f.readlines()
    adj_data = [int(row.rstrip('\n')) for row in data]

    result_part1, idnum = check_numbers(adj_data, 5 if example_run else 25)
    result_part2, inds, k = find_contiguous_set(adj_data, idnum)

    print(f'\nResults for {f"example" if example_run else "my"} input{f" {example_run}" if example_run else ""}:')
    print(f' Result of part 1: {result_part1}')
    print(f' Result of part 2: {result_part2}')

    print(f'\nDescriptives: \n Length of XMAS output: {len(data)}'
          f'\n First number of contiguous set: {inds}'
          f'\n Length of continguous set: {k} \n')


if __name__ == "__main__":
    [run_all(example_run=i) for i in [1]]
    run_all(example_run=False)
