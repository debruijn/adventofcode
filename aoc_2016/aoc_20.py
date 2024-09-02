from typing import Union
from util.util import ProcessInput, run_day


def run_all(example_run: Union[int, bool]):

    data = ProcessInput(example_run=example_run, day=20, year=2016).data

    class IPRange:
        # Simplified version of my `intervalues` package. This could have been done without a class but after doing
        # `intervalues` I can't resist the urge. :) The overhead in this case is minimal, and the clarity in information
        # processing is worth it imo.
        def __init__(self, low=0, high=4294967295):
            self.range = [[low, high]]  # At first the full spectrum is allowed

        def __isub__(self, other):  # Only feature that is needed in this case
            new_ranges = []  # Could be done more efficiently - see `intervalues.combine_intervals()` :)
            for rng in self.range:
                if rng[1] < other[0]:
                    new_ranges.append(rng)
                    continue
                if rng[0] > other[1]:
                    new_ranges.append(rng)
                    continue
                if other[0] < rng[0] < other[1] and other[0] < rng[1] < other[1]:
                    continue
                if rng[0] < other[0]:
                    new_ranges.append([rng[0], other[0] - 1])
                if rng[1] > other[1]:
                    new_ranges.append([other[1] + 1, rng[1]])
            self.range = new_ranges
            return self

    ranges = IPRange(high=9) if example_run else IPRange()
    for row in data:
        ranges -= [int(x) for x in row.split('-')]

    result_part1 = ranges.range[0][0]  # Ranges are automatically in order, so lowest val is lowerbound of first range
    result_part2 = sum(x[1] - x[0] + 1 for x in ranges.range)

    extra_out = {'Number of disallowed IP ranges in input': len(data),
                 'Number of subranges remaining in the end:': len(ranges.range)}

    return result_part1, result_part2, extra_out


if __name__ == "__main__":
    run_day(run_all, [1])
