from typing import Union
from util.util import ProcessInput, run_day

debug = False


def run_all(example_run: Union[int, bool]):

    data = ProcessInput(example_run=example_run, day=6, year=2019).data

    mapping = {}
    for row in data:
        x, y = row.split(')')
        mapping.update({y: (x, None, None)})

    count_orbits = 0
    while any(None in x for x in mapping.values()):

        for key, val in mapping.items():
            if val[1] is None:
                if val[0] == 'COM':
                    mapping[key] = (val[0], 1, {'COM'})
                    count_orbits += 1
                elif mapping[val[0]][1] is not None:
                    mapping[key] = (val[0], 1 + mapping[val[0]][1], mapping[val[0]][2].union({val[0]}))
                    count_orbits += mapping[key][1]

    result_part1 = count_orbits
    if 'SAN' in mapping:
        result_part2 = len(mapping['SAN'][2].union(mapping['YOU'][2]) - mapping['SAN'][2].intersection(mapping['YOU'][2]))
    else:
        result_part2 = 'N/A'

    extra_out = {'Number of direct orbits in input': len(data),
                 'Maximum orbit depth': max([len(val[2]) for val in mapping.values()])}
    if 'SAN' in mapping:
        extra_out.update({'Number of shared orbits between SAN and YOU':
                              len(mapping['SAN'][2].intersection(mapping['YOU'][2]))})

    return result_part1, result_part2, extra_out


if __name__ == "__main__":
    run_day(run_all, [1])
