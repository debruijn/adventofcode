import numpy as np

with open('aoc_10_data') as f:
    data = f.readlines()

open_char = np.array([x for x in '([{<'])
close_char = np.array([x for x in ')]}>'])
points = [3, 57, 1197, 25137]

sum_points = 0
for row in data:
    proc_row = ''
    row_done = False
    for char in row.replace('\n', ''):
        if not row_done:
            if char in open_char:
                proc_row = proc_row + char
            else:
                index = np.where(close_char == char)[0][0]
                if open_char[index] != proc_row[-1]:
                    sum_points = sum_points + points[index]
                    row_done = True
                else:
                    proc_row = proc_row[:-1]

print(sum_points)

# Part 2
points = [1, 2, 3, 4]

sum_points = []
for row in data:
    proc_row = ''
    row_done = False
    for char in row.replace('\n', ''):
        if not row_done:
            if char in open_char:
                proc_row = proc_row + char
            else:
                index = np.where(close_char == char)[0][0]
                if open_char[index] != proc_row[-1]:
                    row_done = True
                else:
                    proc_row = proc_row[:-1]
    if not row_done:
        iter_points = 0
        for char in proc_row[::-1]:
            index = np.where(open_char == char)[0][0]
            iter_points = 5*iter_points + points[index]
        sum_points.append(iter_points)

print(int(np.median(np.array(sum_points))))
