import numpy as np

with open('aoc_4_data') as f:
    data = f.readlines()

adj_data = [row.rstrip('\n') for row in data]
np_data = np.array([x.split(',') for x in adj_data])

sum_overlap = 0
for row in np_data:
    elf1 = [int(x) for x in row[0].split('-')]
    elf2 = [int(x) for x in row[1].split('-')]

    if (elf1[0] <= elf2[0] and elf1[1] >= elf2[1]) or (elf2[0] <= elf1[0] and elf2[1] >= elf1[1]):
        sum_overlap += 1

print(sum_overlap)


sum_overlap = 0
debug = False
for row in np_data:
    elf1 = [int(x) for x in row[0].split('-')]
    elf2 = [int(x) for x in row[1].split('-')]

    if (elf1[0] <= elf2[0] and elf1[1] >= elf2[0]) or (elf2[0] <= elf1[1] and elf2[1] >= elf1[1]) or \
            (elf1[0] <= elf2[1] and elf1[1] >= elf2[1]) or (elf2[0] <= elf1[0] and elf2[1] >= elf1[0]):
        if debug:
            print(f'Yes: {row}')
        sum_overlap += 1
    else:
        if debug:
            print(f'No: {row}')

print(sum_overlap)
