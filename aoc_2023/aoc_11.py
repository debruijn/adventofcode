from typing import Union
from util.util import ProcessInput, run_day
import itertools

debug = False


def get_galaxies(data, scale):

    dims_orig = (len(data), len(data[0]))

    galaxies = []
    add_i = 0
    for i in range(dims_orig[0]):
        check_i = False
        for k in range(dims_orig[1]):
            if data[i][k] == '#':
                galaxies.append(add_i + i + k * 1j)
                check_i = True
        if not check_i:
            add_i += scale

    return galaxies, dims_orig


def get_sum_of_distances(galaxies, dims_orig, scale):

    empty_cols = []
    for k in range(dims_orig[1]):
        if not any([int(galaxy.imag) == k for galaxy in galaxies]):
            empty_cols.append(k)

    upd_galaxies = []
    for galaxy in galaxies:
        offset = sum([galaxy.imag > x for x in empty_cols]) * scale
        upd_galaxies.append(galaxy.real + (galaxy.imag + offset) * 1j)

    sum_length = 0
    for galaxy_x, galaxy_y in itertools.combinations(upd_galaxies, 2):
        sum_length += int(abs(galaxy_x.real - galaxy_y.real) + abs(galaxy_x.imag - galaxy_y.imag))

    return sum_length



def run_all(example_run: Union[int, bool]):

    data = ProcessInput(example_run=example_run, day=11, year=2023).data
    scale = 1000000 - 1

    galaxies, dims_orig = get_galaxies(data, 1)
    result_part1 = get_sum_of_distances(galaxies, dims_orig, 1)
    galaxies, dims_orig = get_galaxies(data, scale)
    result_part2 = get_sum_of_distances(galaxies, dims_orig, scale)

    extra_out = {'Original grid size': dims_orig,
                 'Number of galaxies': len(galaxies)}

    return result_part1, result_part2, extra_out


if __name__ == "__main__":
    run_day(run_all, [1])
