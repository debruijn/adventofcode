from typing import Union
from util import timing
import z3 as z3

from aoc_15_alt import find_number_of_points_known_to_not_have_beacon, Datapoint

debug = False


def z3_abs(x):
    return z3.If(x >= 0, x, -x)


def find_distress_beacon(dps, range_len):

    # Initialize solver and variables
    s = z3.Solver()
    x, y = z3.Ints("x y")

    # Add restrictions
    s.add(x >= 0, x <= range_len, y >= 0, y <= range_len)
    for dp in dps:
        s.add(z3_abs(dp.sensor[0] - x) + z3_abs(dp.sensor[1] - y) > dp.distance)

    # Check restrictions and run model
    assert s.check() == z3.sat
    model = s.model()

    if debug:
        for d in model.decls():
            print("%s = %s" % (d.name(), model[d]))

    return model[x].as_long() * range_len + model[y].as_long()


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
