
from typing import Union
from util import timing

debug = False


def next_blizzards(blizzard_locs, map_dims, blizzard_dirs):
    new_blizzards = []
    for i in range(len(blizzard_locs)):
        blz = blizzard_locs[i]
        dir = blizzard_dirs[i]
        if blz[0] + dir[0] >= map_dims[0] - 1:
            new_blz = (1, blz[1])
        elif blz[1] + dir[1] >= map_dims[1] - 1:
            new_blz = (blz[0], 1)
        elif blz[0] + dir[0] <= 0:
            new_blz = (map_dims[0] - 2, blz[1])
        elif blz[1] + dir[1] <= 0:
            new_blz = (blz[0], map_dims[1] - 2)
        else:
            new_blz = (blz[0] + dir[0], blz[1] + dir[1])
        new_blizzards.append(new_blz)

    return new_blizzards


def optimal_path(blizzard_locs, blizzard_dirs, start_loc, map_dims, target_loc):
    queue = list()
    queue.append((0, start_loc))
    curr_time = 0
    blizzards_time = {0: blizzard_locs}
    blizzards_time.update({1: next_blizzards(blizzard_locs, map_dims, blizzard_dirs)})
    result = 10000000000000000000000000000

    while queue:

        t, loc = queue.pop(0)

        if loc == target_loc:  #:
            result = t
            break

        if t > curr_time:
            if debug:
                print(f"{t}: {len(queue)+1}, {loc}")
            blizzards_time.update({t + 1: next_blizzards(blizzards_time[t], map_dims, blizzard_dirs)})
            curr_time = t

        # New candidates in every direction:
        if (loc[0] + 1, loc[1]) not in blizzards_time[t + 1]:
            if (loc[1] == map_dims[1] - 2 and loc[0] + 1 <= map_dims[0] - 1) or loc[0] + 1 <= map_dims[0] - 2:
                cand = (t + 1, (loc[0] + 1, loc[1]))
                if cand not in queue:
                    queue.append(cand)
        if (loc[0], loc[1] + 1) not in blizzards_time[t + 1] and loc[1] + 1 <= map_dims[1] - 2 and loc[0] != start_loc[
            0]:
            cand = (t + 1, (loc[0], loc[1] + 1))
            if cand not in queue:
                queue.append(cand)
        if (loc[0] - 1, loc[1]) not in blizzards_time[t + 1]:
            if (loc[1] == 1 and loc[0] - 1 >= 0) or loc[0] - 1 >= 1:
                cand = (t + 1, (loc[0] - 1, loc[1]))
                if cand not in queue:
                    queue.append(cand)
        if (loc[0], loc[1] - 1) not in blizzards_time[t + 1] and loc[1] - 1 >= 1 and loc[0] != start_loc[0]:
            cand = (t + 1, (loc[0], loc[1] - 1))
            if cand not in queue:
                queue.append(cand)
        if loc not in blizzards_time[t + 1]:
            cand = (t + 1, loc)
            if cand not in queue:
                queue.append(cand)

    return result, blizzards_time


@timing
def run_all(example_run: Union[int, bool]):
    file = f'aoc_24_exampledata{example_run}' if example_run else 'aoc_24_data'
    with open(file) as f:
        data = f.readlines()
    adj_data = [row.rstrip('\n') for row in data]

    blizzard_locs = []
    blizzard_dirs = []
    for i in range(len(adj_data)):
        for j in range(len(adj_data[i])):
            if adj_data[i][j] in ">v<^":
                blizzard_locs.append((i, j))
                if adj_data[i][j] == ">":
                    blizzard_dirs.append((0, 1))
                elif adj_data[i][j] == "v":
                    blizzard_dirs.append((1, 0))
                elif adj_data[i][j] == "<":
                    blizzard_dirs.append((0, -1))
                elif adj_data[i][j] == "^":
                    blizzard_dirs.append((-1, 0))

    map_shape = (len(adj_data), len(adj_data[0]))
    start = (0, 1)
    end = (map_shape[0] - 1, map_shape[1] - 2)
    result_part1, blizzards_time = optimal_path(blizzard_locs, blizzard_dirs, start, map_shape, end)
    result_midway, blizzards_time2 = optimal_path(blizzards_time[result_part1], blizzard_dirs, end, map_shape, start)
    result_2nd, _ = optimal_path(blizzards_time2[result_midway], blizzard_dirs, start, map_shape, end)
    result_part2 = result_part1 + result_midway + result_2nd

    print(f'\nResults for {f"example" if example_run else "my"} input{f" {example_run}" if example_run else ""}:')
    print(f' Result of part 1: {result_part1}')
    print(f' Result of part 2: {result_part1} + {result_midway} + {result_2nd} = {result_part2}')

    print(f'\nDescriptives: \n Number blizzards: {len(blizzard_locs)} \n'
          f' Map shape: {map_shape} \n')


if __name__ == "__main__":
    [run_all(example_run=i) for i in [1, 2]]
    run_all(example_run=False)
