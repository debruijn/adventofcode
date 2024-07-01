from typing import Union
from util.util import ProcessInput, run_day, DefaultDictWithCustomFactory
from itertools import product


debug = False


def run_all(example_run: Union[int, bool]):

    data = ProcessInput(example_run=example_run, day=11, year=2018).as_single_int().data

    size = 300
    subsize = 30  # Smaller size to run part 2 for - can set this to 300 if you want to check that it stays optimal

    # Calculate all individual fuel cells without aggregating to a square
    fuel_cell = {}
    for i, j in product(range(1, size+1), repeat=2):
        rack_id = i + 10
        power_lvl = rack_id * j
        power_lvl += data
        power_lvl *= rack_id
        power_lvl = int(str(power_lvl)[-3]) if power_lvl >= 100 else 0
        fuel_cell[(i + j*1j)] = power_lvl - 5

    # Go over all square sizes and upper-left corners. Reuse the sum for earlier steps if already used.
    curr_max = -1000000
    curr_max_coor = ""
    all_squares = {}
    result_part1 = ""

    all_horizontal = DefaultDictWithCustomFactory(lambda x: fuel_cell[x[0] + (x[1] + x[2] - 1) * 1j] +
                                                            (all_horizontal[(x[0], x[1], x[2]-1)] if x[2] > 1 else 0))
    all_vertical = DefaultDictWithCustomFactory(lambda x: fuel_cell[x[0] + x[2] - 1 + x[1] * 1j] +
                                                          (all_vertical[(x[0], x[1], x[2]-1)] if x[2] > 1 else 0))

    for k in range(1, subsize):
        for i, j in product(range(1, size+2-k), repeat=2):
            if k > 1:
                this_square = all_squares[(i, j, k-1)] + all_horizontal[(i+k-1, j, k)] + all_vertical[(i, j+k-1, k-1)]

                # Old implementation (slow!):
                # this_square = (all_squares[(i, j, k-1)] + sum([fuel_cell[i+k-1 + y*1j] for y in range(j, j+k)]) +
                #                sum([fuel_cell[x + (j+k-1)*1j] for x in range(i, i + k-1)]))
            else:
                this_square = fuel_cell[i + j*1j]
            all_squares[(i, j, k)] = this_square
            if this_square > curr_max:
                curr_max = this_square
                curr_max_coor = f"{i},{j},{k}"
        if debug:
            print(f"Best after {k}: {curr_max_coor} at {curr_max}")

        if k == 3:
            result_part1 = curr_max_coor  # Note: this indirectly assumes that solution at k=3 is better than at k<3

    result_part2 = curr_max_coor

    extra_out = {'Input value': data}

    return result_part1, result_part2, extra_out


if __name__ == "__main__":
    run_day(run_all, [1, 2])
