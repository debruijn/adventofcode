import functools
from typing import Union
from util import timing


debug = False


@timing
def run_all(example_run: Union[int, bool]):

    file = f'aoc_7_exampledata{example_run}' if example_run else 'aoc_7_data'
    with open(file) as f:
        data = f.readlines()
    adj_data = [row.rstrip('\n').replace(' bags', "").replace(' bag', "").split(' contain ') for row in data]
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
            print(f'{key}: {1 + sum([int(x[0]) * (get_counts(x[1])) for x in dict_data[key]])}')
            return 1 + sum([int(x[0]) * (get_counts(x[1])) for x in dict_data[key]])

    result_part1 = len(target) - 1
    result_part2 = get_counts('shiny gold') - 1

    print(f'\nResults for {f"example" if example_run else "my"} input{f" {example_run}" if example_run else ""}:')
    print(f' Result of part 1: {result_part1}')
    print(f' Result of part 2: {result_part2}')

    print(f'\nDescriptives: \n Number of descriptions: {len(data)} \n')


if __name__ == "__main__":
    [run_all(example_run=i) for i in [1]]
    run_all(example_run=False)
