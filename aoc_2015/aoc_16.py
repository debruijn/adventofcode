from typing import Union
from util.util import ProcessInput, run_day, batched


def run_all(example_run: Union[int, bool]):

    data = ProcessInput(example_run=example_run, day=16, year=2015).data

    # Hard-coded input from the problem description.
    to_check = {'children': 3,
                'cats': 7,
                'samoyeds': 2,
                'pomeranians': 3,
                'akitas': 0,
                'vizslas': 0,
                'goldfish': 5,
                'trees': 3,
                'cars': 2,
                'perfumes': 1}

    # Part 1 - self-explanatory, just explicitly checking all Sues to find one that meets all criteria
    nr_sue = "TODO"
    for row in data:
        row = row.replace(':', '')
        this_passes = True
        for k, v in batched(row.split()[2:], 2):
            if to_check[k] != int(v.replace(',', '')):
                this_passes = False
                continue
        if this_passes:
            nr_sue = row.split()[1]
            break

    result_part1 = nr_sue

    # Part 2 - self-explanatory, just explicitly checking the adjusted criteria for cats/trees and pomeranians/goldfish.
    nr_sue = "TODO"
    for row in data:
        row = row.replace(':', '')
        this_passes = True
        for k, v in batched(row.split()[2:], 2):
            if k in ['cats', 'trees']:
                if to_check[k] >= int(v.replace(',', '')):
                    this_passes = False
                    continue
            elif k in ['pomeranians', 'goldfish']:
                if to_check[k] <= int(v.replace(',', '')):
                    this_passes = False
                    continue
            else:
                if to_check[k] != int(v.replace(',', '')):
                    this_passes = False
                    continue
        if this_passes:
            nr_sue = row.split()[1]
            break

    result_part2 = nr_sue

    extra_out = {'Number of Sues in input': len(data),
                 'Number of items to check': len(to_check)}

    return result_part1, result_part2, extra_out


if __name__ == "__main__":
    run_day(run_all, [])
