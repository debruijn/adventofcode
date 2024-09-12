from random import shuffle
from typing import Union
from util.util import ProcessInput, run_day


def run_all(example_run: Union[int, bool]):

    data = ProcessInput(example_run=example_run, day=19, year=2015).data

    # Processing input
    mapping = [[x for x in tuple(row.split(' => '))] for row in data[:-2]]
    curr = data[-1]

    # Part 1: apply mapping L -> R
    new = set()
    for k, v in mapping:
        lk = len(k)
        new.update(set([curr[:i] + v + curr[i + lk:] for i in range(len(curr)) if curr[i:i+lk] == k]))

    result_part1 = len(new)

    # Part 2: apply mapping R -> L. There are way too many options though, so just try stuff until it works. If it
    # doesn't work, try again with a different permutation of the mapping variable.
    # I have also tried: BFS (got stuck, way too slow), greedy DFS (greedy option results in a non-replaceable string at
    # some point, I have not tried going back one step in that case although some people had success with that).
    target = 'e'
    curr = data[-1]
    stop = False
    count = 0
    while not stop:
        if any([x[1] in curr for x in mapping]):
            for x in mapping:  # just apply random mapping, if it's possible, until you get stuck or get at 'e'
                if x[1] not in curr:
                    continue
                curr = curr.replace(x[1], x[0], 1)
                count += 1
                if curr == target:
                    stop = True
        else:
            count = 0
            shuffle(mapping)
            curr = data[-1]

    result_part2 = count

    extra_out = {'Number of translations in input': len(data[:-2])}

    return result_part1, result_part2, extra_out


if __name__ == "__main__":
    run_day(run_all, [])
