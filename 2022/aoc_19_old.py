import numpy as np
import z3
import functools
import itertools
from typing import Union
from util import timing
import tqdm


debug = False


def apply_resource_gathering(robots, resources):
    for i in range(len(robots)):
        resources[i] += robots[i]
    return resources


@functools.lru_cache(2**25)
def optimal_robot_choice(T, prices, robots, resources):

    if T == 1:  # You don't have to look at last day -> even if you can buy a new geode robot, it will not mine in time.
        return resources[3] + robots[3]

    # Improvement: if you can buy geode, buy geode. Will be true because of obsidian decision beforehand.
    if (prices[4] <= resources[0]) and (prices[5] <= resources[2]):  # Try: buy geode robot
        resources_i = apply_resource_gathering(robots, list(resources))
        robots_i = list(robots)  # TODO: This could be improved
        robots_i[3] += 1
        resources_i[0] -= prices[4]
        resources_i[2] -= prices[5]
        return optimal_robot_choice(T-1, prices, tuple(robots_i), tuple(resources_i))

    # Compare 4 situations (do nothing, or buy one of the non-geode robots).
    # Assumption: you would never buy 2 in the same minute, since it would be better to buy 1 earlier already.
    #   But: you could generate enough in 1 minute to buy 2 (in theory)

    # Try: do nothing
    resources_i = apply_resource_gathering(robots, list(resources))
    best = optimal_robot_choice(T-1, prices, robots, tuple(resources_i))

    # Try: buy ore robot
    if prices[0] <= resources[0]:
        resources_i = apply_resource_gathering(robots, list(resources))
        robots_i = list(robots)  # TODO: This could be improved
        robots_i[0] += 1
        resources_i[0] -= prices[0]
        curr = optimal_robot_choice(T-1, prices, tuple(robots_i), tuple(resources_i))
        best = curr if curr > best else best
    if prices[1] <= resources[0]:  # Try: buy clay robot
        resources_i = apply_resource_gathering(robots, list(resources))
        robots_i = list(robots)  # TODO: This could be improved
        robots_i[1] += 1
        resources_i[0] -= prices[1]
        curr = optimal_robot_choice(T-1, prices, tuple(robots_i), tuple(resources_i))
        best = curr if curr > best else best
    if (prices[2] <= resources[0]) and (prices[3] <= resources[1]):  # Try: buy obsidian robot
        resources_i = apply_resource_gathering(robots, list(resources))
        robots_i = list(robots)  # TODO: This could be improved
        robots_i[2] += 1
        resources_i[0] -= prices[2]
        resources_i[1] -= prices[3]
        curr = optimal_robot_choice(T-1, prices, tuple(robots_i), tuple(resources_i))
        best = curr if curr > best else best

    return best


def run_optimization(blueprints, T):
    best = []
    for bp in tqdm.tqdm(blueprints):
        prices = tuple(bp[1:])
        robots = (1, 0, 0, 0)
        resources = (0, 0, 0, 0)
        best.append(optimal_robot_choice(T, prices, robots, resources))
        print(f'\n{best}')
        optimal_robot_choice.cache_clear()  # New problem, new prices, no need to keep cache
    return best


@timing
def run_all(example_run: Union[int, bool]):

    file = f'aoc_19_exampledata{example_run}' if example_run else 'aoc_19_data'
    with open(file) as f:
        data = f.readlines()
    adj_data = [row.rstrip('\n') for row in data]

    blueprints = [[int(x) for x in row.replace('Blueprint ', '').replace(': Each ore robot costs', '').
                  replace('ore. Each clay robot costs ', '').replace('ore. Each obsidian robot costs ', '').
                  replace('ore and ', '').replace('clay. Each geode robot costs ', '').replace('ore and ', '').
                  replace(' obsidian.', '').split(' ')] for row in adj_data]

    best_part1 = 0 # run_optimization(blueprints, T=24)  # 10 mins
    result_part1 = 1262  # sum([(i+1) * best_part1[i] for i in range(len(best_part1))])
    best_part2 = run_optimization(blueprints[:3], T=32)
    result_part2 = sum(best_part2)

    print(f'\nResults for {f"example" if example_run else "my"} input{f" {example_run}" if example_run else ""}:')
    print(f' Result of part 1: {result_part1}')
    print(f' Result of part 2: {result_part2}')

    print(f'\nDescriptives: \n TODO \n')


if __name__ == "__main__":
    # [run_all(example_run=i) for i in [1]]
    run_all(example_run=False)  # 1220
