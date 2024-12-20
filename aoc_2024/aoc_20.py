from collections import defaultdict
from typing import Union
from util.util import ProcessInput, run_day, get_neighbors_cplx


def run_all(example_run: Union[int, bool]):

    data = ProcessInput(example_run=example_run, day=20, year=2024).data

    # Process data into free spaces, start and end; also into 'cheats': all 1-step cheat spaces for use in part 1
    free, cheats, start, end = set(), set(), 0, 0
    for i, row in enumerate(data):
        for j, el in enumerate(row):
            if el != '#':
                free.add(i + j*1j)
                if el == 'S':
                    start = i + j*1j
                if el == 'E':
                    end = i + j*1j
    for i, row in enumerate(data):
        for j, el in enumerate(row):
            if el == '#' and sum(x in free for x in get_neighbors_cplx(i + j*1j)) >= 2:
                cheats.add(i + j * 1j)

    # Find original full path
    queue = [(start, 0, [start])]
    hist = {(start, False)}
    path = [start]
    while len(queue) > 0:
        loc, step, path = queue.pop(0)
        if loc == end:
            break
        for nghbr in get_neighbors_cplx(loc):
            if nghbr in free and nghbr not in hist:
                queue.append((nghbr, step + 1, path + [nghbr]))
                hist.add(nghbr)

    # Part 1 algorithm: normal BFS with states: (loc, steps, has_cheat). After cheat, directly to end using path
    queue = [(start, 0, False)]
    hist = {(start, False)}
    res = []
    while len(queue) > 0:
        loc, step, has_cheat = queue.pop(0)

        if loc == end:
            res.append((step, has_cheat))
            continue

        for nghbr in get_neighbors_cplx(loc):
            if nghbr in free and (nghbr, has_cheat) not in hist:
                queue.append((nghbr, step + 1, has_cheat))
                hist.add((nghbr, has_cheat))
            elif nghbr in cheats and not has_cheat:
                nexts = get_neighbors_cplx(nghbr)
                inds = [path.index(nxt) for nxt in nexts if nxt in path]
                res.append((step + 1 + len(path) - max(inds), nghbr))
                hist.add((nghbr, nghbr))

    non_cheat_res = [x for x in res if not x[1]][0][0]
    time_saves = ([non_cheat_res - x[0] for x in res if x[0] < non_cheat_res])

    result_part1 = len([x for x in time_saves if x >= (10 if example_run else 100)])

    # Part 2: if cheats are on, you can skip from one point on the path to a future one in pure Manhattan distance style
    # We could have used this for part 1 as well but I will leave part 1 code. (Part 1 uses this logic only for after
    # the cheat but it also works for before the cheat, of course).
    cheat_count = defaultdict(int)
    for i, cheat_start in enumerate(path):
        for diff_i, cheat_end in enumerate(path[i + 1:]):
            diff_loc = cheat_end - cheat_start
            cheat_steps = int(abs(diff_loc.imag) + abs(diff_loc.real))
            if cheat_steps > 20:
                continue
            time_saved = diff_i - cheat_steps + 1
            if time_saved > 0:
                cheat_count[time_saved] += 1

    result_part2 = sum([v for k,v in cheat_count.items() if k >= (50 if example_run else 100)])

    extra_out = {'Dimensions of input': (len(data), len(data[0])),
                 'Length of non-cheating path': len(path),
                 'Number of potential 1-step cheats': len(cheats)}

    return result_part1, result_part2, extra_out


if __name__ == "__main__":
    run_day(run_all, [1])
