from typing import Union
from util.util import run_day

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

    extra_out = {'Length of program': len(data),
                 'Corrupted instruction:': f"instruction {idrow} with text '{row}'"}
    return result_part1, result_part2, extra_out


if __name__ == "__main__":
    run_day(run_all, [1])
