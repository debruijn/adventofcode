from typing import Union
from util.util import ProcessInput, run_day


def run_all(example_run: Union[int, bool]):

    data = ProcessInput(example_run=example_run, day=24, year=2017).data

    component = [tuple(int(x) for x in row.split('/')) for row in data]

    start = (0, 0, ())  # Order: Last pin, sum of counts, component used
    queue = [start]

    best = start[1]
    best_among_longest = best
    longest = 0
    count_valid_bridges = -1  # -1 because start doesn't count according to example
    while len(queue) > 0:
        this = queue.pop()
        count_valid_bridges += 1

        for cmpt in component:
            if cmpt in this[2]:
                continue
            if cmpt[0] == this[0]:
                queue.append((cmpt[1], this[1] + cmpt[0] + cmpt[1], (*this[2], cmpt)))
            elif cmpt[1] == this[0]:
                queue.append((cmpt[0], this[1] + cmpt[0] + cmpt[1], (*this[2], cmpt)))

        if len(this[2]) > longest:
            best_among_longest = this[1]
            longest = len(this[2])
        elif len(this[2]) == longest:
            best_among_longest = this[1] if this[1] > best_among_longest else best_among_longest

        best = this[1] if this[1] > best else best

    result_part1 = best
    result_part2 = best_among_longest

    extra_out = {'Number of components in input': len(data),
                 'Number of valid bridges to make': count_valid_bridges}

    return result_part1, result_part2, extra_out


if __name__ == "__main__":
    run_day(run_all, [1])
