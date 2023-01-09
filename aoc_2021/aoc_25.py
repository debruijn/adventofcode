
import numpy as np

with open('aoc_25_data') as f:
    data_raw = f.readlines()

data = [row.replace('\n', '').split(" ") for row in data_raw]
data = np.array([[1 if x == ">" else 2 if x == "v" else 0 for x in row[0]] for row in data])

curr = data.copy()
old = np.zeros_like(curr)  # Just some random initialization
counter = 0
dims = data.shape
while not np.all(curr == old):
    old = curr.copy()

    # Move 1s right
    cand = curr.copy()
    index_1s = np.where(curr == 1)
    pot_locs = (index_1s[0], np.mod(index_1s[1] + 1, dims[1]))
    pot_locs_free = np.where(curr[pot_locs] == 0)
    cand[index_1s[0][pot_locs_free], index_1s[1][pot_locs_free]] = 0
    cand[pot_locs[0][pot_locs_free], pot_locs[1][pot_locs_free]] = 1
    curr = cand

    # Move 2s down
    cand = curr.copy()
    index_2s = np.where(curr == 2)
    pot_locs = (np.mod(index_2s[0] + 1, dims[0]), index_2s[1])
    pot_locs_free = np.where(curr[pot_locs] == 0)
    cand[index_2s[0][pot_locs_free], index_2s[1][pot_locs_free]] = 0
    cand[pot_locs[0][pot_locs_free], pot_locs[1][pot_locs_free]] = 2
    curr = cand

    counter += 1
    print(curr)
    print(counter)
