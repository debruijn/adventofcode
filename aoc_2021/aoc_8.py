import numpy as np

with open('aoc_8_data') as f:
    data = f.readlines()

input_vals = []
output_vals = []
for row in data:
    tmp = row.replace('\n', '').split('|')
    input_vals.append(tmp[0])
    output_vals.append(tmp[1])

count = 0
for row in output_vals:
    digits = row.split(' ')
    for digit in digits:
        if len(digit) in (2, 3, 4, 7):
            count = count + 1

print(count)

output_val = 0
for i in range(len(input_vals)):
    row = np.array([x for x in input_vals[i].split(' ') if x != ''])
    lenghts = np.array([len(digits) for digits in row])
    options = {j: [k for k in range(7)] for j in range(7)}
    solution = np.ones(10) * -1
    solution_dict = {}

    solution[lenghts == 2] = 1
    solution[lenghts == 3] = 7
    solution[lenghts == 4] = 4
    solution[lenghts == 7] = 8

    row_5 = row[lenghts == 5]
    sol_3 = row_5[np.where([all([d in x for d in row[solution == 7][0]]) for x in row_5])][0]
    row_5 = row_5[row_5 != sol_3]
    sol_5 = row_5[np.where([sum([d in x for d in row[solution == 4][0]]) == 3 for x in row_5])][0]
    row_5 = row_5[row_5 != sol_5]
    sol_2 = row_5[0]

    solution[row == sol_3] = 3
    solution[row == sol_5] = 5
    solution[row == sol_2] = 2

    row_6 = row[lenghts == 6]
    sol_9 = row_6[np.where([all([d in x for d in row[solution == 4][0]]) for x in row_6])][0]
    row_6 = row_6[row_6 != sol_9]
    sol_6 = row_6[np.where([all([d in x for d in row[solution == 5][0]]) for x in row_6])][0]
    row_6 = row_6[row_6 != sol_6]
    sol_0 = row_6[0]

    solution[row == sol_9] = 9
    solution[row == sol_6] = 6
    solution[row == sol_0] = 0

    for num in range(10):
        solution_dict.update({row[solution == num][0]: num})

    output_digits = np.array([x for x in output_vals[i].split(' ') if x != ''])
    sol = ''
    for digit in output_digits:
        index = [set(digit) == set(y) for y in solution_dict.keys()]
        sol = sol + str(np.where([set(digit) == set(y) for y in solution_dict.keys()])[0][0])

    output_val = output_val + int(sol)

print(output_val)



# notes:
# 7 in 3
# 4 deelt 3 met 5, en 2 met 2
# 4 in 9
# 5 in 6
# 0