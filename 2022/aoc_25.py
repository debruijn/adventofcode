from typing import Union
from util import timing


debug = False


def number_to_base(n, b):
    # Generic function to convert numbers to a base format - no SNAFU adjustments here.
    if n == 0:
        return [0]
    digits = []
    while n:
        digits.append(int(n % b))
        n //= b
    return digits[::-1]


@timing
def run_all(example_run: Union[int, bool]):

    file = f'aoc_25_exampledata{example_run}' if example_run else 'aoc_25_data'
    with open(file) as f:
        data = f.readlines()  #
    adj_data = [row.rstrip('\n') for row in data]

    total = 0
    base = 5
    for row in adj_data:
        pos_part = int(row.replace('=', '0').replace('-', '0'), base)
        neg_part = int(row.replace('2', '0').replace('1', '0').replace('=', '2').replace('-', '1'), base)
        total += pos_part - neg_part

    base5_total = number_to_base(total, base)

    # Loop over digits from the back. If 3 or 4, replace with = or - and increase one to previous digit
    result = ""
    for i in range(len(base5_total)-1, -1, -1):
        if base5_total[i] == 3:
            result = "=" + result
            base5_total[i-1] += 1
        elif base5_total[i] == 4:
            result = "-" + result
            base5_total[i-1] += 1
        elif base5_total[i] >= 5:
            result = f"{base5_total[i] - 5}" + result
            base5_total[i-1] += 1
        else:
            result = str(base5_total[i]) + result

    result_part1 = result

    print(f'\nResults for {f"example" if example_run else "my"} input{f" {example_run}" if example_run else ""}:')
    print(f' Result: {result_part1} (which is {total} in base 10).')

    print(f'\nDescriptives: \n Number of fuel requirements: {len(adj_data)} \n')


if __name__ == "__main__":
    [run_all(example_run=i) for i in [1]]
    run_all(example_run=False)
