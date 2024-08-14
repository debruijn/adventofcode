from typing import Union
from util.util import ProcessInput, run_day


def run_all(example_run: Union[int, bool]):

    data = ProcessInput(example_run=example_run, day=25, year=2017).as_list_of_strings_per_block().data

    # Initialize state, loc, and required number of steps
    curr_state = data[0][0].split(' ')[-1].replace('.', '')
    nr_steps = int(data[0][1].split(' ')[-2])
    curr_loc = 0

    # Process how the states link up together -> dict with key the statenames and value two tuples for what happens if
    # the current location is 0 or 1 (each tuple: new value; how to update location; new state)
    states = {}
    for state in data[1:]:
        state_name = state[0].split()[-1].replace(':', '')
        if_0 = (1 if state[2].endswith('1.') else 0, 1 if state[3].endswith('right.') else -1, state[4][-2])
        if_1 = (1 if state[6].endswith('1.') else 0, 1 if state[7].endswith('right.') else -1, state[8][-2])
        states[state_name] = (if_0, if_1)

    # Approach chosen: use a set to contain which locations are active (=1) or not (=0)
    # Alternatives considered: deque or defaultdict to collect 0s and 1s -> might become big, and defaultdict is slower
    # Alternatively: deduce what happens with these input states, it is bound to predictable. That would be the backup
    # option in case the set implementation was not fast enough (but it is).
    active = set()
    for _ in range(nr_steps):
        if curr_loc in active:
            this = states[curr_state][1]
            if this[0] == 0:  # No need to do anything is this[0]==1 and curr_loc is already in active
                active.remove(curr_loc)
        else:
            this = states[curr_state][0]
            if this[0] == 1:  # No need to do anything is this[0]==0 and curr_loc is already not in active
                active.add(curr_loc)
        curr_loc += this[1]
        curr_state = this[2]

    result_part1 = len(active)
    result_part2 = "Merry Christmas!"

    extra_out = {'Number of states in input': len(data),
                 'Number of steps required': nr_steps}

    return result_part1, result_part2, extra_out


if __name__ == "__main__":
    run_day(run_all, [1])
