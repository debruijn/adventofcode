from itertools import groupby
from typing import Union
from util.util import ProcessInput, run_day


def run_all(example_run: Union[int, bool]):

    data = ProcessInput(example_run=example_run, day=10, year=2015).data

    # I love itertools, and now the new example of that: groupby. An earlier implementation in which I did this manually
    # got very slow (especially for the additional 10..) and it also took me a for-loop in 10 extra lines compared to
    # what I have now.
    # For whom groupby is new: you can use it to get subsequent iterators of the same value. You get it basically like
    # this: [(val, iterator), (val, iterator), ..., ]
    # So the iterator will produce the val K times, with K dependent on the input of course. In this case, I could use
    # that to convert to a list, take the length, and convert that to a string, to have how often the 'val' is repeated.

    N = 1 if example_run else 40
    num = data[0]

    for i in range(N):
        num = "".join([str(len(list(y))) + x for x, y in groupby(num)])
    result_part1 = len(num)

    for i in range(10):
        num = "".join([str(len(list(y))) + x for x, y in groupby(num)])
    result_part2 = len(num)

    extra_out = {'Length of original number': len(data[0])}

    return result_part1, result_part2, extra_out


if __name__ == "__main__":
    run_day(run_all, [1, 2, 3, 4, 5, 6])
