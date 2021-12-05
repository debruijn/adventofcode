with open('aoc_2_data') as f:
    data = f.readlines()

pos = 0
depth = 0

for row in data:
    if row.startswith('forward'):
        pos += int(row.lstrip('forward '))
    elif row.startswith('down'):
        depth += int(row.lstrip('down '))
    else:
        depth -= int(row.lstrip('up '))

print(pos)
print(depth)
print(pos*depth)

## Part 2
pos = 0
depth = 0
aim = 0

for row in data:
    if row.startswith('forward'):
        pos += int(row.lstrip('forward '))
        depth += int(row.lstrip('forward ')) * aim
    elif row.startswith('down'):
        aim += int(row.lstrip('down '))
    else:
        aim -= int(row.lstrip('up '))

print(pos)
print(depth)
print(aim)
print(pos*depth)
