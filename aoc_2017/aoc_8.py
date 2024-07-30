from typing import Union
from util.util import ProcessInput, run_day
from collections import defaultdict
from operator import lt, le, eq, ne, ge, gt

condition_map = {'>': gt, '>=': ge, '<': lt, '<=': le, '==': eq, '!=': ne}


def run_all(example_run: Union[int, bool]):

    data = ProcessInput(example_run=example_run, day=8, year=2017).data

    registry = defaultdict(int)
    max_val = 0
    for row in data:
        operation, condition = row.split(' if ')
        condition = condition.split(' ')
        if condition_map[condition[1]](registry[condition[0]], int(condition[2])):
            operation = operation.split(' ')
            registry[operation[0]] += int(operation[2]) * (1 if operation[1] == 'inc' else -1)
        if max(registry.values()) > max_val:
            max_val = max(registry.values())

    result_part1 = max(registry.values())
    result_part2 = max_val

    extra_out = {'Number of operations in input': len(data),
                 'Number of elements in registry': len(registry)}

    return result_part1, result_part2, extra_out


if __name__ == "__main__":
    run_day(run_all, [1])
