from collections import defaultdict, Counter
from typing import Union
from util.util import ProcessInput, run_day


def run_all(example_run: Union[int, bool]):

    data = ProcessInput(example_run=example_run, day=6, year=2015).data

    # I first had a "smart" grid in line with my `intervalues` package, but some of the components were difficult to do
    # in that. It turned out that a naive ('stupid') solution for part 1 was decently fast.
    # In part 2 I assumed that a Counter that goes below 0 will ignore that, but it doesn't. So I have to manually
    # reset.

    stupid_grid = defaultdict(set)
    stupid_grid2 = defaultdict(Counter)

    for row in data:
        # Get nums from the row data
        nums = [x for x in row.split() if ',' in x]
        nums = [int(y) for x in nums for y in x.split(',')]

        # Based on starting words, do something different
        for x in range(nums[1], nums[3] + 1):
            if row.startswith('turn on'):
                stupid_grid[x].update(set(range(nums[0], nums[2] + 1)))
                stupid_grid2[x].update(set(range(nums[0], nums[2] + 1)))
            if row.startswith('turn off'):
                [stupid_grid[x].remove(y) for y in range(nums[0], nums[2]+1) if y in stupid_grid[x]]
                [stupid_grid2[x].subtract([y]) for y in range(nums[0], nums[2] + 1) if y in stupid_grid2[x]]
            if row.startswith('toggle'):
                [stupid_grid[x].remove(y) if y in stupid_grid[x] else stupid_grid[x].add(y)
                 for y in range(nums[0], nums[2] + 1)]
                [stupid_grid2[x].update([y, y]) for y in range(nums[0], nums[2] + 1)]

        # Ugly code to clean up the Counter in part 2 of zero or negative values
        for x in stupid_grid2.keys():
            for y in list(stupid_grid2[x].keys()):
                if stupid_grid2[x][y] <= 0:
                    del stupid_grid2[x][y]

    result_part1 = sum(len(x) for x in stupid_grid.values())
    result_part2 = sum(x.total() for x in stupid_grid2.values())

    extra_out = {'Number of instructions in input': len(data)}

    return result_part1, result_part2, extra_out


if __name__ == "__main__":
    run_day(run_all, [1, 2, 3])
