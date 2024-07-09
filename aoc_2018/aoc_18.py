from math import prod
from typing import Union
from util.util import ProcessInput, run_day
from itertools import product


def count_adjacent(i, j, data, char):
    return sum(data[x][y] == char for x, y in product(range(i-1, i+2), range(j-1, j+2))
               if not (x == i and y == j) and 0 <= x < len(data) and 0 <= y < len(data[0]))


def run_all(example_run: Union[int, bool]):

    data = ProcessInput(example_run=example_run, day=18, year=2018).data

    target_minutes = 1000000000
    resource_value = -1
    resource_at_t10 = -1
    resource_at_t1b = -1
    nr_wooded, nr_lumber = 0, 0
    history = []
    while resource_value != 0:
        old_data = data.copy()  # might need to build this in loop
        nr_lumber = 0
        nr_wooded = 0
        for i, row in enumerate(data):
            for j, char in enumerate(row):
                if char == '.':
                    if count_adjacent(i, j, old_data, '|') >= 3:
                        data[i] = data[i][:j] + '|' + data[i][j+1:]
                elif char == '|':
                    if count_adjacent(i, j, old_data, '#') >= 3:
                        data[i] = data[i][:j] + '#' + data[i][j+1:]
                else:
                    if count_adjacent(i, j, old_data, '|') == 0 or count_adjacent(i, j, old_data, '#') == 0:
                        data[i] = data[i][:j] + '.' + data[i][j+1:]
                if data[i][j] == '|':
                    nr_wooded += 1
                if data[i][j] == '#':
                    nr_lumber += 1
        resource_value = nr_wooded * nr_lumber

        if history.count((nr_wooded, nr_lumber)) >= 2:
            find_all = [i for i, x in enumerate(history) if x == (nr_wooded, nr_lumber)]
            most_recent_2 = find_all[-2:]
            if history[most_recent_2[0]:most_recent_2[1]] == history[most_recent_2[1]:]:
                loc_in_cycle = (target_minutes - 1 - most_recent_2[1]) % (most_recent_2[1] - most_recent_2[0])
                resource_at_t1b = history[most_recent_2[0] + loc_in_cycle]
                break

        history.append((nr_wooded, nr_lumber))
        if len(history) == 10:
            resource_at_t10 = resource_value

    result_part1 = resource_at_t10
    result_part2 = prod(resource_at_t1b) if not example_run else 0

    extra_out = {'Dimensions of field': (len(data), len(data[0])),
                 'Number wooded/lumber at convergence': f'{nr_wooded}/{nr_lumber}'}

    return result_part1, result_part2, extra_out


if __name__ == "__main__":
    run_day(run_all, [1])
