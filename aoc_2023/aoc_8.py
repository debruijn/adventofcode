from typing import Union
from util.util import ProcessInput, run_day

debug = False


def run_all(example_run: Union[int, bool]):

    data = ProcessInput(example_run=example_run, day=8, year=2023).data

    steps = [1 if x == 'R' else 0 for x in data[0]]

    # Create mapping for where to go next based on current step
    mapping = {}
    for row in data[2:]:
        orig, dest = row.split(' = ')
        dest = dest.replace('(', '').replace(')', '').split(', ')
        mapping.update({orig: dest})

    # Part 1: start at AAA, and find ZZZ
    curr_pos = 'AAA'
    stop = False
    n_steps = 0
    while not stop:
        for step in steps:
            n_steps += 1
            curr_pos = mapping[curr_pos][step]
            if curr_pos == 'ZZZ':
                stop = True
    result_part1 = n_steps

    # Part 2: I don't assume that LCM can work (which can work just due to the specific input)
    # So for each start point ending in 'A', I find a loop in which it gets back at same point with same step-index
    # Then, I apply Chinese Remainder Theorem to check overlap between loops, and construct a new loop to compare with
    # the next until all have been taking into account.

    # So first, loop over all starting points and go through steps until we have a loop. Collect relevant info.
    try_pos = [x for x in mapping if x.endswith('A')]
    loop_info = []
    for curr_pos in try_pos:
        stop = False
        n_steps = 0
        history = []
        while not stop:
            for i, step in enumerate(steps):
                n_steps += 1
                if (curr_pos, i) in history:
                    loc_curr = history.index((curr_pos, i))
                    for j, hist in enumerate(history[loc_curr:]):
                        if hist[0].endswith('Z'):  # This works because there is only one Z in each loop
                            loop_info.append((loc_curr, len(history) - loc_curr, j))
                            break  # Info gathered: length to loop, loop length, length to Z
                    stop = True
                    break
                else:
                    history.append((curr_pos, i))
                curr_pos = mapping[curr_pos][step]

    def check(loop_info_other, x):
        # Utility function to check Chinese Remainder Theorem property
        return (x - loop_info_other[0]) % loop_info_other[1] == loop_info_other[2]

    # Aggregate loop info into when overlaps between loops happen -> this is a new loop. Iterate until all are joined.
    start = loop_info[0][0] + loop_info[0][2]
    step = loop_info[0][1]
    res = [start, start+step]
    for k in range(1, len(loop_info)):
        count = 0
        i = start
        while count < 2:
            if check(loop_info[k], i):
                res[count] = i
                count += 1
            i += step
        start = res[0]
        step = res[1] - res[0]

    result_part2 = res[0]

    extra_out = {'Number of steps in input': len(steps),
                 'Number of nodes in input': len(mapping),
                 'Number of nodes ending with an A': len(try_pos)}

    return result_part1, result_part2, extra_out


if __name__ == "__main__":
    run_day(run_all, [1, 2])
