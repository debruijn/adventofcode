from copy import deepcopy
import numpy as np

with open('aoc_15_data') as f:
    data = f.readlines()

data = np.array([[int(x) for x in row if x != '\n'] for row in data])


def find_path(data, tile_size=1, max_val=9):
    risk = []  # risk per tile
    path_risk = []  # cumulative risk to get to that tile
    for htile in range(tile_size):
        for row in data:
            risk.append([])
            path_risk.append([])
            for vtile in range(tile_size):
                for val in row:
                    path_risk[-1].append(np.inf)
                    risk[-1].append(int(val) + htile + vtile)  # htile + vtile = nr of times it is tiled from top-left
                    while risk[-1][-1] > max_val:  # Keep decreasing until below max_val
                        risk[-1][-1] -= max_val

    risk_last = []
    path_risk[0][0] = 0  # Start path has risk 0

    has_changed = True  # Boolean to track whether risk have changed in last iter
    while has_changed:
        for i in range(len(path_risk)):
            for j in range(len(path_risk[-1])):
                if i == 0 and j == 0:
                    continue

                risk_up = path_risk[i - 1][j] if i > 0 else np.inf
                risk_left = path_risk[i][j - 1] if j > 0 else np.inf
                risk_down = path_risk[i + 1][j] if i < len(path_risk) - 1 else np.inf
                risk_right = path_risk[i][j + 1] if j < len(path_risk[-1]) - 1 else np.inf

                minimum = np.min([risk_up, risk_left, risk_down, risk_right])
                path_risk[i][j] = min(minimum + risk[i][j], path_risk[i][j])

        if path_risk == risk_last:
            has_changed = False
        else:
            risk_last = deepcopy(path_risk)

    return path_risk


print(f"Solution part 1: {find_path(data, tile_size=1, max_val=9)[-1][-1]}")
print(f"Solution part 2: {find_path(data, tile_size=5, max_val=9)[-1][-1]}")
