from functools import cache
from typing import Union
from util.util import ProcessInput, run_day
import math


def get_prime_factors(N):
    factors = []
    N_orig = N
    while N % 2 == 0:
        factors.append(2)
        N = N // 2

    for i in range(3, int(math.sqrt(N_orig)) + 1, 2):
        while N % i == 0:
            factors.append(i)
            N = N // i

    return set(factors)


@cache
def get_divisors(N, filter=False):

    result = []
    prime_factors = get_prime_factors(N)

    for i in [x for x in prime_factors if x <= N ** 0.5]:
        result.extend([(N // i) * x for x in get_divisors(i, filter)])
        if i != N // i:
            result.extend([i * x for x in get_divisors(N // i, filter)])
    if not filter:
        return set(result + [1, N])
    else:
        return [i for i in set(result + [1, N]) if N <= 50 * i]


def calc_presents(N, k=10, filter=False):
    return sum(get_divisors(N, filter)) * k


def run_all(example_run: Union[int, bool]):

    data = ProcessInput(example_run=example_run, day=20, year=2015).as_single_int().data

    curr = 1
    stop = False
    while not stop:
        if calc_presents(curr) >= data:
            stop = True
        else:
            curr += 1

    result_part1 = curr

    curr = 1
    stop = False
    while not stop:
        if calc_presents(curr, k=11, filter=True) >= data:
            stop = True
        else:
            curr += 1
    result_part2 = curr

    extra_out = {'Number in input': data}

    return result_part1, result_part2, extra_out


if __name__ == "__main__":
    run_day(run_all, [])
