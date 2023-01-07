import numpy as np
from typing import Union
from util.util import timing
import tqdm


debug = False
wind_r = np.array([1, 0])
wind_l = np.array([-1, 0])
fall = np.array([0, -1])

rock_ = np.array(((0, 0), (1, 0), (2, 0), (3, 0)))
rockP = np.array(((0, 1), (1, 0), (1, 1), (2, 1), (1, 2)))
rockL = np.array(((0, 0), (1, 0), (2, 0), (2, 1), (2, 2)))
rockI = np.array(((0, 0), (0, 1), (0, 2), (0, 3)))
rockO = np.array(((0, 0), (0, 1), (1, 0), (1, 1)))
rock_types = [rock_, rockP, rockL, rockI, rockO]

chamber_width = 7


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


def get_max(chamber):
    return np.where(chamber.any(axis=0))[0].max()


def do_single_rock_iteration(setting, wind):

    chamber = setting['chamber']
    curr_rock_type = setting['curr_rock_type']
    wind_ind = setting['wind_ind']

    rock_shape = rock_types[curr_rock_type]
    curr_rock_type = curr_rock_type + 1 if curr_rock_type + 1 < len(rock_types) else 0
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

        if check_loc(rock_loc + fall, rock_shape, chamber):  # Can change to reduce wind_r
            rock_loc = rock_loc + fall
        else:
            moving = False
            chamber = set_loc(rock_loc, rock_shape, chamber)

    return {'chamber': chamber, 'wind_ind': wind_ind, 'curr_rock_type': curr_rock_type}


def brute_force_method(wind, nr_rocks=2022, setting=None):

    if setting is None:
        chamber = np.zeros([chamber_width, 3 * nr_rocks])  # chamber = np.ones([chamber_width, 1])
        chamber[:, 0] = 1
        setting = {'chamber': chamber, 'curr_rock_type': 0, 'wind_ind': 0}

    for _ in tqdm.trange(nr_rocks):
        setting = do_single_rock_iteration(setting, wind)

    return get_max(setting['chamber'])


def skyline(chamber):
    init_skyline = [np.where(chamber[i,:])[0].max() for i in range(chamber.shape[0])]
    norm_skyline = tuple([max(init_skyline) - i for i in init_skyline])
    return norm_skyline


def cycle_detection_method(wind, nr_rocks=1000000000000):

    states = set()
    init_height = 10000

    r = 0
    all_states_unique = True
    first_encounter = 0
    first_height = 0

    chamber = np.zeros([chamber_width, init_height])  # chamber = np.ones([chamber_width, 1])
    chamber[:, 0] = 1
    setting = {'chamber': chamber, 'curr_rock_type': 0, 'wind_ind': 0}

    while all_states_unique:

        this_state = (setting['curr_rock_type'], setting['wind_ind'], skyline(chamber))
        if this_state in states:
            if first_encounter > 0:
                break
            else:
                first_encounter = r
                first_height = np.where(setting['chamber'].any(axis=0))[0].max()
                states = set()  # Reset states to keep track of second time you find it
        states.add(this_state)

        setting = do_single_rock_iteration(setting, wind)
        r += 1

    this_height = np.where(chamber.any(axis=0))[0].max()
    cycle_height = this_height - first_height
    cycle_length = r - first_encounter
    nr_rocks_after_converge = nr_rocks - first_encounter
    summed_cycle_height = cycle_height * int(nr_rocks_after_converge/cycle_length)

    for _ in tqdm.trange(nr_rocks_after_converge % cycle_length):
        setting = do_single_rock_iteration(setting, wind)
    remainder = np.where(setting['chamber'].any(axis=0))[0].max() - this_height

    return first_height + summed_cycle_height + remainder, first_encounter, cycle_length, cycle_height


@timing
def run_all(example_run: Union[int, bool]):

    file = f'aoc_17_exampledata{example_run}' if example_run else 'aoc_17_data'
    with open(file) as f:
        data = f.readlines()
    wind = [row.rstrip('\n') for row in data][0]

    result_part1_brute = brute_force_method(wind, nr_rocks=2022)
    result_part1_cycle = cycle_detection_method(wind, nr_rocks=2022)[0]
    result_part2_cycle, first_encounter, cycle_length, cycle_height = cycle_detection_method(wind,
                                                                                             nr_rocks=1000000000000)

    print(f'\nResults for {f"example" if example_run else "my"} input{f" {example_run}" if example_run else ""}:')
    print(f' Result of part 1: {result_part1_brute} (via brute force), '
          f'{result_part1_cycle} (via cycle detection method)')
    print(f' Result of part 2: {result_part2_cycle} (via cycle detection method)')  # 1566272189327  1566272189352

    print(f'\nDescriptives: \n First repeat: {first_encounter} \n Cycle length: {cycle_length} '
          f'\n Cycle height: {cycle_height} \n Converged to cycle: {first_encounter - cycle_length}\n')


if __name__ == "__main__":
    [run_all(example_run=i) for i in [1]]
    run_all(example_run=False)
