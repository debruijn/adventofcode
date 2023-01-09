example_run = False
debug = False

file = 'aoc_9_exampledata2' if example_run else 'aoc_9_data'
with open(file) as f:
    data = f.readlines()

adj_data = [row.rstrip('\n') for row in data]


def follow_prev(curr, prev):
    if abs(curr[0] - prev[0]) > 1 or abs(curr[1] - prev[1]) > 1:
        pos_T0 = prev[0] + (curr[0] - prev[0]) / abs(curr[0] - prev[0]) if not curr[0] == prev[0] else prev[0]
        pos_T1 = prev[1] + (curr[1] - prev[1]) / abs(curr[1] - prev[1]) if not curr[1] == prev[1] else prev[1]
        prev = [pos_T0, pos_T1]
    return prev


def track_knots(data, n_knots, tracked_knots):
    pos_H = [0, 0]
    pos_T = pos_H.copy()
    knots = [[0, 0] for _ in range(n_knots)]

    visited_pos = {i: {tuple(pos_T.copy())} for i in tracked_knots}

    for row in data:
        direction = row[0]
        distance = int(row.split(' ')[1])

        for _ in range(distance):
            pos_H = [pos_H[0]+1, pos_H[1]] if direction == 'R' else pos_H
            pos_H = [pos_H[0]-1, pos_H[1]] if direction == 'L' else pos_H
            pos_H = [pos_H[0], pos_H[1]+1] if direction == 'U' else pos_H
            pos_H = [pos_H[0], pos_H[1]-1] if direction == 'D' else pos_H

            knots[0] = pos_H
            for i in range(1, n_knots):
                knots[i] = follow_prev(knots[i-1], knots[i])

            for i in tracked_knots:
                visited_pos[i].add(tuple(knots[i - 1]))

    if debug:
        print(visited_pos)

    return visited_pos


visited_pos = track_knots(adj_data, 2, [2])
result_part1 = len(visited_pos[2])
print(f'Result of part 1: {result_part1}')

visited_pos = track_knots(adj_data, 10, [2, 10])
result_part1 = len(visited_pos[2])
result_part2 = len(visited_pos[10])
print(f'Result of part 1 and 2: {result_part1} and {result_part2}')

nr_knots = 100
visited_pos = track_knots(adj_data, nr_knots, range(1, nr_knots+1))
print('Number of unique positions for each knot:')
for knot in range(1, nr_knots+1):
    print(f'    knot {knot}: {len(visited_pos[knot])}')

print('Difference of unique positions for each knot compared with previous:')
for knot in range(1, nr_knots):
    print(f'    knot_{knot} - knot_{knot+1}: {len(visited_pos[knot]) - len(visited_pos[knot+1])}')

print('Ratio of unique positions for each knot compared with previous:')
for knot in range(1, nr_knots):
    print(f'    knot_{knot} / knot_{knot+1}: {len(visited_pos[knot]) / len(visited_pos[knot+1]):.3f}')
