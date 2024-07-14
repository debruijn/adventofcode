from typing import Union
from util.util import ProcessInput, run_day
import z3


def z3_abs(x):
    return z3.If(x >= 0, x, -x)


def run_all(example_run: Union[int, bool]):
    data = ProcessInput(example_run=example_run, day=23, year=2018).data

    # Processing raw into bots with location and radius. Identifying bot with the largest radius/range.
    bots = []
    big_boy = -1
    for row in data:
        loc, radius = row.split(', ')
        loc = [int(x) for x in loc[loc.find('<') + 1:loc.find('>')].split(',')]
        radius = int(radius.split('=')[1])
        if radius > (bots[big_boy][1] if big_boy >= 0 else 0):
            big_boy = len(bots)  # The current length is what will be the index of this bot after appending
        bots.append((loc, radius))

    # Part 1: with utility function in_range, directly count how many bots meet that requirement for the big_boy.
    def in_range(loc1, loc2, radius):
        return abs(loc1[0] - loc2[0]) + abs(loc1[1] - loc2[1]) + abs(loc1[2] - loc2[2]) <= radius

    count_in_range = 0
    for bot in bots:
        count_in_range += in_range(bot[0], bots[big_boy][0], bots[big_boy][1])

    result_part1 = count_in_range

    # Part 2: use z3 again, like in 2022!
    x, y, z = z3.Int('x'), z3.Int('y'), z3.Int('z')  # The locations of the final solution
    in_ranges = [z3.Int('in_range_' + str(i)) for i in range(len(bots))]  # Each bot radius
    opt = z3.Optimize()
    for i, bot in enumerate(bots):
        opt.add(in_ranges[i] == z3.If(z3_abs(x - bot[0][0]) + z3_abs(y - bot[0][1]) + z3_abs(z - bot[0][2]) <= bot[1],
                                      1, 0))  # If (x, y, z) within radius, this bot-restriction is 1; else 0

    # The number of bots that pass the restriction (e.g. that can see the current candidate point)
    range_count = z3.Int('count_in_range')
    opt.add(range_count == sum(in_ranges))

    # Utility variable for finding point with the lowest distance to origin (0, 0, 0)
    distance_origin = z3.Int('origin_distance')
    opt.add(distance_origin == z3_abs(x) + z3_abs(y) + z3_abs(z))

    # Primary target: maximize number of bots in range. Secondary target: minimize distance from point to origin.
    h1 = opt.maximize(range_count)
    h2 = opt.minimize(distance_origin)
    if not opt.check() == z3.sat:
        raise AssertionError('No solution found')

    result_part2 = opt.lower(h2)

    extra_out = {'Number of bots': len(data),
                 'Number of bots in range of final solution': opt.upper(h1)}

    return result_part1, result_part2, extra_out


if __name__ == "__main__":
    run_day(run_all, [1])
