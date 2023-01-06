import numpy as np
import z3
import functools
import itertools
from typing import Union
from util import timing
import tqdm


debug = False


def check_loc(loc, shape, chamber):
    locs_to_check = np.array(loc) + np.array(shape)
    if max(locs_to_check[:, 0]) >= chamber.shape[0]:
        return False
    if min(locs_to_check[:, 0]) < 0:
        return False
    return not chamber[locs_to_check[:, 0], locs_to_check[:, 1]].any()


def set_loc(loc, shape, chamber, val=1):
    locs_to_set = np.array(loc) + np.array(shape)
    chamber[locs_to_set[:, 0], locs_to_set[:, 1]] = val
    return chamber


def part1(chamber_width, rock_types, wind, wind_r, wind_l, fall, nr_rocks=2022):
    # nr_rocks = 1000000000000
    chamber = np.zeros([chamber_width, 3 * nr_rocks])  # chamber = np.ones([chamber_width, 1])
    chamber[:, 0] = 1
    curr_rock_type = 0
    wind_ind = 0
    for r in tqdm.trange(nr_rocks):
        # extend chamber if needed (if size is done dynamically)

        # get new rock from rocktype
        rock_shape = rock_types[curr_rock_type]
        curr_rock_type = curr_rock_type + 1 if curr_rock_type + 1 < len(rock_types) else 0

        # find starting loc compared to chamber
        rock_loc = (2, np.where(chamber.any(axis=0))[0].max() + 4)

        # while rock has not stopped, iterate between:
        #   check and move to right/left, if possible
        #   check and move down fall -> if not, stop
        moving = True
        while moving:
            iter_wind = wind[wind_ind]
            wind_ind = wind_ind + 1 if wind_ind + 1 < len(wind) else 0

            if iter_wind == '>':
                if check_loc(rock_loc + wind_r, rock_shape, chamber):
                    rock_loc = rock_loc + wind_r
            else:
                if check_loc(rock_loc + wind_l, rock_shape, chamber):  # Can change to reduce wind_r
                    rock_loc = rock_loc + wind_l
            if debug:
                print(set_loc(rock_loc, rock_shape, chamber.copy(), val=2)[:3 * r + 7, :])

            if check_loc(rock_loc + fall, rock_shape, chamber):  # Can change to reduce wind_r
                rock_loc = rock_loc + fall
            else:
                moving = False
                chamber = set_loc(rock_loc, rock_shape, chamber)
            if debug:
                print(set_loc(rock_loc, rock_shape, chamber.copy(), val=2)[:3 * r + 7, :])
        if debug:
            print(chamber[:3 * r + 7, :])

    result_part1 = np.where(chamber.any(axis=0))[0].max()

    return result_part1


def skyline(chamber):
    init_skyline = [np.where(chamber[i,:])[0].max() for i in range(chamber.shape[0])]
    norm_skyline = tuple([max(init_skyline) - i for i in init_skyline])
    return norm_skyline


