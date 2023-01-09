from typing import Union
from util.util import timing


debug = False


def find_touching_pairs(cubes, other_cubes=None):

    if other_cubes is None:
        other_cubes = cubes
        other = False
    else:
        other = True

    touching_pairs = 0
    for i in range(len(cubes)):  # Could have used itertools.combinations..
        pt = cubes[i]
        for j in range((i+1) * (1-other), len(other_cubes)):
            other_pt = other_cubes[j]
            if (abs(pt[0] - other_pt[0]) == 1) and (pt[1] == other_pt[1]) and (pt[2] == other_pt[2]):  # Could have used manhattan distance
                touching_pairs += 1
            elif (abs(pt[2] - other_pt[2]) == 1) and (pt[1] == other_pt[1]) and (pt[0] == other_pt[0]):
                touching_pairs += 1
            elif (abs(pt[1] - other_pt[1]) == 1) and (pt[0] == other_pt[0]) and (pt[2] == other_pt[2]):
                touching_pairs += 1
    return touching_pairs


def part1(cubes):

    nr_cubes = len(cubes)
    touching_pairs = find_touching_pairs(cubes)

    return 6 * nr_cubes - 2 * touching_pairs


def part2(cubes):

    # Get min/max of elements to make containment space of cubes together
    xs = [cube[0] for cube in cubes]
    ys = [cube[1] for cube in cubes]
    zs = [cube[2] for cube in cubes]
    x_range = range(min(xs) + 1, max(xs) + 1)
    y_range = range(min(ys) + 1, max(ys) + 1)
    z_range = range(min(zs) + 1, max(zs) + 1)

    # Initialize inside cubes to all cubes in containment space except the given cubes
    inside = set()  # TODO
    for x in x_range:
        for y in y_range:
            for z in z_range:
                if (x, y, z) not in cubes:
                    inside.add((x, y, z))

    to_check = [(x_range.start, y_range.start, z_range.start)]

    # Remove all outside cubes
    outside = set()
    for p in to_check:
        if p in cubes or p in outside:
            continue
        outside.add(p)
        if p in inside:
            inside.remove(p)

        # Find potential new locations to check
        if p[0] - 1 >= x_range.start:
            to_check.append((p[0] - 1, p[1], p[2]))
        if p[0] + 1 <= x_range.stop:
            to_check.append((p[0] + 1, p[1], p[2]))
        if p[1] - 1 >= y_range.start:
            to_check.append((p[0], p[1] - 1, p[2]))
        if p[1] + 1 <= y_range.stop:
            to_check.append((p[0], p[1] + 1, p[2]))
        if p[2] - 1 >= z_range.start:
            to_check.append((p[0], p[1], p[2] - 1))
        if p[2] + 1 <= z_range.stop:
            to_check.append((p[0], p[1], p[2] + 1))

    # Do part 1, but also subtract borders with inside cubes
    nr_cubes = len(cubes)
    touching_pairs = find_touching_pairs(cubes)
    internal_borders = find_touching_pairs(cubes, other_cubes=list(inside))

    return 6 * nr_cubes - 2 * touching_pairs - 1 * internal_borders


@timing
def run_all(example_run: Union[int, bool]):

    file = f'aoc_18_exampledata{example_run}' if example_run else 'aoc_18_data'
    with open(file) as f:
        data = f.readlines()
    adj_data = sorted([tuple([int(i) for i in row.rstrip('\n').split(',')]) for row in data])

    result_part1 = part1(adj_data)
    result_part2 = part2(adj_data)

    print(f'\nResults for {f"example" if example_run else "my"} input{f" {example_run}" if example_run else ""}:')
    print(f' Result of part 1: {result_part1}')
    print(f' Result of part 2: {result_part2}')

    print(f'\nDescriptives: \n TODO \n')


if __name__ == "__main__":
    [run_all(example_run=i) for i in [2, 1]]
    run_all(example_run=False)
