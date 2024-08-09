from itertools import combinations
from typing import Union
from util.util import ProcessInput, run_day


def run_all(example_run: Union[int, bool]):

    data = ProcessInput(example_run=example_run, day=20, year=2017).data

    # Part 1: long-term nearest is particle with lowest absolute acceleration (summed across dimensions)
    # Also: process particles for part 2 to a list of p, v, a tuples.
    particles = []
    min_a = (100000000000, -1)
    for i, row in enumerate(data):
        row = row.replace('< ', '<')
        p, v, a = row.split(' ')
        p = tuple(int(x) for x in p[3:-2].split(','))
        v = tuple(int(x) for x in v[3:-2].split(','))
        a = tuple(int(x) for x in a[3:-1].split(','))
        abs_a = sum(abs(x) for x in a)
        min_a = (abs_a, i) if abs_a < min_a[0] else min_a
        particles.append((p, v, a))

    result_part1 = min_a[1]

    # Part 2: remove collisions and move particles that are "safe" to a separate list
    # Stop when all particles are either removed or safe
    safe = []
    nr_ticks = 0

    while len(particles) > 0:

        # Remove collisions, but not immediately because >2 might collide at same spot
        to_remove = set()
        for pt1, pt2 in combinations(range(len(particles)), 2):
            if particles[pt1][0] == particles[pt2][0]:
                to_remove.update({pt1, pt2})
        [particles.pop(i) for i in sorted(list(to_remove), reverse=True)]

        # Update each velocity and location
        for i, point in enumerate(particles):
            p, v, a = point
            v = tuple(v[i] + a[i] for i in range(len(p)))
            p = tuple(v[i] + p[i] for i in range(len(p)))
            particles[i] = (p, v, a)
        nr_ticks += 1

        # Detect particles that are safe: compared to each other particle, for each dimension,
        # either staying bigger or smaller for sure
        to_move = []
        for i, pt in enumerate(particles):
            safe_dim = [True, True, True]
            for j, other in enumerate(particles):  # Could be optimized by stopping when all safe_dim is False
                if i == j:
                    continue  # Don't compare particle with itself
                for d, dim in enumerate(safe_dim):
                    if pt[0][d] < other[0][d]:
                        if other[1][d] < pt[1][d] or other[2][d] < pt[2][d]:
                            safe_dim[d] = False
                    else:
                        if other[1][d] > pt[1][d] or other[2][d] > pt[2][d]:
                            safe_dim[d] = False
                if not all(safe_dim):
                    break
            if all(safe_dim):
                safe.append(pt)
                to_move.append(i)

        [particles.pop(i) for i in reversed(to_move)]

    result_part2 = len(safe)

    extra_out = {'Number of particles': len(data),
                 'Number of ticks needed': nr_ticks}

    return result_part1, result_part2, extra_out


if __name__ == "__main__":
    run_day(run_all, [1])
