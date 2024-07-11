from collections import defaultdict
from typing import Union
from util.util import ProcessInput, run_day

debug = False


def split_next_regex(next_regex):
    splits = next_regex.split('|')
    i = 0
    while i < len(splits):
        if splits[i].count('(') > splits[i].count(')'):
            splits[i] = splits[i] + '|' + splits.pop(i+1)
        else:
            i += 1
    return splits


def split_regex(regex):

    first = regex[:regex.find('(')]
    regex = regex[regex.find('(') + 1:]
    count = 1
    ind = 0
    while count > 0:
        if regex[ind] == '(':
            count += 1
        if regex[ind] == ')':
            count -= 1
        ind += 1
    second = regex[:ind-1]
    third = regex[ind:]

    return first, second, third


move_mapping = {'E': 1j, 'W': -1j, 'N': -1, 'S': 1}


def run_all(example_run: Union[int, bool]):

    data = ProcessInput(example_run=example_run, day=20, year=2018).data

    # Process regex to room structure:
    # - Split regex into "sure thing" at start, the next "option" and what happens in each case after that option.
    # - Use "sure thing" to find new locations and doors
    # - Use each option + afterpart as new regex to evaluate, starting from location "sure thing" ended at
    locs = [0 + 0*1j]
    doors = defaultdict(list)
    queue = [(locs[0], data[0].replace('^', '').replace('$', ''))]
    hist = []
    while len(queue) > 0:
        this_iter = queue.pop()
        if this_iter not in hist:
            this_loc, this_regex = this_iter
            hist.append(this_iter)

            # Detect if current regex has multiple options; if so, split it accordingly (only get the top-level split).
            if '(' in this_regex:
                this_regex, next_regex, final_part = split_regex(this_regex)
                next_regex = split_next_regex(next_regex)  # Get list with all options, without outer (, | and )
            else:
                next_regex, final_part = [], ""

            # Evaluate this first sure component of the path to find new locations and doors.
            for move in this_regex:
                last_loc = this_loc
                this_loc += move_mapping[move]
                if this_loc not in locs:
                    locs.append(this_loc)
                if this_loc not in doors[last_loc]:
                    doors[last_loc].append(this_loc)
                    doors[this_loc].append(last_loc)

            # Add all combinations of the next component and the final part to the queue to process next.
            for next_reg in next_regex:
                queue.append((this_loc, next_reg + final_part))

    # From starting point, find all points you can find for a given distance that you iteratively increase. (Dijkstra)
    todo = locs.copy()
    queue = [(0, 0 + 0*1j)]
    hist_dict = {}
    while len(queue) > 0:
        this_dist, this_loc = queue.pop(0)

        if this_loc not in hist_dict:
            hist_dict[this_loc] = this_dist
        else:
            if this_dist < hist_dict[this_loc]:
                hist_dict[this_loc] = this_dist

        for point in doors[this_loc]:
            if point in todo:
                queue.append([this_dist+1, point])
                todo.remove(point)

    result_part1 = max(hist_dict.values())
    result_part2 = sum([1 for x in hist_dict.values() if x >= 1000])

    extra_out = {'Number of chars in input': len(data[0]),
                 'Number of rooms': len(locs),
                 'Number of connections': int(0.5 * sum(len(x) for x in doors.values()))}

    return result_part1, result_part2, extra_out


if __name__ == "__main__":
    run_day(run_all, [1, 2, 3, 4, 5])
