from itertools import combinations, pairwise
from typing import Union
from util.util import ProcessInput, run_day


def run_all(example_run: Union[int, bool]):

    data = ProcessInput(example_run=example_run, day=9, year=2025).data
    data = [tuple([int(y) for y in x.split(',')]) for x in data]

    # Part 1
    # Simply finding the largest - could be written even shorter but this makes the idea clear.
    largest = 0
    for x,y in combinations(data,2):
        this = (abs(x[0]- y[0])+1)*(abs(x[1]-y[1])+1)
        if this > largest:
            largest = this

    result_part1 = largest

    # Part 2
    # If there is an intersection of the span with our candidate rectangle, then it is not fully in the span.
    # This assumes:
    # - In general, the rectangle is in the shape (required due to the same points being used for making the rectangle
    #   and the shape)
    # - There is no loop around without a gap (say, 5 to the right, 1 up, 5 to the left, with no gap in between) ->
    #   this happens to not happen for the data in this puzzle
    largest = 0
    for x1, y1 in combinations(data, 2):
        z1min, z1max = min(x1[0], y1[0]), max(x1[0], y1[0])
        z2min, z2max = min(x1[1], y1[1]), max(x1[1], y1[1])
        for x2, y2 in pairwise(data + [data[0]]):
            if not (max(x2[0], y2[0]) <= z1min or z1max <= min(x2[0], y2[0]) or
                    max(x2[1], y2[1]) <= z2min or z2max <= min(x2[1], y2[1])):
                break
        else:
            this = (z1max - z1min + 1) * (z2max - z2min + 1)
            if this > largest:
                largest = this

    # Speedup potential: heapify the combinations like in day 8 & stop for first that meets check
    # Generalization potential:
    #   - convert span into union of rectangles
    #   - for each candidate rectangle, check if it or its subrectangles are in each span-rectangle
    # Using rectangles for the span can speed up the check compared to having a massive list of each element.
    # Alternative to this: start with the smallest rectangle around all points, and subtract rectangles.

    # Idea of approach to convert span into union of rectangles:
    # - Need: util to add/subtract rectangles to a collection (like intervalues for intervals)
    # - Start with 1 pt
    # - Then iteratively add 2 pts
    #   - If going out: add rectangle(s); if going in: remove them.
    #   - Repeat until end of list

    result_part2 = largest

    extra_out = {'Number of rows in input': len(data),
                 'Number of candidate rectangles': int(len(data)*(len(data)-1)/2),
                 'Number of edges': len(data)}

    return result_part1, result_part2, extra_out


if __name__ == "__main__":
    run_day(run_all, [1])
