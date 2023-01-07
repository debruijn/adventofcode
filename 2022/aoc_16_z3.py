from collections import defaultdict
from typing import Union
from util.util import timing
import math
import z3

debug = False


# Improvement ideas:
# - Use bool instead of Int ->  Use if(bool_var, 1, 0) for sums, if needed (or to_int)
# - Remove the "start" variable from a lot of computations (or as variable!!)
# - Rewrite to single variable over Time (so x_AA = 5 means AA is turned on at 5) <-- This!!
# - Cam we also have some not selected at all? (0<=T<=30 or T==999)

def solve_with_z3_integers(valves, rel_valves, T=30, start="AA", N=1):

    rates = {x[0]: valves[x[0]]['flow_rate'] for x in rel_valves}
    nodeId = defaultdict(lambda: len(nodeId))
    [nodeId[u] for u in rates if rates[u] or u == start]
    reverse_id = {nodeId[x]: x for x in nodeId}
    V = len(nodeId)

    opt = z3.Optimize()
    total_pressure = z3.Int('total_pressure')
    X = [[z3.Int(f"x_{p}_{reverse_id[i]}")
          for i in range(V)]
         for p in range(N)]  # V x T

    # Every valve is turned on only once max on a given time by a given person
    [[opt.add(X[p][i] >= 0, X[p][i] <= T) for i in range(V)] for p in range(N)]   # TODO: skip AA in loop
    # [[opt.add(X[p][i] >= 0) for i in range(V)] for p in range(N)]   # TODO: skip AA in loop
    assert opt.check() == z3.sat

    # Every valve is only turned on once max across time and people; ignore last time period due to not having value
    [[[opt.add(z3.Xor(X[p][i] < T, X[q][i] < T)) for q in range(p+1, N)] for p in range(0, N-1)]
     for i in range(V) if i != nodeId[start]]
    assert opt.check() == z3.sat

    # Every person starts at start point
    [opt.add(X[p][nodeId[start]] == 0) for p in range(N)]
    assert opt.check() == z3.sat

    for p in range(N):

        i = nodeId[start]
        for j in [x for x in reverse_id if x != i]:  # x != i
            dist = rel_valves[i][1]['connected'][reverse_id[j]]
            opt.add(X[p][j] >= min(T, dist+1))
            assert opt.check() == z3.sat

        for i in [x for x in reverse_id if x != nodeId[start]]:  # Can do: if i == nodeId[start], only check for t=0.
            for j in [x for x in reverse_id if x > i and x != nodeId[start]]:  # x != i
                dist = rel_valves[i][1]['connected'][reverse_id[j]]
                opt.add(z3.Or(z3.Or(X[p][j] - X[p][i] >= dist + 1,
                                    X[p][j] == T),
                              z3.Or(X[p][j] - X[p][i] <= -dist - 1,
                                    X[p][i] == T)))
                assert opt.check() == z3.sat

    opt.add(total_pressure == sum([sum([(T - X[p][i]) * rates[reverse_id[i]] for i in range(V)]) for p in range(N)]))

    h = opt.maximize(total_pressure)
    opt.check()
    # s.upper(h)
    if debug:
        print(opt)
    model = opt.model()

    if debug or True:
        for d in model.decls():
            if (model[d].as_long() > 0) and (model[d].as_long() < T):
                print(f"{d.name()}: {model[d].as_long()}")

    return model[total_pressure].as_long()


def solve_with_z3(valves, rel_valves, T=30, start="AA", N=1):
    rates = {x[0]: valves[x[0]]['flow_rate'] for x in rel_valves}
    nodeId = defaultdict(lambda: len(nodeId))
    [nodeId[u] for u in rates if rates[u] or u == start]
    reverse_id = {nodeId[x]: x for x in nodeId}
    added_pressure = [[rates[reverse_id[i]] * (T - t) for t in range(T + 1)] for i in range(len(nodeId))]

    opt = z3.Optimize()
    total_pressure = z3.Int('total_pressure')
    X = [[[z3.Int(f"x_{p}_{reverse_id[i]}_{t}") for t in range(T + 1)]
          for i in range(len(rel_valves))]
         for p in range(N)]  # V x T

    # Every valve is turned on only once max on a given time by a given person
    [[[opt.add(X[p][i][t] >= 0) for t in range(T + 1)] for i in range(len(nodeId))] for p in
     range(N)]

    # Every valve is only turned on once max across time and people; ignore first time period
    [opt.add(sum([sum(X[p][i][1:]) for p in range(N)]) <= 1) for i in range(len(X[0]))]

    # Every person starts at start point
    [opt.add(X[p][nodeId[start]][0] == 1) for p in range(N)]

    for p in range(N):

        i = nodeId[start]
        for j in [x for x in reverse_id if x != i]:  # x != i
            dist = rel_valves[i][1]['connected'][reverse_id[j]]
            s_range = range(min(T, dist + 1))
            for s in s_range:
                # No points can be visited close enough to another that is visited
                opt.add(X[p][j][s] == 0)

        for i in [x for x in reverse_id if x != nodeId[start]]:  # Can do: if i == nodeId[start], only check for t=0.
            for t in range(1, T + 1):
                for j in [x for x in reverse_id if x > i and x != nodeId[start]]:  # x != i
                    dist = rel_valves[i][1]['connected'][reverse_id[j]]
                    s_range = range(max(0, t - dist), min(T, t + dist + 1))
                    for s in s_range:
                        # No points can be visited close enough to another that is visited
                        opt.add(z3.Not(z3.And(X[p][i][t] == 1, X[p][j][s] == 1)))

    opt.add(total_pressure == sum([sum([sum([X[p][i][t] for p in range(N)]) * added_pressure[i][t]
                                        for t in range(T + 1)])
                                   for i in range(len(nodeId))]))

    h = opt.maximize(total_pressure)
    opt.check()
    # s.upper(h)
    if debug:
        print(opt)
    model = opt.model()

    if debug or True:
        for d in model.decls():
            if model[d].as_long() > 0:
                print(f"{d.name()}: {model[d].as_long()}")

    return model[total_pressure].as_long()


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

    result_part1 = solve_with_z3_integers(valves, rel_valves, T=30, start="AA", N=1)

    print(f'Results for {f"example" if example_run else "my"} input{f" {example_run}" if example_run else ""}:')
    print(f' Result of part 1: {result_part1}')
    result_part2 = solve_with_z3_integers(valves, rel_valves, T=26, start="AA", N=2)
    print(f' Result of part 2: {result_part2}')

    print(f'\nDescriptives: \n Number valves: {len(valves)} \n'
          f' Number relevant valves (flow rate > 0): {len(rel_valves)} \n'
          f' All possible routes of relevant valves, ignoring time constraint: '
          f'{math.factorial(len(rel_valves) - 1)} \n')
    # f' All possible puzzle versions: {ALL_MASK} \n'
    # f' Puzzle states that are considered: {considered_states}\n')


if __name__ == "__main__":
    [run_all(example_run=i) for i in [1]]
    run_all(example_run=False)
