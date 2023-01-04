import numpy as np
import matplotlib.pyplot as plt

with open('aoc_13_data') as f:
    data = f.readlines()

data = np.array([row.replace('\n', '') for row in data])

data_folds = [row.replace('fold along ', '') for row in data if row.startswith('fold along')]
data_dots = np.array([[int(x) for x in row.split(',')] for row in data if row != '' and not row.startswith('fold along')])

for fold in data_folds:

    new_data_dots = []

    fold_nr = int(fold.replace('y=', '').replace('x=', ''))
    for dots in data_dots:
        if fold.startswith('y='):
            if dots[1] > fold_nr:
                dots = np.array([dots[0], fold_nr - (dots[1] - fold_nr)])
        else:
            if dots[0] > fold_nr:
                dots = np.array([fold_nr - (dots[0] - fold_nr), dots[1]])
        new_data_dots.append(dots)

    data_dots = np.unique(np.array(new_data_dots), axis=0)

print(len(data_dots))
print(data_dots)


plt.plot(data_dots[:, 0], -data_dots[:, 1], 'ro')
plt.axis([-1, data_dots[:, 0].max()+1, -data_dots[:, 1].max()-1, 1])
plt.show()
