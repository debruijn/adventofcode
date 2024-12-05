from typing import Union

from utils.lists import flatten

from util.util import ProcessInput, run_day
from functools import cmp_to_key, partial


def comp_func(x1, x2, rules):
    if (x1, x2) in rules:
        return -1
    elif (x2, x1) in rules:
        return 1
    return 0


def run_all(example_run: Union[int, bool]):

    data = ProcessInput(example_run=example_run, day=5, year=2024).as_list_of_strings_per_block().data

    # Process rules to get sorted version of the pages according to those rules using a page_key from comp_to_key
    rules = [tuple(int(y) for y in x.split('|')) for x in data[0]]
    pages = list(set(flatten(rules)))
    page_key = cmp_to_key(partial(comp_func, rules=rules))
    pages = sorted(pages, key=page_key)

    # With the sorted pages, just check whether a update row is following that sort or not
    sum_of_correct_middle_pages = 0
    sum_of_incorrect_middle_pages = 0
    for row in data[1]:
        i_row = [int(x) for x in row.split(',')]
        if i_row == sorted(i_row, key=page_key):
            sum_of_correct_middle_pages += i_row[len(i_row)//2]
        else:
            sum_of_incorrect_middle_pages += sorted(i_row, key=page_key)[len(i_row) // 2]

    result_part1 = sum_of_correct_middle_pages
    result_part2 = sum_of_incorrect_middle_pages

    extra_out = {'Number of updates to check': len(data[1]),
                 'Number of rules': len(rules),
                 'Number of pages within those rules': len(pages)}

    return result_part1, result_part2, extra_out


if __name__ == "__main__":
    run_day(run_all, [1])
