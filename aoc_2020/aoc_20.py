from typing import Union
from util.util import ProcessInput, run_day
import itertools
import numpy as np
from collections import defaultdict, Counter

debug = False


def check_match(x, y):
    locations = []
    if np.all(x[:, -1] == y[:, 0]):  # x y
        locations.append(1)
    if np.all(x[:, 0] == y[:, -1]):  # y x
        locations.append(2)
    if np.all(x[-1, :] == y[0, :]):  # x on top of y
        locations.append(3)
    if np.all(x[0, :] == y[-1, :]):  # y on top of x
        locations.append(4)
    return locations


def rotate(x, times=1):
    if times == 0:
        return x.copy()
    if times == 1:
        y = x.copy().transpose()
        for i in range(x.shape[0]):
            y[:, i] = x[i, -1:-x.shape[0] - 1:-1]
        return y
    if times >= 4:
        return rotate(flip(x.copy()), times - 4)
    return rotate(np.flip(x.copy()), times - 2)


def flip(x):
    return np.fliplr(x.copy())


def run_all(example_run: Union[int, bool]):
    data = ProcessInput(example_run=example_run, day=20, year=2020).as_list_of_strings_per_block().data
    tiles = {int(tile[0].replace(':', '').split(' ')[1]): tile[1:] for tile in data}
    tiles = {k: np.array([[1 if y == '#' else 0 for y in x] for x in tiles[k]]) for k in tiles.keys()}
    n_dim = int(np.sqrt(len(tiles)))
    T = 10  # Tile size

    matches = defaultdict(lambda: defaultdict(dict))
    alt_matches = defaultdict(list)
    full_matches = defaultdict(list)

    for x, y in itertools.permutations(tiles.keys(), 2):
        for rot in range(8):
            locations = check_match(tiles[x], rotate(tiles[y], rot))
            if len(locations) > 0:
                matches[x][y].update({rot: locations})
                alt_matches[y].append(x)
                full_matches[x].append(y)

    # Corner pieces have only 2 neighbours. In both example and actual data, there are 4 tiles with only 2 neighbours.
    must_be_corner_pieces = [x for x in full_matches if len(full_matches[x]) == 2]

    solution = np.zeros((n_dim, n_dim), dtype=int)
    full_pic = np.zeros([T * x for x in solution.shape])

    # Find a piece must can be in upper-left corner for this rotation. (If none had existed, rotate until they do)
    for corner_piece in must_be_corner_pieces:
        if [list(x.values())[0][0] for x in matches[corner_piece].values()] in ([1, 3], [3, 1]):
            solution[0, 0] = corner_piece
            full_pic[0:T, 0:T] = tiles[corner_piece]

    # Loop over all other positions in the configuration, and find which tile must be there using the possible mappings.
    for i, j in itertools.product(range(n_dim), repeat=2):
        if i+j > 0:
            if j > 0:  # Look to the left if is there is a tile there -> location is 1
                prev = solution[i, j-1]
                this = [(x, matches[prev][x]) for x in matches[prev] if [1] in matches[prev][x].values()]
            else:  # Otherwise, look above -> location is 3
                prev = solution[i-1, j]
                this = [(x, matches[prev][x]) for x in matches[prev] if [3] in matches[prev][x].values()]
            solution[i, j] = this[0][0]  # There will be only 1 that passes (for these datasets, not necessarily)

            # Rotate "this" such that it fits next to / below "prev" without further rotation.
            rot = list(matches[prev][this[0][0]].keys())[0]
            tiles[this[0][0]] = rotate(tiles[this[0][0]], rot)

            # Update the location/rotation of neighbours of "this" after applying its own rotation.
            other = matches[this[0][0]].keys()
            for o in other:
                matches[this[0][0]][o] = dict()
                for rot in range(8):
                    locations = check_match(tiles[this[0][0]], rotate(tiles[o], rot))
                    if len(locations) > 0:
                        matches[this[0][0]][o].update({rot: locations})

            # Also update the full picture with the tile.
            full_pic[T * i:T * (i + 1), T * j:T * (j + 1)] = tiles[this[0][0]]

    # Check to see if in final full picture the columns/rows that should be the same are the same
    for i in range(n_dim-1):
        if not np.all(full_pic[:, (i+1)*T] == full_pic[:, (i+1)*T - 1]):
            raise ValueError
        if not np.all(full_pic[(i+1)*T, :] == full_pic[(i+1)*T - 1, :]):
            raise ValueError

    # Delete overlapping entries (part 1) --> delete all borders (part 2)
    full_pic = np.delete(full_pic, [T * x - 1 for x in range(1, n_dim)] + [T * x for x in range(1, n_dim)], axis=0)
    full_pic = np.delete(full_pic, [0, -1], axis=0)
    full_pic = np.delete(full_pic, [T * x - 1 for x in range(1, n_dim)] + [T * x for x in range(1, n_dim)], axis=1)
    full_pic = np.delete(full_pic, [0, -1], axis=1)

    # Result for part 1 doesn't need full picture, we can just look at which pieces had to be in the corner.
    result_part1 = np.cumprod(must_be_corner_pieces)[-1]

    # Work specific for part 2
    nr_monsters = np.zeros(8)
    monster_shape = np.array([[1, 2, 2, 1, 1, 2, 2, 1, 1, 2, 2, 1, 1, 1, 0],
                              [0, 1, 4, 5, 6, 7, 10, 11, 12, 13, 16, 17, 18, 19, 18]])
    for rot in range(8):
        this_pic = rotate(full_pic, rot)
        for i in range(this_pic.shape[0] - max(monster_shape[0])):
            for j in range(this_pic.shape[1] - max(monster_shape[1])):
                check_pic = this_pic[monster_shape[0]+i, monster_shape[1]+j]
                if np.all(check_pic):
                    nr_monsters[rot] += 1

    result_part2 = int(full_pic.sum() - monster_shape.shape[1] * max(nr_monsters))

    extra_out = {'Number of tiles in input': len(data),
                 'Number of potential matches': len(matches)}

    return result_part1, result_part2, extra_out


if __name__ == "__main__":
    run_day(run_all, [1])
