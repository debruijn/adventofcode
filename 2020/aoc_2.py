from typing import Union
from util import timing


debug = False


@timing
def run_all(example_run: Union[int, bool]):

    file = f'aoc_2_exampledata{example_run}' if example_run else 'aoc_2_data'
    with open(file) as f:
        data = f.readlines()
    adj_data = [row.rstrip('\n') for row in data]

    sum_valid1 = 0
    sum_valid2 = 0
    for row in adj_data:
        policy, password = row.split(': ')
        bounds, test_char = policy.split(' ')
        lb, ub = (int(x) for x in bounds.split('-'))
        times = password.count(test_char)
        if lb <= times <= ub:
            sum_valid1 += 1

        if (password[lb-1] == test_char) + (password[ub-1] == test_char) == 1:
            sum_valid2 += 1

    result_part1 = sum_valid1
    result_part2 = sum_valid2

    print(f'\nResults for {f"example" if example_run else "my"} input{f" {example_run}" if example_run else ""}:')
    print(f' Result of part 1: {result_part1}')
    print(f' Result of part 2: {result_part2}')


if __name__ == "__main__":
    [run_all(example_run=i) for i in [1]]
    run_all(example_run=False)
