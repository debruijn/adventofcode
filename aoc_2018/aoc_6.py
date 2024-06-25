from typing import Union
from util.util import ProcessInput, run_day
from statistics import mean, median

debug = False


def run_all(example_run: Union[int, bool]):

    data = ProcessInput(example_run=example_run, day=6, year=2018).data
    data = [[x for x in row.split(', ')] for row in data]
    points = [int(x[0]) + int(x[1])*1j for x in data]
    extremes_real = (int(min(points, key=lambda x: x.real).real), int(max(points, key=lambda x: x.real).real) + 1)
    extremes_imag = (int(min(points, key=lambda x: x.imag).imag), int(max(points, key=lambda x: x.imag).imag) + 1)

    # Part 1: two phases, identify infinite points, and then find largest among the remaining points
    #   Identify infinite points: go over the border of the square defined by the points, and find which one is closest
    #   Find largest among remaining: keep expanding region around point until no new points closest to this point

    # Function to find nearest points along one border of a square -> add those points to `infinite_points`
    def check_border(extreme_along, extreme_for, along_real=True):
        for x in range(*extreme_along):
            pt = x * (1 if along_real else 1j) + extreme_for * (1j if along_real else 1)
            min_dist = 1000000000000
            curr_min = -1
            for point in points:
                this_dist = abs(point.imag - pt.imag) + abs(point.real - pt.real)
                if this_dist < min_dist:
                    min_dist = this_dist
                    curr_min = point
                elif this_dist == min_dist:  # In case of ties: don't count it towards any point
                    curr_min = -1
            if curr_min != -1 and curr_min not in infinite_points:
                infinite_points.append(curr_min)

    infinite_points = []
    check_border(extremes_real, extremes_imag[0])
    check_border(extremes_real, extremes_imag[1] - 1)
    check_border(extremes_imag, extremes_real[0], along_real=False)
    check_border(extremes_imag, extremes_real[1] - 1, along_real=False)

    # For non-infinite points, go one wider from their point until you don't gain 1 anymore
    candidate_points = [x for x in points if x not in infinite_points]
    point_counts = {}

    def get_dist_shift(dist):

        # 2 -> 2, 1+1j, 2j, -1+1j, -2, -1-1j, -2j, 1-1j
        shifts = []
        shifts.extend([x + (dist - x) * 1j for x in range(dist + 1)])
        shifts.extend([x - (dist - x) * 1j for x in range(dist + 1)])
        shifts.extend([-x + (dist - x) * 1j for x in range(dist + 1)])
        shifts.extend([-x - (dist - x) * 1j for x in range(dist + 1)])

        return list(set(shifts))

    for pt in candidate_points:
        this_count = 1
        this_dist = 0
        curr_count = 1
        stop = False
        while not stop:
            this_dist += 1
            points_at_dist = [pt + x for x in get_dist_shift(this_dist)]
            for check_pt in points_at_dist:
                this_closest = True
                for other_pt in [x for x in points if x != pt]:
                    if (abs(check_pt.imag - pt.imag) + abs(check_pt.real - pt.real) >=
                            abs(check_pt.imag - other_pt.imag) + abs(check_pt.real - other_pt.real)):
                        this_closest = False
                        break
                if this_closest:
                    curr_count += 1
            if curr_count == this_count:
                stop = True
            else:
                this_count = curr_count
                if debug:
                    print(f'For point {pt}, now at distance {this_dist} with currently {this_count} numbers.')

        point_counts[pt] = this_count

    result_part1 = max(point_counts.values())

    # Part 2: start in the middle (which I had tested) or better in the update: start at the median.
    # Then keep expanding the region to consider to be 1 wider until that doesn't lead to new valid points in the region
    # Better version: make a queue of those "bordering the ones in the region but not yet checked themselves" to avoid
    #   checking in a direction that is already outside the region but at the same distance of 'start' as another
    #   direction that still has points in the region

    # OLD: start = int(round(mean(extremes_real))) + int(round(mean(extremes_imag))) * 1j
    start = int(median([x.real for x in points])) + int(median([x.imag for x in points])) * 1j
    this_count = 1
    this_dist = 0
    curr_count = 1
    stop = False
    while not stop:
        this_dist += 1
        points_at_dist = [start + x for x in get_dist_shift(this_dist)]
        for check_pt in points_at_dist:
            total_dist = sum([abs(check_pt.imag - x.imag) + abs(check_pt.real - x.real) for x in points])
            if total_dist < (32 if example_run else 10000):
                curr_count += 1
        if curr_count == this_count:
            stop = True
        else:
            this_count = curr_count
            if debug:
                print(f'For finding the region, now at distance {this_dist} with currently {this_count} numbers.')

    result_part2 = curr_count

    extra_out = {'Number of points in input': len(data),
                 'Size of region covered by points':
                     f'{extremes_real[1] - extremes_real[0]} x {extremes_imag[1] - extremes_imag[0]}'}

    return result_part1, result_part2, extra_out


if __name__ == "__main__":
    run_day(run_all, [1])
