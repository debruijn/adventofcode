from collections import deque, defaultdict
from itertools import product, accumulate, pairwise
from typing import Union
from util.util import ProcessInput, run_day


def mix(num, secret):
    return num ^ secret


def prune(secret):
    return secret % 16777216


def new(secret):
    secret = prune(mix(secret * 64, secret))
    secret = prune(mix(secret // 32, secret))
    secret = prune(mix(secret * 2048, secret))
    return secret


def price(secret):
    return secret % 10


def run_all(example_run: Union[int, bool]):

    data = ProcessInput(example_run=example_run, day=22, year=2024).as_int().data

    # Part 1 and prep for part 2: find all 2001 first secrets (and thus also the final one)
    N = 2000
    sum_secrets = 0
    all_secrets = []
    for num in data:
        these_secrets = [num]
        for _ in range(N):
            num = new(num)
            these_secrets.append(num)
        sum_secrets += num
        all_secrets.append(these_secrets)

    result_part1 = sum_secrets

    # For each buyer, loop over all diffs and if pattern is new (for that buyer), add the price to a counter
    total_price_diff = defaultdict(int)
    for nums in all_secrets:
        diffs = [price(y) - price(x) for x, y in pairwise(nums)]
        hist = set()
        for i in range(len(diffs)-3):
            this_diffs = tuple(diffs[i:i+4])  # tuple for hashability
            if this_diffs not in hist:
                hist.add(this_diffs)
                total_price_diff[this_diffs] += price(nums[i+4])
    result_part2 = max(total_price_diff.values())

    extra_out = {'Number of secrets in input': len(data)}

    return result_part1, result_part2, extra_out


if __name__ == "__main__":
    run_day(run_all, [1, 2, 3])
