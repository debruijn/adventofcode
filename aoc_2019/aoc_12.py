from typing import Union
from util.util import ProcessInput, run_day
from math import lcm


debug = False


def run_all(example_run: Union[int, bool]):

    data = ProcessInput(example_run=example_run, day=12, year=2019).data
    T = 10 if example_run == 1 else 100 if example_run == 2 else 1000

    moons_loc = [[int(x) for x in row.replace('<x=', '').replace(' y=', '').replace(' z=', '').replace('>', '').split(',')]
                for row in data]
    moons_velo = [[0]*3 for _ in moons_loc]

    t = 0
    hists = [{}, {}, {}]
    loop_size = [None, None, None]  # I had loop_start as well, but turns out LCM works again, no CRT needed
    while any([x is None for x in loop_size]):
        # States of each dim:
        for dim in range(3):
            if loop_size[dim] is None:
                locs = tuple([x[dim] for x in moons_loc])
                velo = tuple([x[dim] for x in moons_velo])
                state = (locs, velo)
                if state in hists[dim].keys():
                    loop_size[dim] = t - hists[dim][state]
                else:
                    hists[dim].update({state: t})

                # Apply gravity: for each dim, if loc is bigger decrease, if loc is lower increase (net)
                for i, moon in enumerate(moons_loc):  # do it with product, update both
                    for j, o_moon in enumerate(moons_loc):
                        if moon[dim] > o_moon[dim]:
                            moons_velo[i][dim] += -1
                        elif moon[dim] < o_moon[dim]:
                            moons_velo[i][dim] += 1

                # Update position
                for i, moon in enumerate(moons_velo):
                    moons_loc[i][dim] += moon[dim]
        t += 1

    t_part1 = [T % loop_size[dim] for dim in range(3)]
    states_part1 = [[x for x in hists[dim] if hists[dim][x] == t_part1[dim]][0] for dim in range(3)]

    pot_energy = [sum([abs(states_part1[i][0][j]) for i in range(3)]) for j in range(len(moons_loc))]
    kin_energy = [sum([abs(states_part1[i][1][j]) for i in range(3)]) for j in range(len(moons_loc))]
    tot_energy = sum([pot_energy[i] * kin_energy[i] for i in range(len(moons_loc))])

    result_part1 = tot_energy
    result_part2 = lcm(loop_size[0], loop_size[1], loop_size[2])

    extra_out = {'Number of moons in input': len(data),
                 'T for part 1': T,
                 'Cycle lengths for each dimension': loop_size}

    return result_part1, result_part2, extra_out


if __name__ == "__main__":
    run_day(run_all, [1, 2])
