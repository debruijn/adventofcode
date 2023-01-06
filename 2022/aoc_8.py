import numpy as np

example_run = False
debug = False

file = 'aoc_8_exampledata' if example_run else 'aoc_8_data'
with open(file) as f:
    data = f.readlines()

adj_data = np.array([[int(y) for y in row.rstrip('\n')] for row in data])

I = adj_data.shape[0]
J = adj_data.shape[1]
sum_inner_visible = 0
for i in range(1, I - 1):
    for j in range(1, J - 1):
        visible = False
        if np.all(adj_data[0:i, j] < adj_data[i, j]):
            visible = True
        if np.all(adj_data[i + 1:I, j] < adj_data[i, j]):
            visible = True
        if np.all(adj_data[i, 0:j] < adj_data[i, j]):
            visible = True
        if np.all(adj_data[i, j + 1:J] < adj_data[i, j]):
            visible = True
        if visible:
            sum_inner_visible += 1

sum_outer_visible = 2 * I + 2 * J - 4
result_part1 = sum_inner_visible + sum_outer_visible

print(f'Result of part 1: {result_part1}')

max_scenic_score = 0
for i in range(1, I - 1):
    for j in range(1, J - 1):
        scenic_score = 1

        viewable = 0
        curr_max = -1
        for ii in range(i + 1, I):
            # if (adj_data[ii, j] >= curr_max) and (curr_max < adj_data[i, j]):   # <- How I think the challenge should have been
            if curr_max < adj_data[i, j]:   # <- What it actually was
                if debug:
                    print(f'  {adj_data[ii, j]}, {curr_max}')
                curr_max = adj_data[ii, j]
                viewable += 1
        scenic_score *= viewable

        viewable = 0
        curr_max = -1
        for ii in range(i - 1, -1, -1):
            # if (adj_data[ii, j] >= curr_max) and (curr_max < adj_data[i, j]):
            if curr_max < adj_data[i, j]:
                if debug:
                    print(f'  {adj_data[ii, j]}, {curr_max}')
                curr_max = adj_data[ii, j]
                viewable += 1
        scenic_score *= viewable

        viewable = 0
        curr_max = -1
        for jj in range(j + 1, J):
            # if (adj_data[i, jj] >= curr_max) and (curr_max < adj_data[i, j]):
            if curr_max < adj_data[i, j]:
                if debug:
                    print(f'  {adj_data[i, jj]}, {curr_max}')
                curr_max = adj_data[i, jj]
                viewable += 1
        scenic_score *= viewable

        viewable = 0
        curr_max = -1
        for jj in range(j - 1, -1, -1):
            # if (adj_data[i, jj] >= curr_max) and (curr_max < adj_data[i, j]):
            if curr_max < adj_data[i, j]:
                if debug:
                    print(f'  {adj_data[i, jj]}, {curr_max}')
                curr_max = adj_data[i, jj]
                viewable += 1
        scenic_score *= viewable

        if debug:
            print(f"{i},{j}: {adj_data[i, j]}, {scenic_score}")
            print('\n')
        if scenic_score > max_scenic_score:
            max_scenic_score = scenic_score

result_part2 = max_scenic_score

print(f'Result of part 2: {result_part2}')
