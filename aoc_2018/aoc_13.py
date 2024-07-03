from typing import Union
from util.util import ProcessInput, run_day
from itertools import cycle

debug = False

turn_mapping = {('\\', 1): 1j, ('/', 1): -1j, ('\\', -1): -1j, ('/', -1): 1j,
                ('\\', 1j): 1, ('/', 1j): -1, ('\\', -1j): -1, ('/', -1j): 1}
cart_mapping = {'>': 1j, 'v': 1, '<': -1j, '^': -1}


def print_grid(data):
    for row in data:
        print(row)


def run_all(example_run: Union[int, bool]):
    data = ProcessInput(example_run=example_run, day=13, year=2018).data

    # Processing: get dict of carts (location: direction, turn_cycle) and of the track (location: track-type)
    grid = {}
    carts = {}
    for i, row in enumerate(data):
        for j, char in enumerate(row):
            if char in cart_mapping.keys():  # Add cart to dict of carts, and replace it with the underlying track
                this_cart = (cart_mapping[char], cycle([1j, 1, -1j]))  # direction, next turn
                carts[i + j * 1j] = this_cart
                data[i] = row[:j] + ('-' if char in '<>' else '|') + row[j + 1:]
            if data[i][j] != ' ':
                grid[i + j * 1j] = data[i][j]
    n_initial_carts = len(carts)

    tick = 0
    first_crash_loc = -1  # This variable will hold result of part 1
    while len(carts) > 1:
        tick += 1
        cart_locs = sorted(carts.keys(), key=lambda x: (x.real, x.imag))  # Carts in order of movement

        this_tick_deleted = []
        for cart in cart_locs:
            if cart not in this_tick_deleted:  # The cart_locs loop isn't affected by whether a cart is deleted already.
                new_loc = cart + carts[cart][0]
                if new_loc in carts.keys():  # Crash on track! Location already exists.
                    first_crash_loc = new_loc if first_crash_loc == -1 else first_crash_loc
                    del carts[new_loc]
                    this_tick_deleted.append(new_loc)  # In case new_loc still has to feature in cart_locs
                else:  # No crash, so adjust new direction based on track type of new location
                    if grid[new_loc] == '+':
                        new_dir = carts[cart][0] * next(carts[cart][1])
                    elif (grid[new_loc], carts[cart][0]) in turn_mapping.keys():
                        new_dir = turn_mapping[(grid[new_loc], carts[cart][0])]
                    else:
                        new_dir = carts[cart][0]
                    carts[new_loc] = (new_dir, carts[cart][1])
                del carts[cart]

    result_part1 = f"{int(first_crash_loc.imag)},{int(first_crash_loc.real)}"
    if len(carts) > 0:
        final_cart_loc = list(carts.keys())[0]
        result_part2 = f"{int(final_cart_loc.imag)},{int(final_cart_loc.real)}"
    else:
        result_part2 = "No carts left"

    extra_out = {'Total track length': len(grid),
                 'Initial number of carts': n_initial_carts,
                 'Number of ticks until all crashes': tick}

    return result_part1, result_part2, extra_out


if __name__ == "__main__":
    run_day(run_all, [1, 2])
