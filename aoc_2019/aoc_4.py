from typing import Union
from util.util import ProcessInput, run_day
from collections import Counter

debug = False


def check(x, part=1):
    digits = [int(y) for y in str(x)]
    if any([digits[i] > digits[i + 1] for i in range(len(digits) - 1)]):  # non-decreasing
        return False
    if not any([digits[i] == digits[i + 1] for i in range(len(digits) - 1)]):  # any double digits
        return False
    if part == 2:
        check_double_digit = [digits[i] == digits[i + 1] for i in range(len(digits) - 1)]
        check_outer_digits = [check_double_digit[0] and (digits[0] != digits[2]),
                              check_double_digit[-1] and (digits[-3] != digits[-1])]
        check_inner_digits = [check_double_digit[i] and digits[i] != digits[i + 2] and digits[i] != digits[i - 1]
                              for i in range(1, len(digits) - 2)]
        if not any(check_inner_digits + check_outer_digits):
            return False
    return True


# alternative check: count occurrence of digits in variable digits -> is there any count >=2 (part 1) or ==2 (part 2)
def check_alt(x, part=1):
    digits = [int(y) for y in str(x)]
    if any([digits[i] > digits[i + 1] for i in range(len(digits) - 1)]):  # non-decreasing
        return False
    if part == 1:
        return True if any(d >= 2 for d in Counter(digits).values()) else False
    if part == 2:
        return True if 2 in Counter(digits).values() else False


def run_all(example_run: Union[int, bool]):

    data = ProcessInput(example_run=example_run, day=4, year=2019).data
    pswd_range = [int(x) for x in data[0].split('-')]

    result_part1 = 0
    result_part2 = 0
    for pswd_i in range(pswd_range[0], pswd_range[1]+1):
        result_part1 += check_alt(pswd_i)
        result_part2 += check_alt(pswd_i, part=2)

    extra_out = {'Range of input': pswd_range[1] - pswd_range[0] + 1}

    return result_part1, result_part2, extra_out


if __name__ == "__main__":
    run_day(run_all, [])
