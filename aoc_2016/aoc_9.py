from typing import Union
from util.util import ProcessInput, run_day


def get_length(j_string, i_times):
    # Get length of substring "j_string" that is repeated "i_times" using recursion if needed

    i, j, j_len, j_times = get_next_decompression(j_string)
    if i >= 0:  # There is a compression in this j_string
        return i_times * (get_length(j_string[j + 1:j + 1 + j_len], j_times) +
                          get_length(j_string[j + 1 + j_len:], 1))  # Inspect later half for more compressions
    else:
        return i_times * len(j_string)  # No compressions: just length of string times nr of repetitions


def get_next_decompression(j_string):
    # Find next compression within this string - if any. If they exist, find length&times of deduplicated string
    i, j = j_string.find('('), j_string.find(')')
    if i >= 0:
        i_len, i_times = [int(x) for x in j_string[i + 1:j].split('x')]
        return i, j, i_len, i_times
    return -1, -1, 0, 0

def run_all(example_run: Union[int, bool]):

    data = ProcessInput(example_run=example_run, day=9, year=2016).data[0]

    # Part 1: naive implementation. Create a new string with all uncompressed characters; remove from the existing one.
    data_p1 = data
    i = 0
    new_str = ""
    while i < len(data_p1):
        if data_p1[i] == '(':  # For more optimization: could use get_next_decompression() from part 2 instead
            j = data_p1.find(')', i)
            i_len, i_times = [int(x) for x in data_p1[i+1:j].split('x')]
            new_str += data_p1[:i]
            new_str += data_p1[j+1:j+1+i_len]*i_times
            data_p1 = data_p1[j+i_len+1:]
            i = 0
        else:
            i += 1
    new_str += data_p1
    result_part1 = len(new_str)

    # Part 2: don't do the actual decompression but only do the counts.
    data_p2 = data
    i = 0
    count_len = 0
    while i < len(data_p2):
        if data_p2[i] == '(': # For optimization: could use get_next_decompression() here instead of in get_length()
            j = data_p2.find(')', i)
            i_len, i_times = [int(x) for x in data_p2[i+1:j].split('x')]
            count_len += i  # Non-repeated text, basically: len(data[:i])
            count_len += get_length(data_p2[j+1:j+1+i_len], i_times)
            data_p2 = data_p2[j+i_len+1:]
            i = 0
        else:
            i += 1
    count_len += len(data_p2)
    result_part2 = count_len

    extra_out = {'Number of characters in compressed input': len(data)}

    return result_part1, result_part2, extra_out


if __name__ == "__main__":
    run_day(run_all, list(range(1, 7)))
