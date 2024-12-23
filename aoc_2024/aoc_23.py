from collections import defaultdict
from itertools import combinations
from typing import Union
from util.util import ProcessInput, run_day


def run_all(example_run: Union[int, bool]):

    data = ProcessInput(example_run=example_run, day=23, year=2024).data

    # Process into connections (both directions)
    connections = defaultdict(list)
    for row in data:
        this, that = row.split('-', maxsplit=1)
        connections[this].append(that)
        connections[that].append(this)

    # Find all triple connections by considering for each A-B connection whether an A-C also means B-C (and any 't.')
    triple_connections = set()
    for key in connections.keys():
        for val1, val2 in combinations(connections[key], 2):
            if not any(x.startswith('t') for x in [key, val1, val2]):
                continue
            if val2 in connections[val1]:
                triple_connections.add(tuple(sorted([key, val1, val2])))

    # Repeat the above but for larger groups: keep increasing group size until there is no solution anymore.
    # - Potential improvement: reuse groups of previous size to avoid checking some connections
    current_answer = []
    k=3
    while True:
        large_connections = set()
        for key in connections.keys():
            for vals in combinations(connections[key], k):
                all_in = True
                for val1, val2 in combinations(vals, 2):
                    if val2 not in connections[val1]:
                        all_in = False
                        break
                if all_in:
                    large_connections.add(tuple(sorted([key, *vals])))
        if len(large_connections) == 1:
            current_answer.extend(list(large_connections)[0])
            break
        else:
            print(k+1, list(large_connections)[0])
            k+=1

    # Other setup: a dynamic solution "biggest_set_with_this_subset" that would call itself iteratively for each
    #   possible candidate to extend, and then takes the max. I might make that still, sounds fun.

    result_part1 = len(triple_connections)
    result_part2 = ",".join(sorted(current_answer))

    extra_out = {'Number of rows in input': len(data)}  # TODO: create dict of additional things to have them printed

    return result_part1, result_part2, extra_out


if __name__ == "__main__":
    run_day(run_all, [1])
