import functools
from typing import Union
from util.util import run_day, get_example_data
from aocd import get_data


debug = False


def run_all(example_run: Union[int, bool]):

    if example_run:
        adj_data = get_example_data(2020, 7, example_run-1)
    else:
        data_raw = get_data(day=7, year=2020)
        adj_data = [x for x in data_raw.split('\n')]

    adj_data = [row.replace(' bags', "").replace(' bag', "").split(' contain ') for row in adj_data]
    adj_data = {row[0]: row[1] for row in adj_data}

    target = ['shiny gold']
    prev_target = ['']
    while target != prev_target:
        prev_target = target.copy()
        target += [x for x in adj_data if x not in target and any(y in adj_data[x] for y in target)]
        if debug:
            print(target)

    dict_data = {key: [x.split(" ", 1) for x in adj_data[key].replace('.', '').split(', ')] for key in adj_data}

    @functools.cache
    def get_counts(key):
        if dict_data[key] == [['no', 'other']]:
            return 1
        else:
            if debug:
                print(f'{key}: {1 + sum([int(x[0]) * (get_counts(x[1])) for x in dict_data[key]])}')
            return 1 + sum([int(x[0]) * (get_counts(x[1])) for x in dict_data[key]])

    result_part1 = len(target) - 1
    result_part2 = get_counts('shiny gold') - 1

    extra_out = {'Number of descriptions': len(adj_data)}
    return result_part1, result_part2, extra_out


if __name__ == "__main__":
    run_day(run_all, [1])
