from typing import Union
from util.util import ProcessInput, run_day
from itertools import product

debug = False


def run_all(example_run: Union[int, bool]):

    data = ProcessInput(example_run=example_run, day=11, year=2018).as_single_int().data

    size = 300

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
    for k in range(1, size+1):
        for i, j in product(range(1, size+2-k), repeat=2):
            if k > 1:
                this_square = (all_squares[(i, j, k-1)] + sum([fuel_cell[i+k-1 + y*1j] for y in range(j, j+k)]) +
                               sum([fuel_cell[x + (j+k-1)*1j] for x in range(i, i + k-1)]))
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

    # Note: this algorithm works, and the data is such that the best result can be found for relatively low k. But
    # running until k=300 costs about 7 minuts on my machine (for each input, so times 3, 21 minutes, for both examples
    # and the actual input). In theory you could find the best value for a k close to 300, so you would need to run it
    # in full.
    # Proposal for better algorithms if this actually mattered:
    # 1 Above we use the k-1 result, and add new lines around it. What if we stored those intermediate calculations? We
    #   can reuse the same line for calculations on either side of a grid. We can also calculate a line as the line one
    #   shorter with one value added.
    # 2 Deconstruct k not just in (k-1, 1), but also in other values. Examples:
    #   - A 9x9 square can be made with 9 3x3 squares, so 9 reads of values, instead of 1 read of a 8x8 grid and then
    #     9+8 additional 1x1 reads
    #   - A 5x5 grid with 1 3x3 square and 3 2x2 squares, and we only have to add/subtract 2 1x1 squares, for a total of
    #     6 reads, versus the current 1 (4x4) + 5+4 = 10 reads.
    #   These gains become bigger for bigger grids. But challenge is: how to determine best cut up:
    #   - Easy: when number is divisible by 2, 3, 5, etc -> use those.
    #   - Otherwise: it is more of a puzzle to find the optimal one. Can go back to use k/2 (floor and ceil), and then
    #     fill up using only 1x1s to avoid errors. So 7x7 -> 4x4 + 3 3x3s + 6 1x1s.
    # 3 Don't stick to just squares, but find all (or all necessary) rectangles.
    #   - Then each square can be decomposed in exactly 4 rectangles. E.g. 7x7 -> 4x4, 4x3, 3x4, 3x3.
    #   - To avoid recalculation, the only non-squares could be all 1xKs or Kx1s. 7x7 -> 6x6, 1x1, 1x6, 6x1.
    #   - So all squares are decomposed into 4 reads always, at the cost of having to calculate some rectangles.
    #
    # Overall, I think approach is 3 is the best.

    extra_out = {'Input value': data}

    return result_part1, result_part2, extra_out


if __name__ == "__main__":
    run_day(run_all, [])
