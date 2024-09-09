from collections import defaultdict
from itertools import permutations
from typing import Union
from util.util import ProcessInput, run_day


def run_all(example_run: Union[int, bool]):

    data = ProcessInput(example_run=example_run, day=9, year=2015).data

    # Process input to get (symmetric) distances from one location to another
    distances = defaultdict(dict)
    for row in data:
        loc_from, loc_to, dist = row.split()[0:6:2]
        distances[loc_from][loc_to] = int(dist)
        distances[loc_to][loc_from] = int(dist)

    # Utility variables
    mapping = {k: v for k, v in enumerate(distances.keys())}
    shortest_dist = max(max(x.values()) for x in distances.values()) * len(mapping)
    longest_dist = 0

    # Go over all potential permutations of the order
    for order in permutations([x for x in range(len(mapping))]):
        this_dist = 0
        curr = order[0]
        for nxt in order[1:]:
            this_dist += distances[mapping[curr]][mapping[nxt]]
            curr = nxt
        shortest_dist = this_dist if this_dist < shortest_dist else shortest_dist
        longest_dist = this_dist if this_dist > longest_dist else longest_dist

    result_part1 = shortest_dist
    result_part2 = longest_dist

    extra_out = {'Number of locations in input': len(mapping)}

    return result_part1, result_part2, extra_out


if __name__ == "__main__":
    run_day(run_all, [1])
