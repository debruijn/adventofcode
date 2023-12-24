from itertools import combinations
from typing import Union
from util.util import ProcessInput, run_day
import z3


debug = False


def run_all(example_run: Union[int, bool]):

    data = ProcessInput(example_run=example_run, day=24, year=2023).data

    # Process data: convert rows to points/speeds for part 2, and to formulas for part 1
    check_range = (7, 27) if example_run else (200000000000000, 400000000000000)
    point_info = []
    points = []
    speeds = []
    for row in data:
        pt, speed = row.split(' @ ')
        pt = [int(x) for x in pt.split(', ')]
        speed = [int(x) for x in speed.split(', ')]
        points.append(pt)
        speeds.append(speed)
        a = pt[1] - pt[0] * speed[1] / speed[0]
        b = speed[1] / speed[0]
        # formula = lambda x, a, b: a + b * x  # removed, directly use a/b instead
        point_info.append((pt, speed, a, b))

    # Part 1: loop over all combinations, find intersection and check if it is in the range and happens after t=0
    count_inside = 0
    for f, g in combinations(point_info, 2):
        if not f[3] == g[3]:
            x_cross = (g[2] - f[2]) / (f[3] - g[3])
            y_cross = f[2] + f[3] * x_cross
            t_f = (x_cross - f[0][0]) / f[1][0]
            t_g = (x_cross - g[0][0]) / g[1][0]
            if (t_f >= 0 and t_g >= 0 and check_range[0] <= x_cross <= check_range[1] and
                    check_range[0] <= y_cross <= check_range[1]):
                count_inside +=1
    result_part1 = count_inside

    # Part 2: solve using z3 again :)
    s = z3.Solver()
    rock_loc = z3.RealVector('rock_loc', 3)
    rock_spd = z3.RealVector('rock_speed', 3)
    time = z3.RealVector('time', 3)  # That 3 points are enough is implied by the text -> all will be on line
    for i, t in enumerate(time):
        [s.add(rock_loc[dim] + rock_spd[dim] * t == points[i][dim] + speeds[i][dim] * t) for dim in range(3)]
    s.check()

    result_part2 = s.model().eval(sum(rock_loc))

    extra_out = {'Number of hailstones in input': len(data)}

    return result_part1, result_part2, extra_out


if __name__ == "__main__":
    run_day(run_all, [1])
