import re
import numpy as np

example_run = False
debug = False

file = 'aoc_10_exampledata' if example_run else 'aoc_10_data'
with open(file) as f:
    data = f.readlines()

adj_data = [row.rstrip('\n') for row in data]

reg_value = 1
cycle = 0
signal_all = [0]
get_res = [20, 60, 100, 140, 180, 220]

for row in adj_data:
    if row.startswith('noop'):
        cycle += 1
        signal = cycle * reg_value
        signal_all.append(signal)
    else:
        value = int(row.replace('addx ', ''))

        cycle += 1
        signal = cycle * reg_value
        signal_all.append(signal)

        cycle += 1
        signal = cycle * reg_value
        signal_all.append(signal)
        reg_value += value

    if debug:
        print(f'{cycle}: {reg_value}')

if debug:
    print('\n')

result_part1 = 0
for i in get_res:
    if debug:
        print(signal_all[i])
    result_part1 += signal_all[i]  # Weird way of taking sum; did this because of debug statement above

print(f'Result of part 1: {result_part1}')


reg_value = 1
cycle = 0
signal_all = [0]
crt_print = []
width = 40


def append_crt(reg_value, cycle):
    if abs(reg_value - np.remainder(cycle, width)) <= 1:
        crt_print.append('#')
    else:
        crt_print.append('.')


for row in adj_data:
    if row.startswith('noop'):
        append_crt(reg_value, cycle)
        cycle += 1
    else:
        append_crt(reg_value, cycle)
        append_crt(reg_value, cycle+1)
        cycle += 2
        value = int(row.replace('addx ', ''))
        reg_value += value
    if debug:
        print(f'{cycle}: {reg_value}')

long_string = ''.join(crt_print)
result_part2 = re.findall('.{1,40}', long_string)  # Experimented with splitting with regex

print(f'Result of part 2:')
for line in result_part2:
    print(line)
