import numpy as np


def run_all(example_run):

    file = 'aoc_12_exampledata' if example_run else 'aoc_12_data'
    with open(file) as f:
        data = f.readlines()

    adj_data = np.array([[element for element in row.rstrip('\n')] for row in data])

    start = np.where(adj_data == 'S')
    end = np.where(adj_data == 'E')

    adj_data[start] = 'a'
    adj_data[end] = 'z'

    elevation = np.array([[ord(element) for element in row] for row in adj_data])

    distances = np.ones_like(elevation) * np.inf
    distances[end] = 0
    distance_backup = [0]

    I, J = elevation.shape
    n_iter = 0

    while np.any(distances != distance_backup):
        distance_backup = distances.copy()
        n_iter += 1

        for i in range(I):
            for j in range(J):
                curr_elevation = elevation[i, j]
                indices = []
                if i > 0:
                    indices.append([i - 1, j])
                if i < I-1:
                    indices.append([i + 1, j])
                if j > 0:
                    indices.append([i, j - 1])
                if j < J-1:
                    indices.append([i, j + 1])
                distances_iter = [distances[ind[0], ind[1]] for ind in indices]
                elevation_iter = [elevation[ind[0], ind[1]] for ind in indices]
                best_distance = distances[i, j]

                for k in range(len(indices)):
                    if (elevation_iter[k] <= curr_elevation + 1) & (distances_iter[k] < best_distance - 1):
                        best_distance = distances_iter[k] + 1
                distances[i, j] = best_distance

    result_part1 = int(distances[start][0])
    result_part2 = int(min(distances[np.where(elevation == np.min(elevation))]))
    # Could, in theory, only check for a's next to b's. But with this solution: is not worth it!

    print(f'Results for {"example" if example_run else "my"} input:')
    print(f' Result of part 1: {result_part1} steps from point S to point E')
    print(f' Result of part 2: {result_part2} steps minimal from elevation a to point E.')

    print(f'\nDescriptives: \n {n_iter} iterations \n'
          f' {len(distances[np.where(elevation == np.min(elevation))])} points at elevation a \n'
          f' {I} by {J} is the size of the grid\n\n')


run_all(example_run=True)
run_all(example_run=False)
