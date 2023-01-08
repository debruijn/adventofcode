from typing import Union
from util.util import timing

debug = False


def run_program(data):
    accumulator = 0
    curr_ind = 0
    stop = False
    inds_visited = set()
    while not stop:
        if curr_ind not in inds_visited:
            inds_visited.add(curr_ind)
        else:
            return accumulator, False
        if curr_ind >= len(data):
            return accumulator, True
        row = data[curr_ind]
        if row.startswith('nop'):
            curr_ind += 1
        elif row.startswith('acc'):
            accumulator += int(row.split(' ')[1])
            curr_ind += 1
        else:
            curr_ind += int(row.split(' ')[1])


@timing
def run_all(example_run: Union[int, bool]):

    file = f'aoc_8_exampledata{example_run}' if example_run else 'aoc_8_data'
    with open(file) as f:
        data = f.readlines()
    adj_data = [row.rstrip('\n') for row in data]

    result_part1, _ = run_program(adj_data)

    accumulator = 0
    for idrow, row in enumerate(adj_data):
        if row.startswith('nop') or row.startswith('jmp'):
            iter_data = adj_data.copy()
            iter_data[idrow] = row.replace('nop', 'jmp') if row.startswith('nop') else row.replace('jmp', 'nop')
            accumulator, success = run_program(iter_data)
            if success:
                break

    result_part2 = accumulator

    print(f'\nResults for {f"example" if example_run else "my"} input{f" {example_run}" if example_run else ""}:')
    print(f' Result of part 1: {result_part1}')
    print(f' Result of part 2: {result_part2}')

    print(f'\nDescriptives: \n Length of program: {len(data)}'
          f'\n Corrupted instruction: instruction {idrow} with text "{row}" \n')


if __name__ == "__main__":
    [run_all(example_run=i) for i in [1]]
    run_all(example_run=False)
