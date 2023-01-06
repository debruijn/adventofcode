import numpy as np

example_run = False
phase = 2
debug = False

file = 'aoc_5_exampledata' if example_run else 'aoc_5_data'
with open(file) as f:
    data = f.readlines()

adj_data = [row.rstrip('\n') for row in data]
break_line = np.where([x == '' for x in adj_data])[0][0]
first_instr = break_line + 1
nr_stacks = max([int(x) for x in adj_data[break_line-1].split(' ') if x != ''])
stack_data = adj_data[:break_line-1]
stack_data = [stack_data[i] for i in range(break_line-2, -1, -1)]

stacks = [[] for _ in range(nr_stacks)]
for row in stack_data:
    new_crates = [row[i] for i in range(1, len(row), 4)]
    [stacks[i].append(new_crates[i]) for i in range(0, len(new_crates)) if new_crates[i] != ' ']
    if debug:
        print(new_crates)
        print(stacks)

adj_data = adj_data[first_instr:]

for row in adj_data:
    move = int(row.split('move ')[1].split(' from')[0])
    from_ind = int(row.split('from ')[1].split(' to')[0]) - 1
    to_ind = int(row.split('to ')[1]) - 1

    if debug:
        print(stacks)
        print(f'{move}, {from_ind}, {to_ind}')

    move_stack = stacks[from_ind][-move:]
    stacks[from_ind] = stacks[from_ind][:-move]
    move_stack = [move_stack[i] for i in range(move-1, -1, -1)] if phase == 1 else move_stack
    [stacks[to_ind].append(x) for x in move_stack]


if debug:
    print(stacks)
top = [x[-1:] for x in stacks]
print(top)
