from collections import defaultdict
from typing import Union
from util.util import ProcessInput, run_day
import math

debug = False


def get_points(data, dims_short):

    free = []
    tps_raw = []
    for i, row in enumerate(data):
        if 2 <= i < 2 + dims_short[0]:
            for j, el in enumerate(row):
                if 2 <= j < 2 + dims_short[1]:
                    if el == '.':
                        free.append(i + j*1j)
                        if ord('A') <= ord(data[i][j-1]) <= ord('Z'):
                            tps_raw.append((data[i][j-2:j], i + (j-1)*1j))  # i + (j-2)*1j
                        if ord('A') <= ord(data[i][j+1]) <= ord('Z'):
                            tps_raw.append((data[i][j+1:j+3], i + (j+1)*1j))  #  i + (j+2)*1j
                        if ord('A') <= ord(data[i-1][j]) <= ord('Z'):
                            tps_raw.append((data[i-2][j]+data[i-1][j], i-1 + j*1j))  # i-2 + j*1j
                        if ord('A') <= ord(data[i+1][j]) <= ord('Z'):
                            tps_raw.append((data[i+1][j]+data[i+2][j], i+1 + j*1j))  #  i+2 + j*1j

    start = 0 + 0j
    end = 0 + 0j
    tps = {}  # convert tps_raw to tps
    for tp in tps_raw:
        if tp[0] == 'AA':
            start = [tp[1] + 1, tp[1] - 1]  # always down
        elif tp[0] == 'ZZ':
            end = tp[1]
        else:
            if tp[0] in tps.keys():
                tps[tp[1]] = tps[tp[0]]
                tps[tps[tp[0]]] = tp[1]
                del tps[tp[0]]
            else:
                tps[tp[0]] = tp[1]

    return start, end, free, tps

