from typing import Union
from util.util import ProcessInput, run_day, isnumeric


def get_distance(fly_t=10, fly_s=10, rest_t=10, time=2503):
    # Recurring loop for each reindeer after fly_t+rest_t: full cycle of flying+resting, doing distance fly_t * fly_s.
    # The given time will likely not result in a fully finished loop, so for the remainder see if that is in the
    # flying or the resting part (see `final_d` below).
    loop_d = fly_t * fly_s
    loop_t = fly_t + rest_t
    n_loops = time // loop_t
    final_d = loop_d if time % loop_t > fly_t else fly_s * (time % loop_t)
    return n_loops * loop_d + final_d


def run_all(example_run: Union[int, bool]):

    data = ProcessInput(example_run=example_run, day=14, year=2015).data

    T = 1000 if example_run else 2503

    # Part 1: use function above to directly calculate how far each reindeer is at time T, and take the maximum.
    distances = []
    nums_all = dict()
    for row in data:
        nums = [int(x) for x in row.split() if isnumeric(x)]
        nums_all[row.split()[0]] = nums
        distances.append(get_distance(nums[1], nums[0], nums[2], time=T))

    result_part1 = max(distances)

    # Part 2
    # An example of "I would not use this approach for part 2 if I hadn't done part 1". For each t, apply the above
    # function to see who has the biggest distance (which recalculates all previous steps as well).
    # Alternative approach: actually keep track of the current distance for all reindeers at time t during the loop.
    # Might not be faster, but would make more sense.
    points = {k: 0 for k in nums_all.keys()}
    for t in range(1, T+1):
        distances = {}
        for name, nums in nums_all.items():
            distances[name] = get_distance(nums[1], nums[0], nums[2], time=t)
        max_distance = max(distances.values())
        winners = [x for x in distances.keys() if distances[x] == max_distance]  # To account for ties
        for winner in winners:
            points[winner] += 1

    result_part2 = max(points.values())

    extra_out = {'Number of reindeers in the race': len(data),
                 'Full points distribution': points,
                 'Number of tied points': sum(points.values()) - T}

    return result_part1, result_part2, extra_out


if __name__ == "__main__":
    run_day(run_all, [1])
