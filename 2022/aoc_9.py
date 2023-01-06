example_run = False
debug = False

file = 'aoc_9_exampledata2' if example_run else 'aoc_9_data'
with open(file) as f:
    data = f.readlines()

adj_data = [row.rstrip('\n') for row in data]

pos_H = [0, 0]
pos_T = pos_H.copy()

visited_pos = [tuple(pos_T.copy())]

for row in adj_data:
    direction = row[0]
    distance = int(row.split(' ')[1])

    for i in range(distance):
        if direction == 'R':
            pos_H = [pos_H[0]+1, pos_H[1]]
        if direction == 'L':
            pos_H = [pos_H[0]-1, pos_H[1]]
        if direction == 'U':
            pos_H = [pos_H[0], pos_H[1]+1]
        if direction == 'D':
            pos_H = [pos_H[0], pos_H[1]-1]

        if abs(pos_H[0] - pos_T[0])>1 or abs(pos_H[1] - pos_T[1])>1:
            if not pos_H[0] == pos_T[0]:
                pos_T0 = pos_T[0] + (pos_H[0] - pos_T[0]) / abs(pos_H[0] - pos_T[0])
            else:
                pos_T0 = pos_T[0]
            if not pos_H[1] == pos_T[1]:
                pos_T1 = pos_T[1] + (pos_H[1] - pos_T[1]) / abs(pos_H[1] - pos_T[1])
            else:
                pos_T1 = pos_T[1]
            pos_T = [pos_T0, pos_T1]

            visited_pos.append(tuple(pos_T))

if debug:
    print(visited_pos)


result_part1 = len(set(visited_pos))

print(f'Result of part 1: {result_part1}')

pos_H = [0, 0]
n_knots = 10
pos_T = pos_H.copy()
knots = [[0, 0] for i in range(n_knots)]

visited_pos = [tuple(pos_T.copy())]


def follow_prev(curr, prev):
    if abs(curr[0] - prev[0]) > 1 or abs(curr[1] - prev[1]) > 1:
        if not curr[0] == prev[0]:
            pos_T0 = prev[0] + (curr[0] - prev[0]) / abs(curr[0] - prev[0])
        else:
            pos_T0 = prev[0]
        if not curr[1] == prev[1]:
            pos_T1 = prev[1] + (curr[1] - prev[1]) / abs(curr[1] - prev[1])
        else:
            pos_T1 = prev[1]
        prev = [pos_T0, pos_T1]
    return prev


for row in adj_data:
    direction = row[0]
    distance = int(row.split(' ')[1])

    for _ in range(distance):
        if direction == 'R':
            pos_H = [pos_H[0]+1, pos_H[1]]
        if direction == 'L':
            pos_H = [pos_H[0]-1, pos_H[1]]
        if direction == 'U':
            pos_H = [pos_H[0], pos_H[1]+1]
        if direction == 'D':
            pos_H = [pos_H[0], pos_H[1]-1]

        knots[0] = pos_H

        for i in range(1, n_knots):
            knots[i] = follow_prev(knots[i-1], knots[i])

        visited_pos.append(tuple(knots[n_knots-1]))

if debug:
    print(visited_pos)


result_part2 = len(set(visited_pos))

print(f'Result of part 2: {result_part2}')
