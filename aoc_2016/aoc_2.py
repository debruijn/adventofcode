from typing import Union
from util.util import ProcessInput, run_day


def run_all(example_run: Union[int, bool]):

    data = ProcessInput(example_run=example_run, day=2, year=2016).data

    # Part 1: take next steps by subtracting/adding 1 or 3, if that results in a valid position
    code = ""
    loc = 5
    for row in data:
        for char in row:
            if char == "U":
                loc = loc - 3 if loc - 3 > 0 else loc
            elif char == "D":
                loc = loc + 3 if loc + 3 < 10 else loc
            elif char == "L":
                loc = loc - 1 if loc - 1 not in (0, 3, 6) else loc
            else:  # char == "R":
                loc = loc + 1 if loc + 1 not in (4, 7, 10) else loc
        code += str(loc)

    result_part1 = code

    # Part 2: due to more complicated setup, apply mapping of char to char manually.
    code = ""
    loc = "5"
    up_mapping = {'1': '1', '2': '2', '3': '1', '4': '4', '5': '5', '6': '2', '7': '3', '8': '4', '9': '9', 'A': '6',
                  'B': '7', 'C': '8', 'D': 'B'}
    down_mapping = {'1': '3', '2': '6', '3': '7', '4': '8', '5': '5', '6': 'A', '7': 'B', '8': 'C', '9': '9', 'A': 'A',
                  'B': 'D', 'C': 'C', 'D': 'D'}
    left_mapping = {'1': '1', '2': '2', '3': '2', '4': '3', '5': '5', '6': '5', '7': '6', '8': '7', '9': '8', 'A': 'A',
                  'B': 'A', 'C': 'B', 'D': 'D'}
    right_mapping = {'1': '1', '2': '3', '3': '4', '4': '4', '5': '6', '6': '7', '7': '8', '8': '9', '9': '9', 'A': 'B',
                    'B': 'C', 'C': 'C', 'D': 'D'}
    mapping = {'U': up_mapping, 'D': down_mapping, 'L': left_mapping, 'R': right_mapping}

    for row in data:
        for char in row:
            loc = mapping[char][loc]
        code += loc

    result_part2 = code

    extra_out = {'Number of numbers to recover': len(data),
                'Highest number of steps per number': max(len(x) for x in data)}

    return result_part1, result_part2, extra_out


if __name__ == "__main__":
    run_day(run_all, [1])
