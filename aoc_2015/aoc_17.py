from collections import defaultdict
from typing import Union
from util.util import ProcessInput, run_day


def run_all(example_run: Union[int, bool]):

    data = ProcessInput(example_run=example_run, day=17, year=2015).as_int().data

    C = 25 if example_run else 150

    count_combinations = 0
    empty_containers = sorted(data)

    # A DFS (for once it makes more sense than BFS) to go over all possible valid combinations.
    # Key insight: you can assume the containers are already ordered in the way you will have them in the end, so when
    # you create the next queue item, you only have to include the ones after the current one (`this_list[i+1:]` below).
    queue = [(empty_containers, C, 0)]  # Containers to check, Capacity left, Nr of containers included
    n_combinations = defaultdict(int)
    while len(queue) > 0:
        this_list, this_C, this_len = queue.pop()

        if this_C == 0:  # None left to fill: this is a solution.
            count_combinations += 1
            n_combinations[this_len] += 1
            continue

        for i, c in enumerate(this_list):
            remainder = this_C - c
            new_list = [x for x in this_list[i+1:] if x <= remainder]  # Here is the key insight to speed up & avoid double-counting.
            queue.append((new_list, remainder, this_len + 1))

    result_part1 = count_combinations
    result_part2 = n_combinations[min(n_combinations.keys())]

    extra_out = {'Number of containers in input': len(data),
                 'Total distribution of container numbers': n_combinations}

    return result_part1, result_part2, extra_out


if __name__ == "__main__":
    run_day(run_all, [1])
