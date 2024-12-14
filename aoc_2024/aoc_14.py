from itertools import combinations
from typing import Union
from util.util import ProcessInput, run_day
from math import prod

def run_all(example_run: Union[int, bool]):

    # Input and minor processing
    data = ProcessInput(example_run=example_run, day=14, year=2024).data
    dims = (11, 7) if example_run else (101, 103)
    robots = [[tuple([int(y) for y in x[2:].split(',')]) for x in row.split(' ') ] for row in data]

    # Part 1: use % to directly calculate where each robot will be after N=100, and then find the quadrant.
    count_quadrants = [0]*4
    N = 100
    for robot in robots:
        loc = ((robot[0][0] + N * robot[1][0]) % dims[0], (robot[0][1] + N * robot[1][1]) % dims[1])
        if loc[0] == (dims[0]-1)/2 or loc[1] == (dims[1]-1)/2:
            continue
        if loc[0] > (dims[0]-1)/2:
            if loc[1] > (dims[1]-1)/2:
                count_quadrants[0] += 1
            else:
                count_quadrants[1] += 1
        else:
            if loc[1] > (dims[1]-1)/2:
                count_quadrants[2] += 1
            else:
                count_quadrants[3] += 1
    result_part1 = prod(count_quadrants)

    # Part 2: construct robot locs at each moment and print it.
    # - To avoid looking at each second, I use as metric the number of elements that are bordering another element -> if
    #   there is a picture, then hopefully that will be among the ones with many neighboring points.
    # - Based on the first 100 seconds, I could see that filtering at >200 would eliminate most iterations
    # - Running that until 10000 resulted in a few to scroll through and easily detect the picture
    # - I have now put the limit at 900 to only return that picture for my input - if you run it, you might need to
    #   tweak that number.
    plot_pictures = False

    # In hindsight, I might have been able to construct a metric based on the "safety value" from part 1 as well.
    # Other potential metrics: variance in points, or separately variance in x or y coordinates
    result_part2 = "TODO"
    if not example_run:
        for i in range(10000):
            locs = [((robot[0][0] + i * robot[1][0]) % dims[0], (robot[0][1] + i * robot[1][1]) % dims[1]) for robot in robots]

            count = 0
            for loc1, loc2 in combinations(locs, 2):
                if loc1 != loc2 and abs(loc1[0] - loc2[0]) <= 1 and abs(loc1[1] - loc2[1]) <= 1:
                    count += 1

            if count > 900:
                result_part2 = i

                if plot_pictures:
                    print(f"i={i}: {count}")
                    for row in range(dims[1]):
                        row_string = ""
                        for col in range(dims[0]):
                            if (col, row) in locs:
                                row_string += "#"
                            else:
                                row_string += ' '
                        print(row_string)
                    print("\n")

    extra_out = {'Number of robots in input': len(robots)}

    return result_part1, result_part2, extra_out


if __name__ == "__main__":
    run_day(run_all, [1])
