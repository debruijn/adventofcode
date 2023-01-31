from typing import Union
from util.util import ProcessInput, run_day
import itertools
import numpy as np
from collections import defaultdict

debug = False


def check_match(x, y):
    matches = []
    if np.all(x[:, -1] == y[:, 0]):
        matches.append(1)
    if np.all(x[:, 0] == y[:, -1]):
        matches.append(2)
    if np.all(x[-1, :] == y[0, :]):
        matches.append(3)
    if np.all(x[0, :] == y[-1, :]):
        matches.append(4)
    return matches


def rotate(x, times=1):

    if times == 0:
        return x
    if times == 1:
        y = x.transpose()
        for i in range(x.shape[0]):
            y[:, i] = x[i, -1:-x.shape[0]-1:-1]
        return y
    else:
        return rotate(rotate(x, 1), times-1)


def run_all(example_run: Union[int, bool]):

    data = ProcessInput(example_run=example_run, day=20).as_list_of_strings_per_block().data
    tiles = {int(tile[0].replace(':', '').split(' ')[1]): tile[1:] for tile in data}
    tiles = {k: np.array([[1 if y == '#' else 0 for y in x] for x in tiles[k]]) for k in tiles.keys()}

    matches = defaultdict(lambda: defaultdict(dict))
    alt_matches = defaultdict(list)
    for x, y in itertools.combinations(tiles.keys(), 2):
        for rot in [0, 1, 2, 3]:
            check = check_match(tiles[x], rotate(tiles[y], rot))
            if len(check) > 0:
                matches[x][y].update({rot: check})
                alt_matches[y].append(x)

    print(matches)
    print(alt_matches)

    ref_tile = [x for x in tiles.keys()][0]
    tile_stack = {k: v for k, v in tiles.items() if k != ref_tile}

    # Create function (to return the correct permutation, or immediately the corner points)
    # For remaining tiles, iterate over each one that can be matched to current tiles in a spot that is not yet taken
    # Also check if total dimension is not too big


    result_part1 = "TODO"
    result_part2 = "TODO"

    extra_out = {'Number of tiles in input': len(data),
                 'Number of potential matches': len(matches)}

    return result_part1, result_part2, extra_out


if __name__ == "__main__":
    run_day(run_all, [1])
