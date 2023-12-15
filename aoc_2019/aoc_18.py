from itertools import combinations
from typing import Union
from util.util import ProcessInput, run_day

debug = False

ord_offset = ord('a') - ord('A')
all_dirs = [1, -1, 1j, -1j]


def get_shortest_path_with_hist(start, end, free, keys, doors):
    # Shortest path from start to end, while collecting other keys/doors on the way
    visited = {start: (0, [], [])}  # Structure: loc => (distance, keys, doors)
    queue = [start]

    while len(queue) > 0:
        curr_state = queue.pop(0)
        this_hist = ((visited[curr_state][1]).copy(), (visited[curr_state][2]).copy())
        for k, v in keys.items():
            if v == curr_state:
                this_hist[0].append(k)
        for k, v in doors.items():
            if v == curr_state:
                this_hist[1].append(k)
        for this_dir in all_dirs:
            this_loc = curr_state + this_dir
            if this_loc == end:
                [this_hist[0].remove(k) for k,v in keys.items() if v==start]
                return visited[curr_state][0] + 1, this_hist[0], this_hist[1]
            if this_loc not in visited and this_loc in free:
                queue.append(this_loc)
                visited.update({this_loc: (visited[curr_state][0] + 1, this_hist[0], this_hist[1])})
    return -1, [], []


def get_all_paths(keys, free, doors, start):
    # Collect all paths from starting points to keys and from keys to each other
    if type(start) in (int, complex):
        start = [start]
    elif type(start) is tuple:
        start = list(start)

    free = tuple(free + start + [x for x in doors.values()] + [x for x in keys.values()])  # Can pass through doors/keys/start

    all_lengths = {}
    print("Getting all unobstructed paths...")
    for s in start:
        for j in keys:
            all_lengths[(s, keys[j])] = get_shortest_path_with_hist(s, keys[j], free, keys, doors)
    print("   ... from start to all keys: done!")
    for i, j in combinations(keys, 2):
        all_lengths[(keys[i], keys[j])] = get_shortest_path_with_hist(keys[i], keys[j], free, keys, doors)
        all_lengths[(keys[j], keys[i])] = all_lengths[(keys[i], keys[j])]
    print("   ... from each key to every other key: done!")

    return all_lengths


def get_locations(data):
    # Collect interesting locations in data: keys, doors, starting point, free spaces
    keys = {}
    doors = {}
    start = 0
    free = []
    for i, row in enumerate(data):
        for j, el in enumerate(row):
            if el == "@":
                start = i + j*1j
            elif el == "#":
                pass  # Used to collect blocked positions instead of free:  blocked.append(i + j*1j)
            elif el == '.':
                free.append(i + j*1j)
            else:
                if 65 <= ord(el) <= 90:
                    doors.update({chr(ord(el)+ord_offset): i+j*1j})
                else:
                    keys.update({el: i + j * 1j})
    target = [x for x in keys.keys() if x not in doors.keys()]

    return keys, doors, start, target, free


def get_keys_to_do(num, rev_key_ids):
    # Convert binary number to which keys still have to be collected
    bin_num = format(num, 'b')
    keys = []
    for i in range(len(bin_num)):
        if bin_num[len(bin_num) - i - 1] == '1':
            keys.append(rev_key_ids[i])
    return tuple(keys)


def is_superior(num1, num2):
    # Based on two binary numbers, check if all 1s in num2 are also in num1
    if num2 >= num1:
        return False
    bin_num1 = format(num1, 'b')
    bin_num2 = format(num2, 'b')
    for i in range(len(bin_num2)):
        if bin_num2[len(bin_num2) - i - 1] == '1':
            if bin_num1[len(bin_num1) - i - 1] == '0':
                return False
    return True


