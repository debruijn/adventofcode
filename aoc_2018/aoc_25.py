from typing import Union
from util.util import ProcessInput, run_day


def within_distance(point, constellation):  # Can a point connect with this constellation?
    return any([sum(abs(point[j] - other[j]) for j in (0, 1, 2, 3)) <= 3 for other in constellation])


def run_all(example_run: Union[int, bool]):

    data = ProcessInput(example_run=example_run, day=25, year=2018).remove_substrings([" "]).as_list_of_ints(',').data
    universe = []  # Keep track of all constellations
    for point in data:
        checks = [i for i in range(len(universe)) if within_distance(point, universe[i])]  # Indices that it can join
        if len(checks) == 0:  # If point can't connect to any existing constellation: create a new one
            universe.append([point])
        else:  # If it can connect to any: join it to the first, and connect any others (if there) to that one as well
            universe[checks[0]].append(point)
            other_checks = checks[1:]
            other_checks.reverse()  # Reverse order such that popping it doesn't impact indices of future pop's
            for other_check in other_checks:
                universe[checks[0]].extend(universe.pop(other_check))

    result_part1 = len(universe)
    result_part2 = "Merry Christmas!"

    extra_out = {'Number of points in input': len(data)}

    return result_part1, result_part2, extra_out


if __name__ == "__main__":
    run_day(run_all, [1, 2, 3, 4])
