import math
import operator
import itertools
from collections import defaultdict
from typing import Union
from util.util import timing, ProcessInput, run_day


def get_permutations(nr):
    permutations = {0: 1,
                    1: 1,
                    2: 2,
                    3: 4,
                    4: 7,
                    5: 13}
    permutations = defaultdict(lambda: get_permutations_sim(nr), permutations)
    return permutations[nr]


def get_permutations_sim(nr):
    raw_options = ['1' + "".join(x) + '1' for x in itertools.product('01', repeat=nr-1 if nr >= 1 else 0)]
    checked_options = [x for x in raw_options if not any([len(y) >= 3 for y in x.split('1')])]
    return len(checked_options)


@timing
def run_all(example_run: Union[int, bool]):

    data = ProcessInput(example_run=example_run, day=10).as_int().sort().data
    data = [0] + data + [max(data)+3]
    diff_data = list(map(operator.sub, data[1:], data[:-1]))

    diff1 = sum([x == 1 for x in diff_data])
    diff3 = sum([x == 3 for x in diff_data])
    result_part1 = diff1 * diff3

    diff_strings = [str(x) for x in diff_data]  # Convert numbers to strings to allow string splitting on value 3
    count_1diffs = [len(x) for x in "".join(diff_strings).split('3')]  # Find length of stretches of diff==1
    result_part2 = math.prod([get_permutations(x) for x in count_1diffs])

    extra_out = {'Number of adapters': len(data),
                 'Number of stretches of 1 diff in a row': len(count_1diffs),
                 'Max numbre of 1 diff in a row': max(count_1diffs)}

    return result_part1, result_part2, extra_out


if __name__ == "__main__":
    run_day(run_all, [1, 2])
