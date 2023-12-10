from typing import Union
from util.util import ProcessInput, run_day
from itertools import product


debug = False


def find_crossings(lph, lpv):
    # Function to find crossings between horizontal and vertical line parts
    crossings_f = []
    steps_f = []
    for lph_i, lpv_i in product(lph, lpv):
        if ((lph_i[0].real - lpv_i[0].real) * (lph_i[1].real - lpv_i[1].real) <= 0) and \
                ((lph_i[0].imag - lpv_i[0].imag) * (lph_i[1].imag - lpv_i[1].imag) <= 0):
            crossings_f.append(lph_i[0].imag + lpv_i[0].real * 1j)
            steps_f.append(lph_i[2] + lpv_i[2] + abs(lpv_i[0].real - lph_i[0].real) +
                           abs(lph_i[0].imag - lpv_i[0].imag))

    return crossings_f, steps_f


def run_all(example_run: Union[int, bool]):

    data = ProcessInput(example_run=example_run, day=3, year=2019).data

    # Additional processing: construct horizontal and vertical line parts of both wires
    line_parts_hor = []
    line_parts_vert = []
    for wire in data:
        line_part_hor = []
        line_part_vert = []
        curr_point = 0+0j
        steps = wire.split(',')
        dist = 0
        for step in steps:
            if step[0] in 'RL':
                new_point = curr_point + (-1) ** (step[0]=='L') * int(step[1:])
                line_part_hor.append((curr_point, new_point, dist))
            else:
                new_point = curr_point + (-1) ** (step[0] == 'D') * int(step[1:])*1j
                line_part_vert.append((curr_point, new_point, dist))
            curr_point = new_point
            dist += int(step[1:])
        line_parts_hor.append(line_part_hor)
        line_parts_vert.append(line_part_vert)

    # Run function to find crossings for horizontal and vertical pieces
    crossings_1, steps_1 = find_crossings(line_parts_hor[0], line_parts_vert[1])
    crossings_2, steps_2 = find_crossings(line_parts_hor[1], line_parts_vert[0])
    crossings = crossings_1 + crossings_2
    steps = steps_1 + steps_2

    distances = [abs(x.real) + abs(x.imag) for x in crossings]

    result_part1 = int(min([x for x in distances if x > 0]))
    result_part2 = int(min([x for x in steps if x > 0]))

    extra_out = {'Number of wires in input': len(data),
                 'Number of line parts in wire 1': len(line_parts_hor[0]) + len(line_parts_vert[0]),
                 'Number of line parts in wire 2': len(line_parts_hor[1]) + len(line_parts_vert[1]),
                 'Number of crossings': len(crossings)}

    return result_part1, result_part2, extra_out


if __name__ == "__main__":
    run_day(run_all, [1, 2, 3])
