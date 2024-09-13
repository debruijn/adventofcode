from typing import Union
from util.util import ProcessInput, run_day


def run_program(data, a=0, b=0, range_init=(1, 17)):

    # First part: create a
    for i, row in enumerate(data[range_init[0]:range_init[1]]):
        a = a + 1 if row.startswith('inc') else 3 * a

    # Second part: reduce a down to 1
    while a != 1:
        b += 1
        a = a // 2 if a % 2 == 0 else 3 * a + 1

    return b


def run_all(example_run: Union[int, bool]):

    data = ProcessInput(example_run=example_run, day=23, year=2015).data

    # Interpretational solution - like is normal in later years (but apparently was not back in 2015 yet?)
    # This program increases a by adding 1 or tripling, in 2 different ways for both parts (depending on whether it
    # skips the first part or the middle part of tpl/inc.
    # Then, the latter part will increase b by 1 for each operation on a (a//2 or 3*a+1) until a==1.

    result_part1 = run_program(data)
    result_part2 = run_program(data, a=1, range_init=(18, 39))

    extra_out = {'Number of commands in program': len(data)}

    return result_part1, result_part2, extra_out


if __name__ == "__main__":
    run_day(run_all, [])
