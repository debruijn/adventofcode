from typing import Union
from util.util import ProcessInput, run_day

debug = False


def run_all(example_run: Union[int, bool]):

    data = ProcessInput(example_run=example_run, day=10, year=2023).data

    # Find locations of pipe and especially of S
    locs = {}
    S_loc = 0
    for i, row in enumerate(data):
        for k, el in enumerate(row):
            if el != '.':
                locs.update({(i + k*1j): el})  # Use complex numbers for 2D indices
            if el == 'S':
                S_loc = i + k*1j  # Use complex numbers for 2D indices

    # Direction mapping, used like "If you pass through an 'F' from direction -1, you come out in direction 1j"
    dir_mapping = {(1, '|'): 1, (-1, '|'): -1,
                   (1j, '-'): 1j, (-1j, '-'): -1j,
                   (1, 'L'): 1j, (-1j, 'L'): -1,
                   (1j, 'J'): -1, (1, 'J'): -1j,
                   (-1, '7'): -1j, (1j, '7'): 1,
                   (-1j, 'F'): 1, (-1, 'F'): 1j
                   }

    best_distance = 0
    best_path = []
    actual_S = []
    for S in (1, -1, 1j, -1j): # Try all start directions of S
        curr_loc = S_loc
        stop = False
        dir_step = S
        this_path = [S_loc]
        while not stop:
            if not curr_loc + dir_step in locs:  # This was the wrong start of S
                stop = True
            elif locs[curr_loc + dir_step] == 'S':  # Back at S -> get info on how did we got here
                stop = True
                if len(this_path) > best_distance:
                    best_path = this_path
                    best_distance = len(this_path)
                    for bend in ('F', '7', 'L', 'J'):
                        if (dir_step, bend) not in dir_mapping:
                            pass
                        elif S == dir_mapping[(dir_step, bend)]:
                            actual_S = bend
            elif (dir_step, locs[curr_loc + dir_step]) not in dir_mapping:  # This was the wrong start of S
                stop = True
            else:  # Take another step, update direction, append to path
                curr_loc = curr_loc + dir_step
                dir_step = dir_mapping[(dir_step, locs[curr_loc])]
                this_path.append(curr_loc)

    # Count number inside by looking at how often you have to cross the loop to get to a location
    data[int(S_loc.real)] = data[int(S_loc.real)].replace('S', actual_S)
    count_in = 0
    for i in range(len(data)):
        row_count = 0
        last_bend = ''
        for k in range(len(data[i])):
            if i + k*1j in best_path:
                if data[i][k] == '|' or (data[i][k] == '7' and last_bend == 'L') or (data[i][k] == 'J' and last_bend == 'F'):
                    row_count += 1
                elif data[i][k] in ('J', 'F', '7', 'L'):
                    last_bend = data[i][k]
            elif row_count % 2 == 1:  # If you have stepped over the loop an odd amount of time, you are in
                count_in += 1

    result_part1 = int(best_distance / 2)
    result_part2 = count_in

    extra_out = {'Number of rows in input': len(data),
                 'Actual S shape': actual_S}

    return result_part1, result_part2, extra_out


if __name__ == "__main__":
    run_day(run_all, [1, 2, 3, 4, 5])
