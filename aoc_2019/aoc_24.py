from typing import Union
from util.util import ProcessInput, run_day

debug = False


def get_biodiversity(bugs, dim):
    alt_bugs = [int(x.imag) + dim * int(x.real) for x in bugs]
    return sum([2 ** x for x in alt_bugs])


def run_all(example_run: Union[int, bool]):

    data = ProcessInput(example_run=example_run, day=24, year=2019).data

    # Process data to lists (normally smart idea, I think in this case it doesn't matter but okay)
    bugs, free, full = [], [], []
    for i, row in enumerate(data):
        for j, el in enumerate(row):
            if el == '#':
                bugs.append(i + j*1j)
            else:
                free.append(i + j*1j)
            if not (i==2 and j==2):
                full.append(i + j*1j)
    bugs_orig, free_orig = bugs.copy(), free.copy()  # For part 2

    # Loop, keeping tracking of history of biodiversity (which is enough to differentiate between states)
    this_biodiversity = get_biodiversity(bugs, len(data[0]))
    hist = [this_biodiversity]
    stop = False
    r = 0
    while not stop:
        new_bugs, new_free = [], []
        for bug in bugs:
            if sum([bug+x in bugs for x in (1, -1, 1j, -1j)]) == 1:
                new_bugs.append(bug)
            else:
                new_free.append(bug)
        for el in free:
            if sum([el+x in bugs for x in (1, -1, 1j, -1j)]) in (1, 2):
                new_bugs.append(el)
            else:
                new_free.append(el)
        r+=1
        this_biodiversity = get_biodiversity(new_bugs, len(data[0]))
        if debug:
            print(r, len(new_bugs), this_biodiversity)
        if this_biodiversity in hist:
            stop = True
        else:
            bugs = new_bugs
            free = new_free
            hist.append(this_biodiversity)

    result_part1 = this_biodiversity

    R = 200 if not example_run else 10
    bugs, free = {0: bugs_orig}, {0: free_orig}
    dims_curr = [0, 0]
    for r in range(R):

        # New dimensions to evaluate: 1 wider than old ones. Also add them to current bugs/free
        new_dims = [dims_curr[0]-1, dims_curr[1]+1]
        new_bugs = {dim: [] for dim in range(new_dims[0], new_dims[1]+1)}
        new_free = {dim: [] for dim in range(new_dims[0], new_dims[1]+1)}
        bugs[new_dims[0]] = []
        free[new_dims[0]] = full.copy()
        bugs[new_dims[1]] = []
        free[new_dims[1]] = full.copy()

        # Below lines could be cleaned up since there is duplication. E.g. "sum in layer, sum above, sum below" with ifs
        # Loop over existing layers for bugs
        for layer in range(dims_curr[0], dims_curr[1] + 1):
            for bug in bugs[layer]:
                sum_neighbours = 0
                for iter_diff in [1, -1, 1j, -1j]:
                    iter_bug = iter_diff + bug
                    if iter_bug.real == 2 and iter_bug.imag == 2:
                        if iter_diff == 1:
                            sum_neighbours += sum([x in bugs[layer+1] for x in (0j, 1j, 2j, 3j, 4j)])
                        if iter_diff == -1:
                            sum_neighbours += sum([x in bugs[layer+1] for x in (4+0j, 4+1j, 4+2j, 4+3j, 4+4j)])
                        if iter_diff == 1j:
                            sum_neighbours += sum([x in bugs[layer+1] for x in (0, 1, 2, 3, 4)])
                        if iter_diff == -1j:
                            sum_neighbours += sum([x in bugs[layer+1] for x in (0+4j, 1+4j, 2+4j, 3+4j, 4+4j)])
                    elif iter_bug.real == -1:
                        sum_neighbours += 1+2j in bugs[layer-1]
                    elif iter_bug.imag == -1:
                        sum_neighbours += 2+1j in bugs[layer-1]
                    elif iter_bug.real == 5:
                        sum_neighbours += 3+2j in bugs[layer-1]
                    elif iter_bug.imag == 5:
                        sum_neighbours += 2+3j in bugs[layer-1]
                    else:
                        sum_neighbours += iter_bug in bugs[layer]
                if sum_neighbours == 1:
                    new_bugs[layer].append(bug)
                else:
                    new_free[layer].append(bug)

        # Loop over new layers for free
        for layer in range(new_dims[0], new_dims[1]+1):
            for el in free[layer]:
                sum_neighbours = 0
                for iter_diff in [1, -1, 1j, -1j]:
                    iter_bug = iter_diff + el
                    if iter_bug.real == 2 and iter_bug.imag == 2:
                        if layer < new_dims[1]:
                            if iter_diff == 1:
                                sum_neighbours += sum([x in bugs[layer + 1] for x in (0j, 1j, 2j, 3j, 4j)])
                            if iter_diff == -1:
                                sum_neighbours += sum(
                                    [x in bugs[layer + 1] for x in (4 + 0j, 4 + 1j, 4 + 2j, 4 + 3j, 4 + 4j)])
                            if iter_diff == 1j:
                                sum_neighbours += sum([x in bugs[layer + 1] for x in (0, 1, 2, 3, 4)])
                            if iter_diff == -1j:
                                sum_neighbours += sum(
                                    [x in bugs[layer + 1] for x in (0 + 4j, 1 + 4j, 2 + 4j, 3 + 4j, 4 + 4j)])
                    elif iter_bug.real == -1:
                        if layer > new_dims[0]:
                            sum_neighbours += 1 + 2j in bugs[layer - 1]
                    elif iter_bug.imag == -1:
                        if layer > new_dims[0]:
                            sum_neighbours += 2 + 1j in bugs[layer - 1]
                    elif iter_bug.real == 5:
                        if layer > new_dims[0]:
                            sum_neighbours += 3 + 2j in bugs[layer - 1]
                    elif iter_bug.imag == 5:
                        if layer > new_dims[0]:
                            sum_neighbours += 2 + 3j in bugs[layer - 1]
                    else:
                        sum_neighbours += iter_bug in bugs[layer]
                if sum_neighbours in (1, 2):
                    new_bugs[layer].append(el)
                else:
                    new_free[layer].append(el)

        if debug:
            print(r, [len(x) for x in new_bugs.values()])

        bugs = new_bugs
        free = new_free

        # Current dims are set to new dims but if outer layers contain no bugs they are ignored (to keep size down)
        dims_curr = new_dims
        if len(bugs[dims_curr[0]]) == 0:
            dims_curr[0] += 1
        if len(bugs[dims_curr[1]]) == 0:
            dims_curr[1] -= 1

    result_part2 = sum([len(x) for x in bugs.values()])

    extra_out = {'Number of rows in input': len(data)}  # TODO: create dict of additional things to have them printed

    return result_part1, result_part2, extra_out


if __name__ == "__main__":
    run_day(run_all, [1])
