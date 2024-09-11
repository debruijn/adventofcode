from collections import defaultdict
from itertools import permutations
from typing import Union
from util.util import ProcessInput, run_day


def get_happiness(happy_mapping):
    # Numbers are low enough that we can just loop over all options
    most_happiness = 0  # Assumes there is a positive schedule possible
    for order in permutations(happy_mapping['A'].keys()):
        this_happiness = 0
        curr = 'A'  # Can assume to start at A without "loss of generalization"
        for nxt in order + ('A',):
            this_happiness += happy_mapping[curr][nxt] + happy_mapping[nxt][curr]
            curr = nxt
        most_happiness = this_happiness if this_happiness > most_happiness else most_happiness
    return most_happiness


def run_all(example_run: Union[int, bool]):

    data = ProcessInput(example_run=example_run, day=13, year=2015).data

    # Processing for part 1: dict of dict of happiness values: from -> to would be happy_mapping[from][to]
    happy_mapping = defaultdict(dict)
    for row in data:
        happy_mapping[row[0]][row.split()[-1][0]] = int(row.split()[3]) if int(row.split()[2] == 'gain') else -int(row.split()[3])

    # Part 1
    result_part1 = get_happiness(happy_mapping)

    # Processing for part 2: add 'me' in using 'I'.
    for k in happy_mapping.keys():
        happy_mapping[k]['I'] = 0
    happy_mapping['I'] = {k: 0 for k in happy_mapping.keys()}

    # Part 2
    result_part2 = get_happiness(happy_mapping)

    extra_out = {'Number of instructions in input': len(data),
                 'Number of people seated (in part 2)': len(happy_mapping)}

    return result_part1, result_part2, extra_out


if __name__ == "__main__":
    run_day(run_all, [1])
