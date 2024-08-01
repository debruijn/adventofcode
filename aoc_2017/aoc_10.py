import operator
from typing import Union
from util.util import ProcessInput, run_day
from itertools import islice, accumulate


def batched(iterable, n):
    # batched('ABCDEFG', 3) → ABC DEF G
    # From Python 3.12 documentation
    iterator = iter(iterable)
    while batch := tuple(islice(iterator, n)):
        yield batch


def do_knot_hash_algorithm(list_nrs, data, curr_pos=0, skip_size=0):
    # Apply knot-hash algorithm, with the only "challenging" component being the split in whether we overrun the list
    # length or not.
    for num in data:
        if curr_pos + num <= len(list_nrs):  # No overrun: we can directly take the part that is to be reversed.
            reversed_list = list_nrs[curr_pos:curr_pos+num]
            reversed_list.reverse()
            list_nrs = list_nrs[:curr_pos] + reversed_list + list_nrs[curr_pos+num:]
        else:  # There is an overrun: we need to combine end & start of list, reverse it, and carefully put it back
            this_overrun = curr_pos + num - len(list_nrs)
            reversed_list = list_nrs[curr_pos:] + list_nrs[:this_overrun]
            reversed_list.reverse()
            list_nrs = reversed_list[-this_overrun:] + list_nrs[this_overrun:curr_pos] + reversed_list[:-this_overrun]
        curr_pos = (curr_pos + num + skip_size) % len(list_nrs)
        skip_size += 1
    return list_nrs, curr_pos, skip_size


def run_all(example_run: Union[int, bool]):
    # Part 1: read data, with a hard-coded 2nd example. For example 1, the spaces need to be removed.
    if example_run == 2:
        data = [1, 2, 3]
    else:
        data = ProcessInput(example_run=example_run, day=10, year=2017).remove_substrings(
            ' ').as_list_of_ints(pattern=',').data[0]

    # Part 1: apply 1 round of the algorithm
    list_nrs = list(range(256 if not example_run else 5))
    list_nrs, _, _ = do_knot_hash_algorithm(list_nrs, data)
    result_part1 = list_nrs[0] * list_nrs[1]

    # Part 2: reread data, since now they can't be converted to integers directly but we need to use ord(.).
    if example_run == 2:
        data = "1,2,3"
    else:
        data = ProcessInput(example_run=example_run, day=10, year=2017).remove_substrings(' ').data[0]
    extended_data = [ord(x) for x in data] + [17, 31, 73, 47, 23]

    # Part 2: apply 64 rounds of the algorithm
    list_nrs = list(range(256))
    curr_pos, skip_size = 0, 0
    for _ in range(64):
        list_nrs, curr_pos, skip_size = do_knot_hash_algorithm(list_nrs, extended_data, curr_pos, skip_size)

    # Part 2: get the dense hash by running xor on each 16-length sublist
    dense_hash = []
    for sublist in batched(list_nrs, 16):
        dense_hash.append(list(accumulate(sublist, operator.xor, initial=None))[-1])

    # Part 2: get the hexed hash by converting each element in the dense hash to a hex, padding with a 0 if needed.
    hex_hash = ""
    for element in dense_hash:
        hexed_el = hex(element)[2:]
        hexed_el = "0" + hexed_el if len(hexed_el) == 1 else hexed_el
        hex_hash += hexed_el

    result_part2 = hex_hash

    extra_out = {'Number of characters in input': len(data),
                 'Dense hash': dense_hash}

    return result_part1, result_part2, extra_out


if __name__ == "__main__":
    run_day(run_all, [1, 2])  # d3285dc610a8b4dcf5dbe590e508a4a2  # 624271549ac0159cb72edb16e582ab4e
