from typing import Union
from util.util import ProcessInput, run_day

debug = False


def get_new_dirs(curr_loc, curr_dir, data):
    i, j = int(curr_loc.real), int(curr_loc.imag)

    if data[i][j] == '.':
        return [curr_dir]
    if data[i][j] == '\\':
        mapping = {1j: 1, 1: 1j, -1: -1j, -1j:-1}
        return [mapping[curr_dir]]
    if data[i][j] == '/':
        mapping = {1j: -1, 1: -1j, -1: 1j, -1j: 1}
        return [mapping[curr_dir]]
    if data[i][j] == '-':
        mapping = {1j: [1j], -1j: [-1j], 1: [1j, -1j], -1: [1j, -1j]}
        return mapping[curr_dir]
    if data[i][j] == '|':
        mapping = {1j: [1, -1], -1j: [1, -1], 1: [1], -1: [-1]}
        return mapping[curr_dir]

    return [1]


def find_energized_tiles(data, curr_loc, curr_dir):
    dims = (len(data), len(data[0]))
    locs = {}
    queue = [(curr_loc, curr_dir)]
    while len(queue) > 0:
        curr_loc, curr_dir = queue.pop(0)
        new_dirs = get_new_dirs(curr_loc, curr_dir, data)
        for new_dir in new_dirs:
            new_loc = curr_loc + new_dir
            add = True
            if not 0 <= new_loc.imag < dims[1] or not 0 <= new_loc.real < dims[0]:
                add = False
            if new_loc in locs.keys():
                if new_dir in locs[new_loc]:
                    add = False
            if add:
                queue.append((new_loc, new_dir))
        if curr_loc not in locs:
            locs[curr_loc] = [curr_dir]
        else:
            locs[curr_loc].append(curr_dir)

    return len(locs)


def run_all(example_run: Union[int, bool]):

    data = ProcessInput(example_run=example_run, day=16, year=2023).data

    dims = (len(data), len(data[0]))
    result_part1 = find_energized_tiles(data, 0+0j, 1j)

    curr_max = result_part1
    for i in range(dims[0]):
        curr_max = max([curr_max,
                        find_energized_tiles(data, i+0j, 1j),
                        find_energized_tiles(data, i+ (dims[1]-1) *1j, -1j)])
    for j in range(dims[1]):
        curr_max = max([curr_max,
                        find_energized_tiles(data, j*1j, 1),
                        find_energized_tiles(data, (dims[0]-1) + j*1j, -1)])
    result_part2 = curr_max

    extra_out = {'Dimension of input': dims}

    return result_part1, result_part2, extra_out


if __name__ == "__main__":
    run_day(run_all, [1])
