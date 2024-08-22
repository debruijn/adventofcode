from typing import Union
from util.util import ProcessInput, run_day
from itertools import chain


def split_row(row_to_split):
    if row_to_split.find('[') < 0:
        return [], [row_to_split]

    next_in, next_out = row_to_split.find('['), row_to_split.find(']')
    next_split = split_row(row_to_split[next_out + 1:])

    return [row_to_split[next_in + 1:next_out]] + next_split[0], [row_to_split[:next_in]] + next_split[1]


def check_abba(str_abba):
    for i in range(len(str_abba) - 3):
        if str_abba[i] == str_abba[i + 3] and str_abba[i + 1] == str_abba[i + 2] and str_abba[i] != str_abba[i + 1]:
            return True
    return False


def check_aba(str_aba):
    valid = []
    for i in range(len(str_aba) - 2):
        if str_aba[i] == str_aba[i + 2] and str_aba[i] != str_aba[i + 1]:
            valid.append("".join(str_aba[i + 1] + str_aba[i] + str_aba[i + 1]))
    return valid


def run_all(example_run: Union[int, bool]):

    data = ProcessInput(example_run=example_run, day=7, year=2016).data

    count_supports_tls = 0  # Part 1
    count_supports_ssl = 0  # Part 2
    nr_hypernet, nr_supernet = 0, 0  # For the extra descriptive output
    for row in data:
        row_in, row_out = split_row(row)  # Find elements within and outside the square brackets
        nr_hypernet += len(row_in)
        nr_supernet += len(row_out)

        # Part 1: check that none "in" are "abba" and at least one "out" is "abba"
        if not any(check_abba(x) for x in row_in) and any(check_abba(x) for x in row_out):
            count_supports_tls += 1

        # Part 2: get all possible "aba"s from "bab"s in "in" and check if any "outs" contain them.
        abas = list(chain(*[check_aba(rw_in) for rw_in in row_in]))
        supports_ssl = False
        for rw_out in row_out:
            if any(rw_out.count(aba)> 0 for aba in abas):
                supports_ssl = True
        count_supports_ssl += supports_ssl

    result_part1 = count_supports_tls
    result_part2 = count_supports_ssl

    extra_out = {'Number of IPs in input': len(data),
                 'Number of hypernet sequences': nr_hypernet,
                 'Number of supernet sequences': nr_supernet}

    return result_part1, result_part2, extra_out


if __name__ == "__main__":
    run_day(run_all, [1, 2, 3, 4])
