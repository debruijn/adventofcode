import functools
from typing import Union
from util.util import ProcessInput, run_day

debug = False
part1_recursive = True


# I know recursive and dynamic don't exclude each other, I just gave these terms to the two approaches here :)
# It's more "recursively replacing" and "dynamically decomposing" the patterns


def check_directly(record, count):
    lengths = [len(x) for x in record.split('.') if x!= ""]
    return lengths == count


def check_recursively(record, count):
    if record.count('?') == 0:
        return check_directly(record, count)
    elif record.count('?') + record.count('#') < sum(count):
        return 0
    elif record.count('#') > sum(count):
        return 0
    elif record.count('#') == sum(count):
        return check_directly(record.replace('?', '.'), count)
    elif record.count('?') + record.count('#') == sum(count):
        return check_directly(record.replace('?', '#'), count)
    else:
        return (check_recursively(record.replace('?', '#', 1), count) +
                check_recursively(record.replace('?', '.', 1), count))


@functools.cache
def count_dynamically(record, count, curr_len=0):
    # Could add early stopping by checking remainder of record with remainder of count/curr_len: are there enough #s?

    if not record:  # Empty remainder: no string to check -> only add 1 if there was nothing to count anymore!
        return 1 if not count and not curr_len else 0
    this_sum = 0
    # Compare first next item, and based on what it is, do next step: continue or break (or both, if '?')
    if record[0] in ("#", "?"):
        this_sum += count_dynamically(record[1:], count, curr_len + 1) # continue current streak of #s
    if record[0] in (".", "?") and (count and count[0] == curr_len or not curr_len): # compare current length with next req
        this_sum += count_dynamically(record[1:], count[1:] if curr_len else count)
    return this_sum


def run_all(example_run: Union[int, bool]):

    data = ProcessInput(example_run=example_run, day=12, year=2023).data

    sum_arrangements_1 = 0
    sum_arrangements_2 = 0
    total_count = 0
    total_groups = 0

    for row in data:
        record, count = row.split(' ')
        count = [int(x) for x in count.split(',')]
        total_count += sum(count)
        total_groups += len(count)
        sum_arrangements_1 += check_recursively(record, count) if part1_recursive else (
            count_dynamically(record + '.', tuple(count)))
        sum_arrangements_2 += count_dynamically((record + '?') * 4 + record + '.', tuple(count * 5), 0)

    result_part1 = sum_arrangements_1
    result_part2 = sum_arrangements_2

    extra_out = {'Number of rows in input': len(data),
                 'Total count of #': total_count,
                 'Total count of groups of #': total_groups}

    return result_part1, result_part2, extra_out


if __name__ == "__main__":
    run_day(run_all, [1])
