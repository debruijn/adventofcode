from typing import Union
from util.util import ProcessInput, run_day

debug = False


def run_all(example_run: Union[int, bool]):

    data = ProcessInput(example_run=example_run, day=23, year=2023).data

    # Process input to which locations are open or one of the ledges
    free = []
    dir_free = [[] for _ in range(4)]
    step_to_dir = {-1: 0, 1: 2, -1j: 3, 1j: 1}

    for i, row in enumerate(data):
        for j, el in enumerate(row):
            if el == '.':
                free.append(i + j*1j)
            elif el == '^':
                dir_free[0].append(i+j*1j)
            elif el == '>':
                dir_free[1].append(i+j*1j)
            elif el == 'v':
                dir_free[2].append(i+j*1j)
            elif el == '<':
                dir_free[3].append(i+j*1j)
    full_free = free.copy()
    [full_free.extend(list_dir) for list_dir in dir_free]

    start = 1j
    target = len(data) - 1 + (len(data[0]) - 2) * 1j

    # Part 1: simple BFS
    # Based on part 2 solution, could speed up to only take decision points into account, and see where you can go to from each of them.
    visited = [start]
    hist = set()
    queue = [(start, hist)]
    max_dist = 0

    stop = False
    while not stop:
        curr_loc, curr_hist = queue.pop(0)

        for step in (-1, 1, -1j, 1j):
            new_loc = curr_loc + step
            if new_loc == target:
                if len(curr_hist) + 1 > max_dist:
                    max_dist = len(curr_hist) + 1
                    if debug:
                        print(f"Found target with length {max_dist} ")
            elif new_loc not in curr_hist:
                if new_loc in free or new_loc in dir_free[step_to_dir[step]]:
                    queue.append((new_loc, curr_hist.union({curr_loc})))
                    visited.append(new_loc)

        if len(queue) == 0:
            stop = True

    result_part1 = max_dist


    # Find decision points: points with three or four sides that are not #
    decision_points = [start, target]
    for pt in full_free:
        i, j = int(pt.real), int(pt.imag)
        if 1<=i<len(data)-1 and 1<=j<len(data[0])-1:
            count_hash = (data[i-1][j]=='#') + (data[i+1][j]=='#') + (data[i][j+1]=='#') + (data[i][j-1]=='#')
            if count_hash < 2:
                decision_points.append(i+j*1j)

    # Find next decision points for each decision point
    next_decision_points = {}
    try_dirs =  (1, -1, 1j, -1j)
    for pt in decision_points:
        this_next = {}
        for try_dir in try_dirs:
            curr_pt = pt + try_dir
            curr_dist = 1
            hist = [pt, curr_pt]
            if curr_pt in full_free:
                stop = False
                while not stop:
                    new_pts = [curr_pt + try_dir for try_dir in try_dirs]
                    new_pts = [x for x in new_pts if x in full_free and x not in hist]
                    if len(new_pts) == 1:
                        curr_pt = new_pts[0]
                        curr_dist += 1
                        hist.append(curr_pt)
                    elif len(new_pts) > 1:
                        if curr_pt in this_next:
                            raise ValueError('yo')
                        this_next[curr_pt] = curr_dist
                        stop = True
                    else:
                        if curr_pt in (start, target):
                            this_next[curr_pt] = curr_dist
                        stop = True
        next_decision_points[pt] = this_next

    # Weighted DFS. Keeping track of point still available instead of history. If a decision point only has 1 point in
    # the availables (and it is not the target point) then you can't visit it anymore -> take it out.
    max_dist = 0
    avail = [x for x in decision_points if x != start]
    avail = tuple(sorted(avail, key=lambda x: x.real * 1000 + x.imag))
    queue = [(start, avail, 0)]
    hist = {}

    stop = False
    while not stop:
        curr_loc, curr_avail, curr_length = queue.pop()
        do_this = True
        if (curr_loc, curr_avail) in hist:
            if curr_length > hist[(curr_loc, curr_avail)]:
                hist[(curr_loc, curr_avail)] = curr_length
            else:
                do_this = False
        else:
            hist[(curr_loc, curr_avail)] = curr_length
        if do_this:
            for next_loc, next_length in next_decision_points[curr_loc].items():
                if next_loc == target:
                    if curr_length + next_length > max_dist:
                        max_dist = curr_length + next_length
                        if debug:
                            print(f"Found target with length {max_dist} ")
                elif next_loc in curr_avail:
                    next_avail = list(curr_avail)
                    next_avail.remove(next_loc)
                    nr_avail_per_pt = {x: len([y for y in next_decision_points[x] if y in curr_avail]) for x in next_avail if x != target}
                    for k, v in nr_avail_per_pt.items():
                        if v < 2:
                            next_avail.remove(k)
                    queue.append((next_loc, tuple(next_avail), curr_length + next_length))

        if len(queue) == 0:
            stop = True

    result_part2 = max_dist

    extra_out = {'Dimension of input': (len(data), len(data[0])),
                 'Number of decision points': len(decision_points)}

    return result_part1, result_part2, extra_out


if __name__ == "__main__":
    run_day(run_all, [1])
