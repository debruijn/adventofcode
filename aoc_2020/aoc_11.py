from typing import Union
from util.util import ProcessInput, run_day
import numpy as np
import itertools
import functools

debug = False


@functools.lru_cache()
def is_neighbour(seatA, seatB):
    diff = seatA - seatB
    return (abs(diff.real) <= 1) and (abs(diff.imag) <= 1)


def get_neighbours(seat):
    return [seat + complex(i, j) for i, j in itertools.product([1, 0, -1], repeat=2)
            if not (i == 0 and j == 0)]


def get_visible(seat, seats, dim):
    visible = []
    for i, j in itertools.product([1, 0, -1], repeat=2):
        if not (i == 0 and j == 0):
            direction = complex(i, j)
            for k in itertools.count(1):
                if (seat + k * direction).real < 0 or (seat + k * direction).real >= dim[0] or (
                        seat + k * direction).imag < 0 \
                        or (seat + k * direction).imag >= dim[1]:
                    break
                if seat + k * direction in seats:
                    visible.append(seat + k * direction)
                    break
    return visible


def run_all(example_run: Union[int, bool]):
    data = ProcessInput(example_run=example_run, day=11).data
    data = np.array([[0 if x == '.' else 1 for x in row] for row in data])
    seats = np.where(data == 1)
    seats = list(zip(seats[0], seats[1]))
    seats = set([complex(x[0], x[1]) for x in seats])
    dim = data.shape

    # Slow implementation - was slow due to check each seat against each other (occupied) seat
    # occupied = set()
    # prev_occupied = {1}
    # for i in itertools.count():
    #     prev_occupied = occupied
    #     occupied = set()
    #     for seat in seats:
    #         sum_occ = sum([is_neighbour(seat, other_seat) for other_seat in prev_occupied if other_seat != seat])
    #         if seat in prev_occupied and sum_occ < 4:
    #             occupied.add(seat)
    #         elif seat not in prev_occupied and sum_occ == 0:
    #             occupied.add(seat)
    #     print(f'{i}: {len(occupied)}')
    #     if occupied == prev_occupied:
    #         break
    #
    # result_part1 = len(occupied)

    # Part 1 and part 2 have two different implementations that could be swapped out:
    # - Method 1 reconstructs occupied from an empty set in each iteration
    # - Method 2 adjusts the existing set by removing/adding elements
    # The methods are about the same in speed, also due to method 2 needing to copy the set into prev_occupied
    occupied = set()
    for _ in itertools.count():
        prev_occupied = occupied
        occupied = set()
        for seat in seats:
            nbrs = get_neighbours(seat)
            sum_occ = sum(x in prev_occupied for x in nbrs)
            if seat in prev_occupied and sum_occ < 4:
                occupied.add(seat)
            elif seat not in prev_occupied and sum_occ == 0:
                occupied.add(seat)
        if occupied == prev_occupied:
            break
    result_part1 = len(occupied)

    occupied = set()
    for _ in itertools.count():
        prev_occupied = occupied.copy()
        for seat in seats:
            nbrs = get_visible(seat, seats, dim)
            sum_occ = sum(x in prev_occupied for x in nbrs)
            if seat in prev_occupied and sum_occ >= 5:
                occupied.remove(seat)
            elif seat not in prev_occupied and sum_occ == 0:
                occupied.add(seat)
        if occupied == prev_occupied:
            break
    result_part2 = len(occupied)

    extra_out = {'Dimension of waiting area': dim,
                 'Total number of seats': len(seats)}

    return result_part1, result_part2, extra_out


if __name__ == "__main__":
    run_day(run_all, [1])
