from typing import Union
from util import timing
import tqdm


debug = False


def get_loc(loc, num, N):
    new_loc = loc + num
    new_loc %= N
    if new_loc <= 0:
        new_loc += N
    return new_loc


def run_mixing(original, multiplier, R):

    original = [x * multiplier for x in original]
    mix = [x for x in range(len(original))]
    N = len(original)

    for r in tqdm.trange(R):
        if debug:
            print(f"{r}: {mix}, {[original[mix[i]] for i in range(N)]}")
        for i in range(N):
            num = original[i]
            loc = mix.index(i)
            get = mix.pop(loc)
            new_loc = get_loc(loc, num, N-1)
            mix.insert(new_loc, get)
            if debug:
                print(f"{num}, {loc}, {get}, {new_loc}, {mix}, {[original[mix[i]] for i in range(N)]}")
        if debug:
            print(f"{r}: {mix}")

    loc0 = mix.index(original.index(0))
    locs = [(loc0 + 1000) % N, (loc0 + 2000) % N, (loc0 + 3000) % N]

    return sum([original[mix[i]] for i in locs])


@timing
def run_all(example_run: Union[int, bool]):

    file = f'aoc_20_exampledata{example_run}' if example_run else 'aoc_20_data'
    with open(file) as f:
        data = f.readlines()
    adj_data = [int(row.rstrip('\n')) for row in data]

    result_part1 = run_mixing(adj_data, 1, 1)
    result_part2 = run_mixing(adj_data, 811589153, 10)

    print(f'\nResults for {f"example" if example_run else "my"} input{f" {example_run}" if example_run else ""}:')
    print(f' Result of part 1: {result_part1}')
    print(f' Result of part 2: {result_part2}')

    print(f'\nDescriptives: \n Length of data: {len(adj_data)} \n'
          f' Range: from {min(adj_data)} to {max(adj_data)} \n'
          f' Original location of 0: {adj_data.index(0)}\n')


if __name__ == "__main__":
    [run_all(example_run=i) for i in [1]]
    run_all(example_run=False)