def compare_past_states(new_state, past_states):
    # Check if new state is possibly better than previous state:
    # - If the loc and opened keys already exist, it is only better if distance is lower
    # - If loc/keys don't exist yet, compare with other past_states to find one superior in keys but lower in distance
    if (new_state[0], new_state[2]) not in past_states:
        none_superior = True
        for key in past_states.keys():
            if key[0] == new_state[0]:
                if is_superior(key[1], new_state[2]) and past_states[key] < new_state[1]:
                    none_superior = False
        if none_superior:
            return True
    else:
        if past_states[(new_state[0], new_state[2])] > new_state[1]:
            return True
    return False


def get_quadrant_of_key(all_lengths, curr_state, key_loc):
    # Which of the current state values can reach the key in key_loc?
    for i in range(len(curr_state[0])):
        if all_lengths[(curr_state[0][i], key_loc)][0] >= 0:
            return i


def find_best_order(all_lengths, starts, keys, all_keys, key_ids, rev_key_ids):
    # Initializing the algorithm
    curr_loc = starts
    curr_dist = 0
    curr_keys = 0
    queue = [(curr_loc, curr_dist, curr_keys)]
    past_states = {}
    best_distance = len(keys) * max([x[0] for x in all_lengths.values()])  # Worst-case: every step is max distance

    print("Going over all possible routes...")
    while len(queue) > 0:
        curr_state = queue.pop()
        if curr_state[2] == all_keys:
            if debug:
                print(f"Found solution: {curr_state[1]}")
            if curr_state[1] < best_distance:
                best_distance = curr_state[1]
        elif curr_state[1] < best_distance:
            keys_to_do = get_keys_to_do(all_keys - curr_state[2], rev_key_ids)
            for key in keys_to_do:
                q = get_quadrant_of_key(all_lengths, curr_state, keys[key])
                if not any([x in all_lengths[(curr_state[0][q], keys[key])][2] +
                            all_lengths[(curr_state[0][q], keys[key])][1]
                            for x in keys_to_do]):
                    key_dist = all_lengths[(curr_state[0][q], keys[key])][0]
                    if key_dist >= 0:
                        new_locs = list(curr_state[0])
                        new_locs[q] = keys[key]
                        new_state = (tuple(new_locs), curr_state[1] + key_dist, curr_state[2] + 2 ** key_ids[key])
                        if compare_past_states(new_state, past_states):
                            queue.append(new_state)
                            past_states.update({(new_state[0], new_state[2]): new_state[1]})

    return best_distance

def run_all(example_run: Union[int, bool]):

    data = ProcessInput(example_run=example_run, day=18, year=2019).data
    if debug:
        [print(row) for row in data]

    # Processing data
    keys, doors, start, target, free = get_locations(data)
    key_ids = {key: i for i, key in enumerate(keys.keys())}
    rev_key_ids = {i: key for i, key in enumerate(keys.keys())}
    all_keys = 2 ** len(key_ids) - 1  # Binary representation of getting all keys
    starts = (start,)

    # Part 1: getting all unobstructed paths, and then finding the best order of keys - only considering possible keys
    print('\nRunning algorithm for part 1: across the entire grid\n')
    all_lengths = get_all_paths(keys, free, doors, starts)
    result_part1 = find_best_order(all_lengths, starts, keys, all_keys, key_ids, rev_key_ids)

    if not example_run:
        # Part 2 additional processing
        starts = tuple([start + i + j for i,j in combinations(all_dirs,2) if start + i + j != start])
        for i_dir in all_dirs:
            free.remove(start + i_dir)

        # Part 2: same but per quadrant: less routes but more info to track
        print('\n\nRunning algorithm for part 2: per quadrant\n')
        all_lengths = get_all_paths(keys, free, doors, starts)
        result_part2 = find_best_order(all_lengths, starts, keys, all_keys, key_ids, rev_key_ids)
    else:
        result_part2 = "N/A"

    extra_out = {'Dimension of input': (len(data), len(data[0])),
                 'Number of keys': len(keys)}

    return result_part1, result_part2, extra_out


if __name__ == "__main__":
    run_day(run_all, [1, 2, 3, 4, 5])
    # run_day(run_all, [])  # <30s to <13s if skipping the examples
