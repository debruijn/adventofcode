from typing import Union
from util.util import run_day, get_example_data
from aocd import get_data

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

    if example_run:
        adj_data = get_example_data(2020, 8, example_run-1)
    else:
        data_raw = get_data(day=8, year=2020)
        adj_data = [x for x in data_raw.split('\n')]

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

    extra_out = {'Length of program': len(adj_data),
                 'Corrupted instruction:': f"instruction {idrow} with text '{row}'"}
    return result_part1, result_part2, extra_out


if __name__ == "__main__":
    run_day(run_all, [1])
