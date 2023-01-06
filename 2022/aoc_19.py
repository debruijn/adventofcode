import itertools
from typing import Union
from util import timing
import tqdm


debug = False


def sort_heuristic(state):
    # Rough guess for sorting: give each resource weight to cost of robot converted to ores (state[1] = prices)
    clay_price = state[1][1]
    obsidian_price = (state[1][3]*clay_price + state[1][2])
    geode_price = (state[1][5]*obsidian_price + state[1][4])

    # Then calculate rough value of state by looking at total collected resources (no matter what they have been spent
    # on) multiplied by these values. (state[3] = cum_resources)
    return geode_price * state[3][3] + obsidian_price * state[3][2] + clay_price * state[3][1] + state[3][0]


def queue_trim(queue):

    # Remove those that are the same
    for i, j in itertools.combinations(queue, 2):
        if i in queue and j in queue:
            tmp1 = i[2] + i[4]
            tmp2 = j[2] + j[4]
            if all(tmp1[k] <= tmp2[k] for k in range(len(tmp1))) and any(tmp1[k] < tmp2[k] for k in range(len(tmp1))):
                queue.pop(queue.index(i))
            elif all(tmp2[k] <= tmp1[k] for k in range(len(tmp1))) and any(tmp2[k] < tmp1[k] for k in range(len(tmp1))):
                queue.pop(queue.index(j))
            elif all(tmp2[k] == tmp1[k] for k in range(len(tmp1))):
                queue.pop(queue.index(i))
    return queue


def optimal_robot_choice(T, prices, robots, resources, keep_queue, trim_queue):
    # BF algorithm that trims the queue for each T, so only consider {keep_queue} "most likely" candidates.
    # Max calculations: T*keep_queue

    # New candidates are generated in the following way:
    # - Do nothing: same robots, increase resources, decrease T
    # - Buy a robot: robots + new one, increase resources but reduce by price, decrease T

    queue = list()
    default_to_check = (True,)*4
    queue.append((T, prices, robots, resources, resources, default_to_check))
    curr_depth = T
    best = 0

    while queue:
        t, prices, robots, cum_resources, resources, to_check = queue.pop(0)

        if t < curr_depth:
            if debug:
                print(f'{curr_depth}: {len(queue)}')

            # TODO: experiment with dropping all elements from queue that are clearly worse than some other
            #   (so resources and robots not higher and at least one smaller than at least one other state)
            #   (oapackage or own implementation)
            # We need to sort our queue and then keep top to not let it explode
            if len(queue) > keep_queue:
                queue.sort(key=sort_heuristic, reverse=True)  # Could convert to set; unlikely to be relevant here
                queue = queue[:keep_queue]
            if trim_queue:  # Can also do this before the heuristic
                queue = queue_trim(queue)
            if debug:
                print(f'       {len(queue)}')
            curr_depth = t

        if t == 1:  # Do the T=1 trick: building a robot at T=1 doesn't matter
            best = resources[3] + robots[3] if resources[3] + robots[3] > best else best
            continue

        # Additional resources due to existing robots - relevant for each case below
        new_cum_mined = tuple([cum_resources[i] + robots[i] for i in range(4)])
        new_resources = tuple([resources[i] + robots[i] for i in range(4)])

        # Add to queue: we do nothing
        to_check_pass = (prices[0] > resources[0],
                         prices[1] > resources[0],
                         (prices[2] > resources[0]) or (prices[3] > resources[1]),
                         (prices[4] > resources[0]) or (prices[5] > resources[2]))
        queue.append((t - 1, prices, robots, new_cum_mined, new_resources, to_check_pass))

        # For each robot type, add to queue: build a robot of this type, if we can afford them
        # Assumes that we never buy multiple robots in one minute -> T is low enough that this works out
        if to_check[0] and (prices[0] <= resources[0]):  # Ore robot
            robots_i = list(robots)
            robots_i[0] += 1
            resources_i = list(new_resources)
            resources_i[0] -= prices[0]
            queue.append((t-1, prices, tuple(robots_i), new_cum_mined, tuple(resources_i), default_to_check))
        if to_check[1] and (prices[1] <= resources[0]):  # Clay robot
            robots_i = list(robots)
            robots_i[1] += 1
            resources_i = list(new_resources)
            resources_i[0] -= prices[1]
            queue.append((t - 1, prices, tuple(robots_i), new_cum_mined, tuple(resources_i), default_to_check))
        if to_check[2] and (prices[2] <= resources[0]) and (prices[3] <= resources[1]):  # Obsidian robot
            robots_i = list(robots)
            robots_i[2] += 1
            resources_i = list(new_resources)
            resources_i[0] -= prices[2]
            resources_i[1] -= prices[3]
            queue.append((t - 1, prices, tuple(robots_i), new_cum_mined, tuple(resources_i), default_to_check))
        if to_check[3] and (prices[4] <= resources[0]) and (prices[5] <= resources[2]):  # Geode robot
            robots_i = list(robots)
            robots_i[3] += 1
            resources_i = list(new_resources)
            resources_i[0] -= prices[4]
            resources_i[2] -= prices[5]
            queue.append((t - 1, prices, tuple(robots_i), new_cum_mined, tuple(resources_i), default_to_check))

    return best


def run_optimization(blueprints, T, keep_queue=500, trim_queue=False):
    best = []
    for bp in tqdm.tqdm(blueprints):
        prices = tuple(bp[1:])
        robots = (1, 0, 0, 0)
        resources = (0, 0, 0, 0)
        best.append(optimal_robot_choice(T, prices, robots, resources, keep_queue=keep_queue, trim_queue=trim_queue))
        if debug:
            print(f'\n{best}')
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

    best_part1 = run_optimization(blueprints, T=24, keep_queue=50, trim_queue=False)  # 10 mins
    result_part1 = sum([(i+1) * best_part1[i] for i in range(len(best_part1))])
    best_part2 = run_optimization(blueprints[:3], T=32, keep_queue=250, trim_queue=False)
    best_part2 = run_optimization(blueprints, T=32, keep_queue=250, trim_queue=True)
    part2_prod = 1
    for x in best_part2:
        part2_prod *= x
    result_part2 = part2_prod

    print(f'\nResults for {f"example" if example_run else "my"} input{f" {example_run}" if example_run else ""}:')
    print(f' Result of part 1: {result_part1}')
    print(f' Result of part 2: {result_part2}')


if __name__ == "__main__":
    [run_all(example_run=i) for i in [1]]
    run_all(example_run=False)
