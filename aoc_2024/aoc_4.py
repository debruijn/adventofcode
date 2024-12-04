from typing import Union
from util.util import ProcessInput, run_day


def run_all(example_run: Union[int, bool]):

    data = ProcessInput(example_run=example_run, day=4, year=2024).data

    # Part 1
    count = 0
    dirs = [1, 1+1j, 1j, -1+1j, -1, -1-1j, -1j, 1-1j]
    for x in range(len(data)):
        for y in range(len(data[0])):
            if data[x][y] != 'X':
                continue
            for dir_ in dirs:
                end = x + y * 1j + 3 * dir_
                if end.real < 0 or end.imag < 0 or end.real>=len(data) or end.imag>=len(data[0]):
                    continue
                word = data[x][y] + "".join(data[x + int(dir_.real) * i][y + int(dir_.imag) * i] for i in range(1, 4))
                if word == 'XMAS':
                    count += 1
    result_part1 = count

    # Part 2
    count = 0
    dirs = [1+1j, -1+1j, -1-1j, 1-1j]  # If you include the non-diagonals, you get a + not an X!
    for x in range(len(data)):
        for y in range(len(data[0])):
            if data[x][y] != 'M':
                continue
            for dir_ in dirs:
                end = x + y*1j + 2*dir_
                if end.real < 0 or end.imag < 0 or end.real>=len(data) or end.imag>=len(data[0]):
                    continue
                rot = dir_ * -1j
                rot_loc = (x+ y*1j) + rot + dir_  # Start point of other MAS - Only to the right to avoid doubles
                # If you would want to do +-MAS as well, uncomment these lines:
                # rot_end = rot_loc - 2 * rot
                # if rot_end.real < 0 or rot_end.imag < 0 or rot_end.real>=len(data) or rot_end.imag>=len(data[0]):
                #     continue
                # if rot_loc.real < 0 or rot_loc.imag < 0 or rot_loc.real>=len(data) or rot_loc.imag>=len(data[0]):
                #     continue
                word = data[x][y] + "".join(data[x + int(dir_.real)*i][y + int(dir_.imag)*i] for i in range(1, 3))
                word2 = "".join(data[int(rot_loc.real - rot.real*i)][int(rot_loc.imag - rot.imag*i)] for i in range(3))
                if word == 'MAS' and word2 == 'MAS':
                    count += 1
    result_part2 = count

    extra_out = {'Number of elements in input': (len(data), len(data[0]))}

    return result_part1, result_part2, extra_out


if __name__ == "__main__":
    run_day(run_all, [1])
