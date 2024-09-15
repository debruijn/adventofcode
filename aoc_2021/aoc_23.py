from collections import defaultdict
from functools import cache
from typing import Union
from util.util import ProcessInput, run_day

debug = False


def find_minimal_energy(data, part_2=False):
    # It works but don't ask how
    # Approach: priority queue (A* like) using lowerbound of required remaining steps to delay evaluating certain paths.
    # For each partial path that we evaluate, if there is a pod we can put on it's target location, just do that only to
    #   avoid unnecessary options (that step will happen anyway, and order doesn't matter at that point).
    # Only otherwise, generate all options of where each pod can move to on the hallway.
    # Warning: a lot of ugly "nr steps to move from x to y" calculations below, due to awkward definition of hallway

    t_data = [data[2], 'DCBA', 'DBAC', data[3]] if part_2 else [data[2], data[3]]

    @cache
    def get_lb_e_i(pod, i):
        if pod[0] == target[i] and pod[1] >= 0:
            return 0  # If pod is already at it's location -> set lb to 0
        if pod[0] in (-2, 4):  # If pod is on the outside, use a separate calculation for those two locations
            if pod[0] == -2:
                return costs[i] * (2 * (target[i] + 1) + 1)
            else:
                return costs[i] * (2 * (3 - target[i]) + 1 + 2)
        if pod[1] == -1:  # If pod is on the hallway but not on the outside
            if pod[0] < target[i]:
                return costs[i] * (2 * (target[i] - pod[0]))
            else:
                return costs[i] * (2 * (pod[0] - target[i] + 1))
        return costs[i] * (2 * abs(target[i] - pod[0]) + (pod[1] + 1) + 1)  # If pod is in another room than target

    @cache
    def get_lb_e(i_locs):
        # Lower bound to energy required to get to solution - ignore location of other pods
        return sum(get_lb_e_i(pod, i) for i, pod in enumerate(i_locs))

    # Location usage: j = 0, 1, 2, 3: in room i; j = -1: hallway location for i in -2, -1, ..., 3, 4
    locs = tuple([(i, j) for j in range(2 + (2*part_2)) for i in range(4)])
    cost_mapping = {'A': 1, 'B': 10, 'C': 100, 'D': 1000}
    costs = [cost_mapping[ele] for row in t_data for ele in row.replace(' ', '').replace('#', '')]
    target = [ord(ele) - ord('A') for row in t_data for ele in row.replace(' ', '').replace('#', '')]
    moved = (False,) * len(locs)
    queue = defaultdict(set)
    queue[get_lb_e(locs)].add((0, locs, moved))
    this_e = get_lb_e(locs)

    while len(queue) > 0:

        # Increase current energy level if none are left
        if len(queue[this_e]) == 0:
            del queue[this_e]
            this_e = min(x for x in queue.keys())
            if debug:
                print(f"Minimum answer is now {this_e}")
            continue

        # Pop from queue
        done_e, this_locs, this_moved = queue[this_e].pop()

        # Check if we have a solution
        count_correct = sum(target[i] == this_locs[i][0] and this_locs[i][1] >= 0 for i in range(len(this_locs)))
        if count_correct == len(this_locs):
            break

        # Check if any pod can go to target - just do that, don't generate others since for total order won't matter
        found_target = False
        for i, pod in enumerate(this_locs):
            if pod[1] == -1:
                if any(other == (target[i], 0) for other in this_locs):
                    continue  # No room in room
                if any(target[i] == other[0] != target[j] for j, other in enumerate(this_locs) if other[1] >= 0):
                    continue  # Another pod is in room and still has to leave
                if target[i] > pod[0]:
                    if any(pod[0] < other[0] < target[i] for other in this_locs if other[1] == -1):
                        continue  # blocked
                else:
                    if any(pod[0] > other[0] >= target[i] for other in this_locs if other[1] == -1):
                        continue  # blocked
                others_in_target = [other[1] for other in this_locs if other[0] == target[i] and other[1] >= 0]
                max_available = min(others_in_target, default=2+2*part_2) - 1
                if target[i] > pod[0]:
                    nr_steps = (target[i] - pod[0] + ((target[i] - pod[0]) if pod[0] >= 0 else target[i] + 1) +
                                max_available)
                else:
                    nr_steps = 1 + pod[0] - target[i] + min(pod[0], 3) - target[i] + 1 + max_available
                new_e = done_e + costs[i] * nr_steps
                new_locs = this_locs[:i] + ((target[i], max_available),) + this_locs[i+1:]
                found_target = True
                est_e = get_lb_e(new_locs)
                queue[new_e + est_e].add((new_e, new_locs, this_moved))
                break

        # If none can go to target, something needs to go to the hallway first, so generate all those options
        if not found_target:
            for i, pod in enumerate(this_locs):
                if pod[1] >= 0:
                    if pod[0] == target[i] and this_moved[i]:
                        continue  # already at target - can't move
                    if any(other[0] == pod[0] and other[1] < pod[1] for other in this_locs if other[1] != -1):
                        continue  # pod is not the top pod in the room
                    for j in range(-2, 5):
                        if j < pod[0]:
                            if not any(j <= other[0] < pod[0] for other in this_locs if other[1] == -1):
                                nr_steps = (1 + pod[1] + 1 + ((2 * (pod[0] - 1 - j))
                                                              if j >= 0 else (pod[0] - 1 - j + pod[0])))
                                new_e = done_e + costs[i] * nr_steps
                                new_locs = this_locs[:i] + ((j, -1),) + this_locs[i+1:]
                                new_moved = this_moved[:i] + (True,) + this_moved[i+1:]
                                est_e = get_lb_e(new_locs)
                                queue[new_e + est_e].add((new_e, new_locs, new_moved))
                        else:
                            if not any(j >= other[0] >= pod[0] for other in this_locs if other[1] == -1):
                                nr_steps = (1 + pod[1] + 1 + ((2 * (j - pod[0]))
                                                              if j <= 3 else (j - pod[0] + 3 - pod[0])))
                                new_e = done_e + costs[i] * nr_steps
                                new_locs = this_locs[:i] + ((j, -1),) + this_locs[i+1:]
                                new_moved = this_moved[:i] + (True,) + this_moved[i+1:]
                                est_e = get_lb_e(new_locs)
                                queue[new_e + est_e].add((new_e, new_locs, new_moved))

    return this_e


def run_all(example_run: Union[int, bool]):

    data = ProcessInput(example_run=example_run, day=23, year=2021).data

    result_part1 = find_minimal_energy(data)
    result_part2 = find_minimal_energy(data, part_2=True)

    return result_part1, result_part2, None


if __name__ == "__main__":
    run_day(run_all, [1])