def run_all(example_run: Union[int, bool]):

    data = ProcessInput(example_run=example_run, day=20, year=2019).data

    dims_short = (len(data)-4, len(data[2])-4)

    start, end, free, tp = get_points(data, dims_short)

    queue = start
    visited = {s: 0 + 0j for s in start}  # Fun trick: use complex numbers to track number of transportations using imaginary part
    res1 = None
    next_dir = [1, -1, 1j, -1j]
    while len(queue)>0:
        this_loc = queue.pop(0)
        # We technically need to have a priority queue instead of popping the oldest, due to TPs not increasing by 1;
        # To avoid that, we don't stop immediately at a result, but simply don't continue with elements above first result
        # In this case it is the same, but mathematically it's possible that the first solution is not the lowest
        # Alternatively, we could've forced another step immediately after a TP (of which there is always only one),
        # then non-priority queue still works even theoretically.
        if res1 is None or visited[this_loc].real < res1.real:
            for nxt in next_dir:
                next_loc = this_loc + nxt
                if next_loc == end:
                    res1 = visited[this_loc]
                if next_loc in free and next_loc not in visited:
                    visited[next_loc] = visited[this_loc] + 1
                    queue.append(next_loc)
                elif next_loc in tp and next_loc not in visited:
                    this_tp = tp[next_loc]
                    visited[next_loc] = visited[this_loc]
                    visited[this_tp] = visited[this_loc] + 1j
                    queue.append(this_tp)

    result_part1 = int(res1.real)

    def is_outer(loc):
        return loc.real <= 1 or loc.imag <= 1 or loc.real >= dims_short[0] or loc.imag >= dims_short[1]

    start, end, free, tp = get_points(data, dims_short)
    outer_tp = [x for x in tp.keys() if is_outer(x)]
    solve_part2_with_heap = True

    if not solve_part2_with_heap:
        queue = [(s, 0) for s in start]
        visited = {(s, 0): 0 for s in start}  # Fun trick: use complex numbers to track number of transportations using imaginary part

        res2 = math.inf
        next_dir = [1, -1, 1j, -1j]
        max_depth = 0
        stop = False
        while len(queue)>0 and not stop:
            this_loc, this_depth = queue.pop(0)
            max_depth = this_depth if this_depth > max_depth else max_depth
            # We technically need to have a priority queue instead of popping the oldest, due to TPs not increasing by 1;
            # To avoid that, we don't stop immediately at a result, but simply don't continue with elements above first result
            # In this case it is the same, but mathematically it's possible that the first solution is not the lowest
            # Alternatively, we could've forced another step immediately after a TP (of which there is always only one),
            # then non-priority queue still works even theoretically.
            if visited[(this_loc, this_depth)] < res2:
                for nxt in next_dir:
                    next_loc = this_loc + nxt
                    if next_loc == end and this_depth == 0:
                        res2 = visited[(this_loc, this_depth)]
                        stop = True
                    if next_loc in free and ((next_loc, this_depth) not in visited):
                        visited[(next_loc, this_depth)] = visited[(this_loc, this_depth)] + 1
                        queue.append((next_loc, this_depth))
                    elif next_loc in tp and ((next_loc, this_depth) not in visited):
                        this_tp = tp[next_loc]
                        visited[(next_loc, this_depth)] = visited[(this_loc, this_depth)]
                        next_depth = this_depth + (1 if this_tp in outer_tp else -1)
                        if 50 > next_depth >= 0:
                            visited[(this_tp, next_depth)] = visited[(this_loc, this_depth)]
                            queue.append((this_tp, next_depth))
    else:
        queue = defaultdict(list)
        queue[0] = [s for s in start]
        this_depth = 0
        visited = {(s, 0): 0 for s in start}  # Fun trick: use complex numbers to track number of transportations using imaginary part
        res2 = math.inf
        next_dir = [1, -1, 1j, -1j]
        max_depth = 0
        stop = False
        while len(queue)>0 and not stop:
            this_loc = queue[this_depth].pop(0)
            max_depth = this_depth if this_depth > max_depth else max_depth
            switch_depth_down = False
            # We technically need to have a priority queue instead of popping the oldest, due to TPs not increasing by 1;
            # To avoid that, we don't stop immediately at a result, but simply don't continue with elements above first result
            # In this case it is the same, but mathematically it's possible that the first solution is not the lowest
            # Alternatively, we could've forced another step immediately after a TP (of which there is always only one),
            # then non-priority queue still works even theoretically.
            if visited[(this_loc, this_depth)] < res2:
                for nxt in next_dir:
                    next_loc = this_loc + nxt
                    if next_loc == end and this_depth == 0:
                        res2 = visited[(this_loc, this_depth)]
                        # stop = True
                    if next_loc in free and ((next_loc, this_depth) not in visited):
                        visited[(next_loc, this_depth)] = visited[(this_loc, this_depth)] + 1
                        queue[this_depth].append(next_loc)
                    elif next_loc in tp and ((next_loc, this_depth) not in visited):
                        this_tp = tp[next_loc]
                        visited[(next_loc, this_depth)] = visited[(this_loc, this_depth)]
                        next_depth = this_depth + (1 if this_tp in outer_tp else -1)
                        if 200 > next_depth >= 0:
                            visited[(this_tp, next_depth)] = visited[(this_loc, this_depth)]
                            queue[next_depth].append(this_tp)
                            if next_depth < this_depth:
                                switch_depth_down = True
            if len(queue[this_depth]) == 0:
                del queue[this_depth]
                this_depth = min([x for x in queue.keys()], default=math.inf)
            if switch_depth_down:
                this_depth = min([x for x in queue.keys()])

    result_part2 = res2

    extra_out = {'Size of the maze': dims_short,
                 'Number of free spots': len(free),
                 'Number of teleport pairs': int(len(tp)/2),
                 'Number of teleports used in solution part 1': int(res1.imag),
                 'Max depth evaluated in part 2': max_depth}

    return result_part1, result_part2, extra_out


if __name__ == "__main__":
    run_day(run_all, [1, 2, 3])
