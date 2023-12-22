from itertools import product
from typing import Union
from util.util import ProcessInput, run_day

debug = False


# Now runs in 41.5 sec by ignoring bricks below the one being removed. Still too slow but IDGAF today.
# To speed up:  keep a running track of each highest Z at every X,Y, and compare new bricks to that.
#               Then you immediately know how much the new brick would drop.
#               You can use the footprint (e.g. X,Y) of the new brick to update the highest Z.
# Thanks for reading :)


def is_conflict_with_settled(settled, low_brick):
    if len(settled) == 0:
        return False
    for el in product(range(low_brick[0][0], low_brick[1][0]+1), range(low_brick[0][1], low_brick[1][1]+1)):
        el = el + (min(low_brick[0][2], low_brick[1][2]),)
        for brick in settled:
            if brick[0][0] <= el[0] <= brick[1][0] and brick[0][1] <= el[1] <= brick[1][1] and brick[0][2] <= el[2] <= brick[1][2]:
                return True
    return False


def settle_bricks(bricks, skip_below=0):
    # One by one, settle down and create list of settled down bricks
    settled = []
    this_safe = True
    for brick in bricks:
        curr_loc = [brick[0].copy(), brick[1].copy()]
        if brick[0][2] > skip_below:
            stop = False
            while not stop:
                low_brick = [curr_loc[0].copy(), curr_loc[1].copy()]
                low_brick[0][2] -= 1
                low_brick[1][2] -= 1
                if low_brick[0][2] > 0 and low_brick[1][2] > 0 and not is_conflict_with_settled(settled, low_brick):
                    curr_loc = low_brick
                    this_safe = False
                else:
                    stop = True
        settled.append(curr_loc)
    return settled, this_safe


def run_all(example_run: Union[int, bool]):

    data = ProcessInput(example_run=example_run, day=22, year=2023).data

    # Get bricks and sort by lowest z coordinate
    bricks = [[[int(x) for x in y.split(',')] for y in row.split('~')] for row in data]
    bricks = sorted(bricks, key=lambda x: min(x[0][2], x[1][2]))

    impact = {}
    count_safe = 0
    settled, _ = settle_bricks(bricks)  # Initial settle-down
    for i, brick in enumerate(settled):
        if i % 100 == 0 and i>0:
            print(f'{i}/{len(settled)}: removing {brick}')
        this_settled = settled.copy()
        this_settled.remove(brick)
        impact[i] = 0
        new_settled, this_safe = settle_bricks(this_settled, skip_below=brick[1][2])
        if this_safe:
            count_safe += 1
        for j, o_brick in enumerate(this_settled):
            if o_brick != new_settled[j]:
                impact[i] += 1

    result_part1 = count_safe
    result_part2 = sum(impact.values())

    extra_out = {'Number of bricks in input': len(data),
                 'Original max height': bricks[-1][1][2],
                 'Settled max height': settled[-1][1][2]}

    return result_part1, result_part2, extra_out


if __name__ == "__main__":
    run_day(run_all, [1])
