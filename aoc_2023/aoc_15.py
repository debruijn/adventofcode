from typing import Union
from util.util import ProcessInput, run_day

debug = False

def get_hash(string):
    curr_num = 0
    for char in string:
        curr_num = ((curr_num + ord(char)) * 17) % 256
    return curr_num


def run_all(example_run: Union[int, bool]):

    data = ProcessInput(example_run=example_run, day=15, year=2023).data
    data = "".join(data).split(',')

    result_part1 = sum([get_hash(string) for string in data])

    boxes = [[] for _ in range(256)]
    box_vals = [[] for _ in range(256)]
    for string in data:
        if '=' in string:
            label, num = string.split('=')
            box_nr = get_hash(label)
            if label in boxes[box_nr]:
                box_vals[box_nr][boxes[box_nr].index(label)] = int(num)
            else:
                boxes[box_nr].append(label)
                box_vals[box_nr].append(int(num))
        else:  # -
            label = string[:-1]
            box_nr = get_hash(label)
            if label in boxes[box_nr]:
                box_vals[box_nr].pop(boxes[box_nr].index(label))
                boxes[box_nr].remove(label)

    sum_lens_power = 0
    for i, box in enumerate(box_vals):
        for j, val in enumerate(box):
            sum_lens_power += (1+i) * (1+j) * val

    result_part2 = sum_lens_power

    extra_out = {'Number of instructions in input': len(data),
                 'Number of filled boxes': sum([len(x)>0 for x in boxes]),
                 'Number of final entries': sum([len(x) for x in boxes])}

    return result_part1, result_part2, extra_out


if __name__ == "__main__":
    run_day(run_all, [1])
