from typing import Union

from aoc_2019.intcode_pc import IntCodePC
from util.util import ProcessInput, run_day

debug = False


def print_locs(locs):
    x_range = (int(min([x.real for x in locs])), int(max([x.real for x in locs])))
    y_range = (int(min([x.imag for x in locs])), int(max([x.imag for x in locs])))

    for y in range(y_range[0], y_range[1] + 1):
        curr_line = ""
        for x in range(x_range[0], x_range[1] + 1):
            curr_line += '#' if x + y * 1j in locs else " "
        print(curr_line)


def take_step(this_dir, prev_dir, data):
    this_pc = IntCodePC(data, input_val=list(prev_dir))
    this_pc.run_until_end()
    this_pc.add_input([this_dir])
    out = this_pc.run_until_end()[0]
    return out[-1]


def run_all(example_run: Union[int, bool]):
    data = ProcessInput(example_run=example_run, day=15, year=2019).as_list_of_ints(',').data[0]

    stop = False
    loc = 0 + 0j
    mapping = {1: 1j, 2: -1j, 3: -1, 4: 1, 0: 0}
    queue_locs = [(loc, tuple())]
    state_memory = {loc: tuple()}
    blockade_locs = []
    found_loc = None

    while not stop:
        curr_state = queue_locs.pop(0)
        for this_dir in [1, 2, 3, 4]:
            this_loc = curr_state[0] + mapping[this_dir]
            if this_loc not in blockade_locs:
                out = take_step(this_dir, curr_state[1], data)
                if out == 2:
                    if not found_loc:
                        found_loc = this_loc
                    if this_loc not in state_memory or len(curr_state[1]) < len(state_memory[curr_state[0]]):
                        state_memory[this_loc] = curr_state[1] + (this_dir,)
                elif out == 1:
                    if this_loc not in state_memory or len(curr_state[1]) < len(state_memory[curr_state[0]]):
                        state_memory[this_loc] = curr_state[1] + (this_dir,)
                        queue_locs.append([this_loc, tuple(curr_state[1] + (this_dir,))])
                else:
                    blockade_locs.append(this_loc)
        if len(queue_locs) == 0:
            stop = True  # Fallback option, should not be needed

    result_part1 = len(state_memory[found_loc])

    if debug:
        print_locs(state_memory.keys())
    oxygen = [found_loc]
    to_fill = [x for x in state_memory.keys() if x != found_loc]
    to_check = [found_loc]
    t = 0

    while len(to_fill) > 0:
        new_to_check = []
        for loc in to_check:
            for this_dir in [1, 2, 3, 4]:
                this_loc = loc + mapping[this_dir]
                if this_loc in to_fill and this_loc not in oxygen:
                    to_fill.remove(this_loc)
                    oxygen.append(this_loc)
                    new_to_check.append(this_loc)
        to_check = new_to_check
        t += 1

    result_part2 = t

    extra_out = {'Number of rows in input': len(data),
                 'Number of discovered reachable locs': len(state_memory),
                 'Number of discovered blockages': len(blockade_locs)}

    return result_part1, result_part2, extra_out


if __name__ == "__main__":
    run_day(run_all, [])
