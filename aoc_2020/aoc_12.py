from typing import Union
from util.util import ProcessInput, run_day

debug = False


def run_all(example_run: Union[int, bool]):

    data = ProcessInput(example_run=example_run, day=12, year=2020).data

    loc = 0j
    facing = 1 + 0j
    mapping_move = {'E': (1+0j), 'W': (-1 + 0j), 'N': 1j, 'S': -1j}
    mapping_rot = {'L': 1j, 'R': -1j}

    for row in data:
        if row[0] in mapping_move.keys():
            loc += mapping_move[row[0]] * int(row[1:])
        elif row[0] == 'F':
            loc += facing * int(row[1:])
        else:
            facing *= mapping_rot[row[0]]**(int(row[1:])/90)
    result_part1 = int(abs(loc.imag) + abs(loc.real))

    loc_p2 = 0j
    waypoint = 10 + 1j

    for row in data:
        if row[0] in mapping_move.keys():
            waypoint += mapping_move[row[0]] * int(row[1:])
        elif row[0] == 'F':
            loc_p2 += waypoint * int(row[1:])
        else:
            waypoint *= mapping_rot[row[0]]**(int(row[1:])/90)
    result_part2 = int(abs(loc_p2.imag) + abs(loc_p2.real))

    extra_out = {'Number of instructions': len(data),
                 'Final location part 1': f"({int(loc.real)}, {int(loc.imag)})",
                 'Final facing': f"({int(facing.real)}, {int(facing.imag)})",
                 'Final location part 2': f"({int(loc_p2.real)}, {int(loc_p2.imag)})",
                 'Final waypoint': f"({int(waypoint.real)}, {int(waypoint.imag)})"}

    return result_part1, result_part2, extra_out


if __name__ == "__main__":
    run_day(run_all, [1])
