from typing import Union
from util.util import ProcessInput, run_day

debug = False


def check_val_rules(val, rules):
    for rule in rules:
        if any([subrule[0] <= val <= subrule[1] for subrule in rule]):
            return True
    return False


def run_all(example_run: Union[int, bool]):

    data = ProcessInput(example_run=example_run, day=16).as_list_of_strings_per_block().data
    rules = [[[int(y) for y in x.split('-')]
              for x in (row.split(' ')[-3], row.split(' ')[-1])]
             for row in data[0]]

    nearby_tickets = [[int(x) for x in row.split(',')] for row in data[2][1:]]

    error_rate = 0
    for ticket in nearby_tickets:
        for val in ticket:
            error_rate += val if not check_val_rules(val, rules) else 0

    result_part1 = error_rate
    result_part2 = "TODO"

    extra_out = {'Number of blocks in input': len(data),
                 'Number of rules': len(data[0]),
                 'Number of nearby tickets': len(data[2])}  # TODO: create dict of additional things to have them printed

    return result_part1, result_part2, extra_out


if __name__ == "__main__":
    run_day(run_all, [1])