def part2(chamber_width, rock_types, wind, wind_r, wind_l, fall, nr_rocks=1000000000000):

    states = set()
    init_nr_rocks = 5000
    chamber = np.zeros([chamber_width, 3 * init_nr_rocks])  # chamber = np.ones([chamber_width, 1])
    chamber[:, 0] = 1
    curr_rock_type = 0
    wind_ind = 0
    r = 0
    all_states_unique = True
    first_encounter = 0
    first_height = 0

    while all_states_unique:

        this_state = (curr_rock_type, wind_ind, skyline(chamber))
        if this_state in states:
            if first_encounter > 0:
                break
            else:
                first_encounter = r
                first_height = np.where(chamber.any(axis=0))[0].max()
                states = set()  # Reset states to keep track of second time you find it
        states.add(this_state)

        # get new rock from rocktype
        rock_shape = rock_types[curr_rock_type]
        curr_rock_type = curr_rock_type + 1 if curr_rock_type + 1 < len(rock_types) else 0

        # find starting loc compared to chamber
        rock_loc = (2, np.where(chamber.any(axis=0))[0].max() + 4)

        # while rock has not stopped, iterate between:
        #   check and move to right/left, if possible
        #   check and move down fall -> if not, stop
        moving = True
        while moving:
            iter_wind = wind[wind_ind]
            wind_ind = wind_ind + 1 if wind_ind + 1 < len(wind) else 0

            if iter_wind == '>':
                if check_loc(rock_loc + wind_r, rock_shape, chamber):
                    rock_loc = rock_loc + wind_r
            else:
                if check_loc(rock_loc + wind_l, rock_shape, chamber):  # Can change to reduce wind_r
                    rock_loc = rock_loc + wind_l
            if debug:
                print(set_loc(rock_loc, rock_shape, chamber.copy(), val=2)[:3 * r + 7, :])

            if check_loc(rock_loc + fall, rock_shape, chamber):  # Can change to reduce wind_r
                rock_loc = rock_loc + fall
            else:
                moving = False
                chamber = set_loc(rock_loc, rock_shape, chamber)
            if debug:
                print(set_loc(rock_loc, rock_shape, chamber.copy(), val=2)[:3 * r + 7, :])
        if debug:
            print(chamber[:3 * r + 7, :])

        r += 1

    # r +=1
    this_heigth = np.where(chamber.any(axis=0))[0].max()
    cycle_heigth = this_heigth - first_height
    cycle_length = r - first_encounter
    nr_rocks_after_converge = nr_rocks - first_encounter
    cycle_heigth_repeated = cycle_heigth * int(nr_rocks_after_converge/cycle_length)

    for r in range(nr_rocks_after_converge % cycle_length):

        # get new rock from rocktype
        rock_shape = rock_types[curr_rock_type]
        curr_rock_type = curr_rock_type + 1 if curr_rock_type + 1 < len(rock_types) else 0

        # find starting loc compared to chamber
        rock_loc = (2, np.where(chamber.any(axis=0))[0].max() + 4)

        # while rock has not stopped, iterate between:
        #   check and move to right/left, if possible
        #   check and move down fall -> if not, stop
        moving = True
        while moving:
            iter_wind = wind[wind_ind]
            wind_ind = wind_ind + 1 if wind_ind + 1 < len(wind) else 0

            if iter_wind == '>':
                if check_loc(rock_loc + wind_r, rock_shape, chamber):
                    rock_loc = rock_loc + wind_r
            else:
                if check_loc(rock_loc + wind_l, rock_shape, chamber):  # Can change to reduce wind_r
                    rock_loc = rock_loc + wind_l
            if debug:
                print(set_loc(rock_loc, rock_shape, chamber.copy(), val=2)[:3 * r + 7, :])

            if check_loc(rock_loc + fall, rock_shape, chamber):  # Can change to reduce wind_r
                rock_loc = rock_loc + fall
            else:
                moving = False
                chamber = set_loc(rock_loc, rock_shape, chamber)
            if debug:
                print(set_loc(rock_loc, rock_shape, chamber.copy(), val=2)[:3 * r + 7, :])
        if debug:
            print(chamber[:3 * r + 7, :])

    remainder = np.where(chamber.any(axis=0))[0].max() - this_heigth

    if debug or True:
        print(f'\n{r}')
        print(first_encounter)
        print(first_height)
        print(cycle_heigth)
        print(cycle_heigth_repeated)
        print(remainder)

    return first_height + cycle_heigth_repeated + remainder


@timing
def run_all(example_run: Union[int, bool]):

    file = f'aoc_17_exampledata{example_run}' if example_run else 'aoc_17_data'
    with open(file) as f:
        data = f.readlines()
    wind = [row.rstrip('\n') for row in data][0]
    wind_r = np.array([1, 0])
    wind_l = np.array([-1, 0])
    fall = np.array([0, -1])

    rock_ = np.array(((0, 0), (1, 0), (2, 0), (3, 0)))
    rockP = np.array(((0, 1), (1, 0), (1, 1), (2, 1), (1, 2)))
    rockL = np.array(((0, 0), (1, 0), (2, 0), (2, 1), (2, 2)))
    rockI = np.array(((0, 0), (0, 1), (0, 2), (0, 3)))
    rockO = np.array(((0, 0), (0, 1), (1, 0), (1, 1)))
    rock_types = [rock_, rockP, rockL, rockI, rockO]

    result_part1 = part1(7, rock_types, wind, wind_r, wind_l, fall, nr_rocks=2022)
    result_part2 = part2(7, rock_types, wind, wind_r, wind_l, fall, nr_rocks=1000000000000)
    # result_part2 = part2(7, rock_types, wind, wind_r, wind_l, fall, nr_rocks=2022)

    print(f'Results for {f"example" if example_run else "my"} input{f" {example_run}" if example_run else ""}:')
    print(f' Result of part 1: {result_part1}')
    print(f' Result of part 2: {result_part2}')  # 1566272189327  1566272189352

    print(f'\nDescriptives: \n TODO \n')


if __name__ == "__main__":
    [run_all(example_run=i) for i in [1]]
    run_all(example_run=False)
