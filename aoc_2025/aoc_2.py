from typing import Union
from util.util import ProcessInput, run_day


def run_part(data, part):

    max_n = 10 if part == 2 else 2
    invalids = set()
    for row in data:
        start, end = row.split('-')
        start, end = int(start), int(end)
        for num in range(start, end+1):
            str_num = str(num)

            for n in range(2, max_n+1):
                if len(str_num) % n != 0:
                    continue
                cut_str_len = int(len(str_num)/ n)
                ref_str = str_num[:cut_str_len]
                this_str_num = str_num[cut_str_len:]
                while len(this_str_num)>0:
                    if this_str_num[:cut_str_len] == ref_str:
                        this_str_num = this_str_num[cut_str_len:]
                    else:
                        break
                else:
                    invalids.update({num})

    return invalids


def run_all(example_run: Union[int, bool]):

    data = ProcessInput(example_run=example_run, day=2, year=2025).data
    data = data[0].split(',')

    invalids_pt1 = run_part(data, part=1)
    invalids_pt2 = run_part(data, part=2)

    result_part1 = sum(invalids_pt1)
    result_part2 = sum(invalids_pt2)

    extra_out = {'Number of ranges in input': len(data),
                 'Number of invalids in part 1': len(invalids_pt1),
                 'Number of invalids in part 2': len(invalids_pt2)}

    return result_part1, result_part2, extra_out


if __name__ == "__main__":
    run_day(run_all, [1])
