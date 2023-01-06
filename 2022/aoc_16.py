from collections import defaultdict

from typing import Union

import numpy as np

from util import timing
import math
import copy

debug = False


def get_max_pressure(minutes_left, curr_valve, valves):
    # Part 1: don't loop by minute but reduce minutes_left with the full time it takes to the best action

    if minutes_left <= 0:
        return 0

    # Find valves that are still left to consider (so closed and feasible in time).
    # Note that I have filtered valves down to just those with flow_rate>0
    left = [(x, valves[x]['flow_rate'], valves[curr_valve]['connected'][x]) for x in valves[curr_valve]['connected']
            if (not valves[x]['open']) and (valves[curr_valve]['connected'][x] < minutes_left)]
    if len(left) == 0:
        return 0

    # For all valves that are left, consider what happens if you select them, and pick the best.
    #   Within this calculation, immediately assign all future pressure gain instead of calculating by minute
    all_max = []
    for valve in left:
        valves_copy = copy.deepcopy(valves)
        valves_copy[valve[0]]['open'] = True
        max_pressure_iter = get_max_pressure(minutes_left - valve[2] - 1, valve[0], valves_copy) + \
                            (minutes_left - valve[2] - 1) * valve[1]
        all_max.append(max_pressure_iter)

    return max(all_max)


def cached_dynamic_solution(u, t, mask, graph, rates, nodeId, cache):
    # For each bit mask (aka: puzzle still left to solve), location and remaining time, find the best next step.
    # Do this by finding the value for each step in the situation that creates.
    if t == 0:
        return 0
    if cache[u][t][mask] == -1:
        best = max(cached_dynamic_solution(v, t - 1, mask, graph, rates, nodeId, cache) for v in
                   graph[u])  # Find best direction to go
        u_bit = 1 << nodeId[u]  # Remove current point u from the puzzle -> it is assigned
        if u_bit & mask:
            best = max(best,
                       cached_dynamic_solution(u, t - 1, mask - u_bit, graph, rates, nodeId, cache) + rates[u] * (t - 1))
        cache[u][t][mask] = best
    return cache[u][t][mask]


def get_max_pressure_2(minutes, curr_valve, valves):
    # Convert input to more direct dicts
    rates = {x: valves[x]['flow_rate'] for x in valves}
    graph = {x: valves[x]['connect'] for x in valves}
    nodeId = defaultdict(lambda: len(nodeId))
    [nodeId[u] for u in rates if rates[u]]  # Only assign consecutive ids to non-zero rates
    ALL_MASK = (1 << len(nodeId)) - 1  # 1 * 2**len(nodeId) - 1  -> all unique states

    # Set initial best value for all unique states
    # If the same state happens in different solution paths, they will share the result without recalculating
    cache = defaultdict(lambda: [[-1 for _ in range(ALL_MASK + 1)] for _ in range(minutes + 1)])

    # Loop over all ways to divide the valves over human and elephant by adjusting the bit mask
    solution = max(cached_dynamic_solution(curr_valve, minutes, ALL_MASK - mask, graph, rates, nodeId, cache) +
               cached_dynamic_solution(curr_valve, minutes, mask, graph, rates, nodeId, cache)
               for mask in range(ALL_MASK + 1))

    n_considered = (np.array([cache[i1] for i1 in cache]) >= 0).sum()
    return solution, ALL_MASK, n_considered


@timing
def run_all(example_run: Union[int, bool]):
    file = f'aoc_16_exampledata{example_run}' if example_run else 'aoc_16_data'
    with open(file) as f:
        data = f.readlines()
    adj_data = [row.rstrip('\n') for row in data]

    valves = {}
    for row in adj_data:
        text = row.replace('tunnels', 'tunnel').replace('valves', 'valve').replace('leads', 'lead').replace('Valve ',
                                                                                                            ''). \
            replace(' has flow rate', '').replace(' tunnel lead to valve ', '').split(';')
        connect = text[1].split(', ')
        name = text[0].split('=')[0]
        flow_rate = int(text[0].split('=')[1])
        valve = {'name': name, 'connect': connect, 'flow_rate': flow_rate, 'open': False}
        valves.update({name: valve})

    # Loop over valves
    # - Find each one it connects to directly, set value to 1
    # - Find each one it connects to at 1 higher level, remove ones it is connected to, set value to 2
    # - Continue until connected to all
    for name in valves:
        valve = valves[name]
        connected = {name: 0}
        for name_i in valve['connect']:
            connected.update({name_i: 1})

        k = 1
        while len(connected) < len(valves):
            for name_i in [x for x in connected if connected[x] == k]:
                for name_j in [x for x in valves[name_i]['connect'] if x not in connected]:
                    connected.update({name_j: k + 1})
            k += 1

        valve.update({'connected': connected})

    for name in valves:
        valve = valves[name]

        for name_i in [x for x in valve['connected']]:
            if valves[name_i]['flow_rate'] == 0:
                del valve['connected'][name_i]

    rel_valves = [valve for valve in valves.items() if (valve[1]['flow_rate'] > 0) or (valve[0] == 'AA')]

    if debug:
        print(len(rel_valves))

    result_part1 = get_max_pressure(30, "AA", copy.deepcopy(valves))
    result_part2, ALL_MASK, considered_states = get_max_pressure_2(26, "AA", valves)

    print(f'Results for {f"example" if example_run else "my"} input{f" {example_run}" if example_run else ""}:')
    print(f' Result of part 1: {result_part1}')
    print(f' Result of part 2: {result_part2}')

    print(f'\nDescriptives: \n Number valves: {len(valves)} \n'
          f' Number relevant valves (flow rate > 0): {len(rel_valves)} \n'
          f' All possible routes of relevant valves, ignoring time constraint: '
          f'{math.factorial(len(rel_valves) - 1)} \n'
          f' All possible puzzle versions: {ALL_MASK} \n'
          f' Puzzle states that are considered: {considered_states}\n')


if __name__ == "__main__":
    [run_all(example_run=i) for i in [1, 2]]
    run_all(example_run=False)
