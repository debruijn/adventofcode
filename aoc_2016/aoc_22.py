from itertools import permutations
from typing import Union
from util.util import ProcessInput, run_day
from collections import deque


def run_all(example_run: Union[int, bool]):

    data = ProcessInput(example_run=example_run, day=22, year=2016).data

    # Part 1: directly loop over all permutations and do the required check (0 < used < avail).
    count_viable_pairs = 0
    for row1, row2 in permutations(data[2:], 2):
        used = int(row1.split('T')[1].strip())
        if used > 0:
            avail = int(row2.split('T')[2].strip())
            if used < avail:
                count_viable_pairs += 1
    result_part1 = count_viable_pairs

    # Part 2
    # First, find empty and big cells. Visual inspect: big: >100. For the non-big: all totals above 80, all used below
    # 80, so they all fit inside each other.
    dims = tuple(int(x[1:]) + 1 for x in data[-1].split()[0].split('-')[1:])
    empty = []
    biggy = []
    for row in data[2:]:
        used = int(row.split('T')[1].strip())
        if used == 0:
            loc = [int(x[1:]) for x in row.split()[0].replace('/dev/grid/node-', '').split('-')]
            empty.append(loc[0] + loc[1]*1j)
        if used > 100:
            loc = [int(x[1:]) for x in row.split()[0].replace('/dev/grid/node-', '').split('-')]
            biggy.append(loc[0] + loc[1]*1j)

    # There are a few biggies (see above) and one empty.
    # Goal: move the empty spot to the node with the target info, and then shift that over to 0,0 like in the example.
    # Assumption (using my input): the biggies form a wall that you have to get around.
    # So on x axis, you have to go down 1 more than the lowest x in `biggy`, and you have to move that distance back
    # again later + the difference at the start between empty.x and target.x
    # On y-axis, it is just bringing down empty.y to 0.
    # Then the shuffle to 0,0, which is just 5 moves for each step (see example)

    empty = empty[0]
    move_x = int( 2*(empty.real - min(x.real for x in biggy) + 1) + (dims[0] - 1 - empty.real) )
    move_y = int(empty.imag)
    shuffle = 5*(dims[0]-2)  # -1 for index vs size; -1 for the initial step being down by the moves above
    result_part2 = move_x + move_y + shuffle

    # Approach without this assumption:
    # - BFS with priority queue (A* like):
    #   - State consists of location of empty and target info
    #   - Priority function is curr_steps + "estimated steps" based on manhattan distance
    #   - Pop candidate based on lowest value of that priority function
    #   - Generate new candidates based on what is allowed (not in biggy) and what is not yet done (keep track of hist)
    #   - When a solution is found, start eliminating candidates that have priority function above that value, and see
    #     if a better solution pops up from the remaining candidates.
    # I might implement this later.

    extra_out = {'Number of nodes in input': len(data)-2,
                 'Size of grid': dims,
                 'Location of biggies': biggy,
                 'Location of empty spot initially': empty}

    return result_part1, result_part2, extra_out


if __name__ == "__main__":
    run_day(run_all, [])
