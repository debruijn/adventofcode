import numpy as np

with open('aoc_12_data') as f:
    data = f.readlines()

data = np.array([row.replace('\n', '') for row in data])


def take_step(point, path_iter):
    point_segments = [segment for segment in segments if point in segment]
    paths_iter = []
    for segment in point_segments:
        other_point = [point_i for point_i in segment if point_i != point][0]
        if other_point == "end":
            this_path = path_iter.copy()
            this_path.extend([point, other_point])
            paths_iter.append(this_path)
        elif other_point == 'start':
            pass
        elif other_point.islower() and other_point in path_iter:
            this_path = path_iter.copy()
            this_path.extend([point, other_point])
            this_path = [x for x in this_path if x.islower()]
            if len(set([x for x in this_path if this_path.count(x) > 1])) > 1:
                pass
            elif len(set([x for x in this_path if this_path.count(x) > 2])) > 0:
                pass
            else:
                new_path = path_iter.copy()
                new_path.append(point)
                new_paths = take_step(other_point, new_path)
                paths_iter.extend(new_paths)
        else:
            new_path = path_iter.copy()
            new_path.append(point)
            new_paths = take_step(other_point, new_path)
            paths_iter.extend(new_paths)

    return paths_iter


# Find all unique points
segments = [x.split('-') for x in data]
start_segments = [segment for segment in segments if 'start' in segment]


paths = []
for start in start_segments:
    curr_point = [point for point in start if point != 'start'][0]
    path = ['start']

    paths.extend(take_step(curr_point, path))

for path in paths:
    print(path)
print(len(paths))
