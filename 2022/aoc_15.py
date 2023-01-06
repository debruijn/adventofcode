import numpy as np
from typing import Union
from util import timing


debug = False


def manhattan_distance(x, y):
    return abs(x[0] - y[0]) + abs(x[1] - y[1])


class Datapoint:

    def __init__(self, text):
        text = text.replace('Sensor at ', '').replace(' closest beacon is at ', '').split(':')
        self.sensor = [int(x[2:]) for x in text[0].split(', ')]
        self.beacon = [int(x[2:]) for x in text[1].split(', ')]
        self.distance = manhattan_distance(self.sensor, self.beacon)

    def is_beacon(self, point):
        return point == self.beacon

    def compare(self, point):
        return manhattan_distance(self.sensor, point) <= self.distance


def find_number_of_points_known_to_not_have_beacon(dps, beacons, target_row):

    y_range = np.array(beacons)[:, 1].max() - np.array(beacons)[:, 1].min() + 1
    x_min = np.array(beacons)[:, 0].min()
    x_max = np.array(beacons)[:, 0].max()

    target_min = int(x_min - y_range/2)
    target_max = int(x_max + y_range/2)

    if debug:
        print(f'Minimum and maximum value of x: {x_min}, {x_max} (diff: {x_max - x_min}), number of sensors: {len(dps)}')

    points_non_existance = 0
    for x_loc in range(target_min-1000, target_max+1001):
        point = [x_loc, target_row]
        if any([dp.is_beacon(point) for dp in dps]):
            pass
        elif any([dp.compare(point) for dp in dps]):
            points_non_existance += 1

    return points_non_existance


def find_distress_beacon(dps, range_len):

    # Loop over potential columns
    for x in range(range_len+1):

        # For all sensors, find ranges of how they overlap with this column.
        # For each range, only check the values just outside each range to see if they fit in another range.
        # If not, that is the location for the answer.

        ranges = []
        for dp in dps:
            if dp.sensor[0] - dp.distance <= x <= dp.sensor[0] + dp.distance:
                if debug:
                    print(dp.sensor, dp.distance)
                remainder = dp.distance - abs(dp.sensor[0] - x)
                ranges.append([dp.sensor[1] - remainder, dp.sensor[1] + remainder])

        for iter_range in ranges[1:]:  # can skip one
            low = not any([iter_range[0] - 1 in range(x[0], x[1] + 1) for x in ranges])
            if low:
                if 0 <= iter_range[0] - 1 <= range_len:
                    return x * 4000000 + iter_range[0] - 1
            high = not any([iter_range[1] + 1 in range(x[0], x[1] + 1) for x in ranges])
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
    result_part2 = find_distress_beacon(dps, range_len=range_len)

    print(f'Results for {f"example" if example_run else "my"} input{f" {example_run}" if example_run else ""}:')
    print(f' Result of part 1: {result_part1}')
    print(f' Result of part 2: {result_part2}')

    print(f'\nDescriptives: \n Number datapoints: {len(dps)} \n'
          f' Number known beacons: {len(set([tuple(dp.beacon) for dp in dps]))} \n')


if __name__ == "__main__":
    [run_all(example_run=i) for i in [1]]
    run_all(example_run=False, target_row=2000000, range_len=4000000)
