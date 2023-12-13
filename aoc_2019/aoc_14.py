from typing import Union
from util.util import ProcessInput, run_day
import math

debug = False


def run_all(example_run: Union[int, bool]):

    data = ProcessInput(example_run=example_run, day=14, year=2019).data

    # Processing: create mapping of product to its count and its ingredients
    mapping = {}
    for row in data:
        inp, out = row.split(' => ')
        count, out = out.split()
        inp = {x[1]: int(x[0]) for x in [x.split() for x in inp.split(',')]}
        mapping.update({out: (int(count), inp)})

    # Part 1: create hypothetical wallet with 1 Fuel and 0 of rest; swap it around until you only have OREs
    wallet = {key: 0 for key in list(mapping.keys()) + ['ORE']}
    wallet['FUEL'] = 1
    while not all([wallet[x] <= 0 for x in wallet if x != 'ORE']):
        for key in wallet.keys():
            if key != 'ORE':
                this_map = mapping[key]
                while wallet[key] > 0:
                    buy_count = math.ceil(wallet[key] / this_map[0])
                    wallet[key] -= this_map[0] * buy_count
                    for o_key, val in this_map[1].items():
                        wallet[o_key] += val * buy_count
    result_part1 = wallet['ORE']

    # Part 2: start at FUEL=target/result_part1, see how many OREs you need; adjust FUEL with wrong factor
    target = 1000000000000
    stop = False
    prev_fac = 1
    while not stop:
        wallet = {key: 0 for key in list(mapping.keys()) + ['ORE']}
        wallet['FUEL'] = int(target / result_part1) * prev_fac
        while not all([wallet[x] <= 0 for x in wallet if x != 'ORE']):
            for key in wallet.keys():
                if key != 'ORE':
                    this_map = mapping[key]
                    while wallet[key] > 0:
                        buy_count = math.ceil(wallet[key] / this_map[0])
                        wallet[key] -= this_map[0] * buy_count
                        for o_key, val in this_map[1].items():
                            wallet[o_key] += val * buy_count
        if wallet['ORE'] > target:
            stop = True
        else:
            prev_fac *= target / wallet['ORE']

    result_part2 = math.floor(target / result_part1 * prev_fac)

    extra_out = {'Number of recipies in input': len(data),
                 'Leftover items': {k: -v for k, v in wallet.items()
                                    if v < 0 and k not in ('ORE', 'FUEL')}}

    return result_part1, result_part2, extra_out


if __name__ == "__main__":
    run_day(run_all, [1, 2, 3, 4, 5])
