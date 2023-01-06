from typing import Union
from util import timing

from aoc_15 import Datapoint


debug = False


# Reduce ranges down by incorporating overlap
def reduce_ranges(ranges):
    reduced_ranges = []
    for low, high in sorted(ranges):  # Sorting means we don't have to check low anymore.
        if reduced_ranges and reduced_ranges[-1][1] >= low - 1:
            reduced_ranges[-1][1] = max(reduced_ranges[-1][1], high)
        else:
            reduced_ranges.append([low, high])
    return reduced_ranges


def find_number_of_points_known_to_not_have_beacon(dps, beacons, target_row):

    # Get ranges of how each datapoint overlaps with the target row.
    # Reduce it down by combining overlapping ranges.
    # Take the sum of the elements of all combined ranges to see what is covered.
    ranges = get_ranges(target_row, dps, axis=1)
    sum_covered = sum([len(range(x[0], x[1] + 1)) for x in reduce_ranges(ranges)])

    # We also need to find the number of known beacons in this row, and substract that from the above.
    known_beacons = 0
    beacons_unique = set([tuple(x) for x in beacons])
    for bcn in beacons_unique:
        known_beacons = known_beacons + 1 if bcn[1] == target_row else known_beacons

    return sum_covered - known_beacons


# Get ranges of how each datapoint overlaps with this column or row
def get_ranges(x, dps, axis):
    ranges = []
    for dp in dps:
        if dp.sensor[axis] - dp.distance <= x <= dp.sensor[axis] + dp.distance:
            if debug:
                print(dp.sensor, dp.distance)
            remainder = dp.distance - abs(dp.sensor[axis] - x)
            ranges.append([dp.sensor[1-axis] - remainder, dp.sensor[1-axis] + remainder])
    return ranges


def find_distress_beacon(dps, range_len):

    # Loop over potential columns
    for x in range(range_len+1):

        # Get ranges of how each datapoint overlaps with this column; combine ranges where they overlap.
        ranges = get_ranges(x, dps, axis=0)
        reduced_ranges = reduce_ranges(ranges)

        # For each of the reduced ranges, look at the border of the range and see if that is in any other range.
        # If not, we have found our point.
        for i in range(len(reduced_ranges)):
            iter_range = reduced_ranges[i]
            low = not any([iter_range[0] - 1 in range(x[0], x[1] + 1) for x in reduced_ranges[i+1:]])
            if low:
                if 0 <= iter_range[0] - 1 <= range_len:
                    return x * 4000000 + iter_range[0] - 1
            high = not any([iter_range[1] + 1 in range(x[0], x[1] + 1) for x in reduced_ranges[i+1:]])
            if high:
                if 0 <= iter_range[1] + 1 <= range_len:
                    return x * 4000000 + iter_range[1] + 1


@timing
def run_all(example_run: Union[int, bool], target_row=10, range_len=20):

    file = f'aoc_15_exampledata{example_run}' if example_run else 'aoc_15_data'
    with open(file) as f:
        data = f.readlines()
    adj_data = [row.rstrip('\n') for row in data]

    dps = []
    beacons = []
    for row in adj_data:
        dp = Datapoint(row)
        beacons.append(dp.beacon)
        dps.append(dp)

    result_part1 = find_number_of_points_known_to_not_have_beacon(dps, beacons, target_row)

    print(f'Results for {f"example" if example_run else "my"} input{f" {example_run}" if example_run else ""}:')
    print(f' Result of part 1: {result_part1}')

    result_part2 = find_distress_beacon(dps, range_len=range_len)
    print(f' Result of part 2: {result_part2}')

    print(f'\nDescriptives: \n Number datapoints: {len(dps)} \n'
          f' Number known beacons: {len(set([tuple(dp.beacon) for dp in dps]))} \n')


if __name__ == "__main__":
    [run_all(example_run=i) for i in [1]]
    run_all(example_run=False, target_row=2000000, range_len=4000000)
