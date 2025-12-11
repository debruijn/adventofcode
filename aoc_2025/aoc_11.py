from collections import defaultdict
from functools import cache
from itertools import permutations
from typing import Union
from util.util import ProcessInput, run_day

run_backwards = True
run_old = False


def get_count_full_steps(data_dict, start='you', end='out'):
    queue = data_dict[start].copy()
    count = 0
    while len(queue) > 0:
        this = queue.pop()
        if this == end:
            count += 1
        else:
            queue.extend(data_dict[this])
    return count


def run_all(example_run: Union[int, bool]):
    data = ProcessInput(example_run=example_run, day=11, year=2025).data

    data_dict = {'out': []}
    rev_dict = defaultdict(list)
    for row in data:
        ind, res = row.split(': ')
        data_dict[ind] = res.split(' ')
        for x in res.split(' '):
            rev_dict[x].append(ind)

    @cache
    def get_count(curr, target):
        if curr == target:
            return 1
        return sum(get_count(x, target) for x in (rev_dict[curr] if run_backwards else data_dict[curr]))

    if example_run == False or example_run == 1:
        # Old approach part 1
        if run_old:
            if run_backwards:
                # For some reason doesn't work anymore - since it is old slow approach, I won't fix this reverse route.
                # count = get_count_full_steps(rev_dict, 'out', 'you')
                count = get_count_full_steps(data_dict, 'you', 'out')
            else:
                count = get_count_full_steps(data_dict, 'you', 'out')
        else:
            count = get_count('out', 'you')
    else:
        count = "N/A"

    result_part1 = count

    if example_run == False or example_run == 2:
        start, end = ('out', 'svr') if run_backwards else ('svr', 'out')
        count = 0

        # From start to end, either go via dac and then fft or first fft and then dac.
        for x, y in permutations(['dac', 'fft'], 2):
            count += get_count(start, x) * get_count(x, y) * get_count(y, end)
    else:
        count = "N/A"
    result_part2 = count

    extra_out = {'Number of devices in input': len(data),
                 'Biggest list of outputs for one device': max(len(x) for x in data_dict.values()),
                 'Count of most common output across devices': max(len(x) for x in rev_dict.values()),
                 'Size of cache': get_count.cache_info().currsize}

    return result_part1, result_part2, extra_out


if __name__ == "__main__":
    run_day(run_all, [1, 2])
