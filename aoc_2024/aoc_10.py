from typing import Union
from util.util import ProcessInput, run_day


def run_all(example_run: Union[int, bool]):

    # Process data into numerical heights and trailhead starting locations
    data = ProcessInput(example_run=example_run, day=10, year=2024).data
    data = [[int(el) for el in row] for row in data]
    trailheads = [i + j*1j for i, row in enumerate(data) for j, el in enumerate(row) if el == 0]

    # For each trailhead, start all potential routes to find score and rating
    total_score, total_rating = 0, 0
    for trailhead in trailheads:
        final_locs = set()
        queue = [(trailhead, 0)]
        while len(queue) > 0:
            this_loc, this_h = queue.pop()

            if this_h == 9:
                final_locs.add(this_loc)
                total_rating += 1
                continue

            for jmp in [1, 1j, -1, -1j]:
                jmp_loc = this_loc + jmp
                if 0 <= jmp_loc.real < len(data) and 0 <= jmp_loc.imag < len(data[0]):
                    if data[int(jmp_loc.real)][int(jmp_loc.imag)] == this_h + 1:
                        queue.append((jmp_loc, this_h + 1))
        total_score += len(final_locs)

    result_part1 = total_score
    result_part2 = total_rating

    extra_out = {'Dimensions of grid': (len(data), len(data[0])),
                 'Number of trailheads': len(trailheads)}

    return result_part1, result_part2, extra_out


if __name__ == "__main__":
    run_day(run_all, [1])
