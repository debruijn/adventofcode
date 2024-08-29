from typing import Union
from util.util import ProcessInput, run_day

# Potential speed-ups (which are really not needed in this case):
# - for disc with highest n_pos, loop only over the possible positions. So:
#   - start not at t=0 but at the first option that would pass through that disc
#   - increase t not by 1 but by that disc's n_pos
# - this could repeated for next highest n_pos -> find when the above procedure goes through that disc, and use that to
#   make the jump bigger (will require checking whether these two n_pos's have a common divisor or not)


def pass_disc(t, info):  # Structured to be "cachable" but turns out maintaining the cache is slower
    n_pos, start_pos, loc = info
    return (start_pos + t + loc) % n_pos == 0


def get_capsule(all_info, additional_disc=False):
    if additional_disc:
        all_info.append((11, 0, all_info[-1][2]+1, ))  # Part 2
    t = 0
    while not all(pass_disc(t % x[0], x) for x in all_info):
        t += 1
    return t


def run_all(example_run: Union[int, bool]):
    data = ProcessInput(example_run=example_run, day=15, year=2016).data

    # Process input lazily into tuples with information per disc
    all_info = []
    for row in data:
        loc = int(row.split()[1][1:])
        n_pos = int(row.split()[3])
        start_pos = int(row.split()[-1][:-1])
        all_info.append((n_pos, start_pos, loc))

    result_part1 = get_capsule(all_info)
    result_part2 = get_capsule(all_info, additional_disc=True)

    extra_out = {'Number of discs in input': len(data)}

    return result_part1, result_part2, extra_out


if __name__ == "__main__":
    run_day(run_all, [1])
