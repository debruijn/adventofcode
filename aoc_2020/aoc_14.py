from typing import Union
from util.util import ProcessInput, run_day
from collections import defaultdict
from collections.abc import Iterable

debug = False


def flatten(xs):
    for x in xs:
        if isinstance(x, Iterable) and not isinstance(x, (str, bytes)):
            yield from flatten(x)
        else:
            yield x


def number_to_base(n, b):
    # Generic function to convert numbers to a base format, and output as string
    if n == 0:
        return "0"
    digits = []
    while n:
        digits.append(int(n % b))
        n //= b
    return "".join(str(x) for x in digits[::-1])


def convert_to_36bit(str_i):
    return "".join(["0"] * (36 - len(str_i))) + str_i


def get_floating_bitmasks(str_i):
    if str_i.count('X') == 1:
        return [int(str_i.replace('X', '0'), 2), int(str_i.replace('X', '1'), 2)]
    else:
        return [get_floating_bitmasks(str_i.replace('X', '0', 1)), get_floating_bitmasks((str_i.replace('X', '1', 1)))]


def run_all(example_run: Union[int, bool]):
    data = ProcessInput(example_run=example_run, day=14).data

    memory_dict = defaultdict(str)
    curr_mask = ''.join(['x'] * 32)
    for row in data:
        if row.startswith('mask'):
            curr_mask = row.replace('mask = ', '')
        else:
            row = row.replace('mem[', '').split('] = ')
            num_as_binary = convert_to_36bit(number_to_base(int(row[1]), 2))
            memory_dict[row[0]] = "".join([num_as_binary[x] if curr_mask[x] == 'X' else curr_mask[x]
                                           for x in range(len(curr_mask))])

    result_part1 = sum(int(x, 2) for x in memory_dict.values())

    if example_run == 1:
        result_part2 = "Not feasible"
    else:
        memory_dict2 = defaultdict(int)
        curr_mask = ''.join(['x'] * 32)
        for row in data:
            if row.startswith('mask'):
                curr_mask = row.replace('mask = ', '')
            else:
                row = row.replace('mem[', '').split('] = ')
                num_as_binary = convert_to_36bit(number_to_base(int(row[0]), 2))
                bitmasks_applied = "".join([num_as_binary[x] if curr_mask[x] == '0' else curr_mask[x]
                                            for x in range(len(curr_mask))])
                floating_locations = get_floating_bitmasks(bitmasks_applied)
                floating_locations = flatten(floating_locations)
                for loc in floating_locations:
                    memory_dict2[loc] = int(row[1])

        result_part2 = sum(memory_dict2.values())

    extra_out = {'Number of rows in input': len(data),
                 'Number of unique vals': len(memory_dict)}

    return result_part1, result_part2, extra_out


if __name__ == "__main__":
    run_day(run_all, [1, 2])
