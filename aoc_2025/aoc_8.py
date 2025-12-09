import heapq
from itertools import combinations
from typing import Union
from util.util import ProcessInput, run_day


def run_all(example_run: Union[int, bool]):

    data = ProcessInput(example_run=example_run, day=8, year=2025).data

    # Process data into circuits and shortest distances
    boxes = [tuple([int(y) for y in x.split(',')]) for x in data]
    circuits = [{box} for box in boxes]
    distances = [(sum([(i[k] - j[k]) ** 2 for k in range(3)]), i, j) for i, j in combinations(boxes, 2)]
    heapq.heapify(distances)

    # Other variable declarations
    N = 1000 if not example_run else 10
    size_circuits = 0,0,0
    final_connections = ([0], [0])

    # Loop over the heaped distances
    for n in range(len(distances)):
        dist = heapq.heappop(distances)

        # For both elements, check in which circuit they are - if the same circuit, skip iteration
        i, j = dist[1], dist[2]
        find_i = [(nr, circ) for nr, circ in enumerate(circuits) if i in circ]
        find_j = [(nr, circ) for nr, circ in enumerate(circuits) if j in circ]
        if find_i == find_j:
            continue

        # If not the same circuit, join then together and add to circuits. Also remove the old ones.
        joined_circ = find_i[0][1].union(find_j[0][1])
        circuits.append(joined_circ)
        circuits.remove(find_i[0][1])
        circuits.remove(find_j[0][1])

        # After n steps, check size of largest circuits for part 1
        if n + 1 == N:
            size_circuits = sorted([len(x) for x in circuits], reverse=True)

        # Break when there is a single circuit while keeping the last connections made
        if len(circuits) == 1:
            final_connections = (i, j)
            break

    result_part1 = size_circuits[0] * size_circuits[1] * size_circuits[2]
    result_part2 = final_connections[0][0] * final_connections[1][0]

    extra_out = {'Number of boxes in input': len(data),
                 'Number of connections possible': int(len(data)*(len(data)-1)/2),
                 'Number of connections used': int(len(data)*(len(data)-1)/2) - len(distances),
                 'Number of connections left over': len(distances)}

    return result_part1, result_part2, extra_out


if __name__ == "__main__":
    run_day(run_all, [1])
