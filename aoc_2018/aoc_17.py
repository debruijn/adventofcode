import math
from typing import Union
from util.util import ProcessInput, run_day, isdigit


def as_list_of_ints(row, pattern=" ", remove=()):
    for rm in remove:
        row = row.replace(rm, pattern)
    row = [int(s) for s in row.split(pattern) if isdigit(s)]
    return row


def run_all(example_run: Union[int, bool]):

    data = ProcessInput(example_run=example_run, day=17, year=2018).data

    source = (500, 0)

    # Process to coordinates with clay (and find max/min y)
    clay = set()
    for row in data:
        nums = as_list_of_ints(row, pattern=" ", remove=(",", "..", "="))
        if row.startswith('x'):
            clay = clay.union([(nums[0], i) for i in range(nums[1], nums[2]+1)])
        else:
            clay = clay.union([(i, nums[0]) for i in range(nums[1], nums[2]+1)])
    min_y = int(min(clay, key=lambda x: x[1])[1])
    max_y = int(max(clay, key=lambda x: x[1])[1])
    min_x = int(min(clay, key=lambda x: x[0])[0])
    max_x = int(max(clay, key=lambda x: x[0])[0])

    # Initializing queue and where water is set or falling.
    queue = [(source[0], source[1], True)]  # x_loc, y_loc, dropping
    stable = set()
    unstable = set()
    checked = []

    while len(queue) > 0:
        this = queue.pop(0)
        if this[2] and this not in checked:  # Falling
            droppable = [x[1] for x in clay.union(stable) if x[0] == this[0] and x[1] > this[1]]
            if len(droppable) > 0:
                blocked = min(droppable)
                unstable = unstable.union(set((this[0], x) for x in range(this[1], blocked)))
                queue.append((this[0], blocked-1, False))
            else:  # Falling out of the map
                unstable = unstable.union(set([(this[0], x) for x in range(this[1], max_y + 1)]))
        elif this not in checked:  # Not falling -> spreading
            clay_stable = clay.union(stable)

            # Spreading to the left: find distance i that can be spread to
            to_left, i, stop = [], 0, False
            while not stop:
                to_left.append((this[0]-i, this[1]))
                if (this[0]-i-1, this[1]) in clay or (this[0]-i, this[1]+1) not in clay_stable:
                    stop = True
                else:
                    i += 1

            # Spreading to the right: find distance j that can be spread to
            to_right, j, stop = [], 0, False
            while not stop:
                to_right.append((this[0] + j, this[1]))
                if (this[0] + j + 1, this[1]) in clay or (this[0] + j, this[1] + 1) not in clay_stable:
                    stop = True
                else:
                    j += 1

            # If in either direction we can fall, water is unstable and we fall.
            if (this[0] + j, this[1] + 1) not in clay_stable or (this[0]-i, this[1]+1) not in clay_stable:
                unstable = unstable.union(set(to_left + to_right))
                if (this[0] + j, this[1] + 1) not in clay_stable:
                    queue.append((this[0] + j, this[1], True))
                if (this[0] - i, this[1]+1) not in clay_stable:
                    queue.append((this[0] - i, this[1], True))
            else:  # Otherwise, water is stable and we can spread one level higher
                stable = stable.union(set(to_left + to_right))
                queue.append((this[0], this[1]-1, False))
        checked.append(this)
        unstable = unstable - stable

    result_part1 = len(stable) + len(unstable) - (min_y + source[1])
    result_part2 = len(stable)

    extra_out = {'Number of lineparts in input': len(data),
                 'Total amount of clay': len(clay),
                 'Area that we measure': (max_x - min_x + 1) * (max_y - min_y + 1),
                 'Coordinates of square containing the area': f"{(min_x, max_x)} by {(min_y, max_y)}"}

    return result_part1, result_part2, extra_out


if __name__ == "__main__":
    run_day(run_all, [1])
