from collections import Counter, defaultdict
from typing import Union
from util.util import ProcessInput, run_day

debug = False


def run_all(example_run: Union[int, bool]):

    data = ProcessInput(example_run=example_run, day=4, year=2018).data
    data = sorted(data)

    # Processing: for each guard, keep track (using a Counter) how many teams asleep at each minute
    count_shifts = Counter()
    count_asleep = defaultdict(Counter)
    curr_guard = -9999
    start_sleep = 0
    for row in data:
        if row.endswith('begins shift'):
            curr_guard = int(row[row.find('#')+1:].split(' ')[0])
            count_shifts[curr_guard] += 1
        elif row.endswith('falls asleep'):
            start_sleep = int(row.split(']')[0].split(' ')[-1].split(':')[1])
        else:
            end_sleep = int(row.split(']')[0].split(' ')[-1].split(':')[1])
            this_nap = Counter(range(start_sleep, end_sleep))
            count_asleep[curr_guard].update(this_nap)

    # Part 1: use Counter.total() to get the total minutes asleep for each guard, and use that to find most sleepy
    most_sleepy_guard = max(count_asleep, key=lambda x: count_asleep[x].total())
    most_sleepy_minute = count_asleep[most_sleepy_guard].most_common(1)[0][0]
    result_part1 = most_sleepy_guard * most_sleepy_minute

    # Part 2: adjust lambda to take the most common minute for each guard as the criterion.
    most_sleepy_guard_alt = max(count_asleep, key=lambda x: count_asleep[x].most_common(1)[0][1])
    most_sleepy_minute_alt = count_asleep[most_sleepy_guard_alt].most_common(1)[0][0]
    result_part2 = most_sleepy_guard_alt * most_sleepy_minute_alt

    # Bonus part 3: actual most sleepy guard by taking number of shifts into account. Note that in example, both have a
    # minute for which they always sleep but this only returns 1 (which is enough to find a max).
    actual_most_sleepy_guard = max(count_asleep, key=lambda x: count_asleep[x].most_common(1)[0][1]/count_shifts[x])
    actual_most_sleepy_minute, number_times_asleep = count_asleep[actual_most_sleepy_guard].most_common(1)[0]
    perc_asleep = number_times_asleep / count_shifts[actual_most_sleepy_guard] * 100

    extra_out = {'Number of notes in input': len(data),
                 'Number of guards': len(count_asleep),
                 'Most sleepy guard': f'{most_sleepy_guard}, the most at {most_sleepy_minute}' ,
                 'Most sleepy minute': f'{most_sleepy_minute_alt}, by guard {most_sleepy_guard_alt}',
                 'Relative most sleepy guard': f'{actual_most_sleepy_guard}, the most at {actual_most_sleepy_minute}, '
                                               f'asleep at {perc_asleep:.2f}%'
                 }

    return result_part1, result_part2, extra_out


if __name__ == "__main__":
    run_day(run_all, [1])
