from typing import Union
from util.util import ProcessInput, run_day


def get_tokens(data, part_2=False):

    tokens = 0
    for block in data:
        xA = int(block[0].replace(',', '').split(' ')[2].split('+')[1])
        yA = int(block[0].replace(',', '').split(' ')[3].split('+')[1])
        xB = int(block[1].replace(',', '').split(' ')[2].split('+')[1])
        yB = int(block[1].replace(',', '').split(' ')[3].split('+')[1])
        xT = int(block[2].replace(',', '').split(' ')[1].split('=')[1]) + (10000000000000 if part_2 else 0)
        yT = int(block[2].replace(',', '').split(' ')[2].split('=')[1]) + (10000000000000 if part_2 else 0)
        nB = (yT - yA * xT/xA ) / (yB - xB * yA/xA)
        nA = (xT - xB*nB) / xA

        if part_2:
            if 0 <= nA and 0 <= nB and round(nA) == round(nA, 3) and round(nB) == round(nB, 3):
                tokens += 3 * round(nA) + round(nB)
        else:
            if 0 <= nA <= 100 and 0 <= nB <= 100 and round(nA) == round(nA, 3) and round(nB) == round(nB, 3):
                tokens += 3 * round(nA) + round(nB)

    return tokens


def run_all(example_run: Union[int, bool]):

    data = ProcessInput(example_run=example_run, day=13, year=2024).as_list_of_strings_per_block().data

    result_part1 = get_tokens(data)
    result_part2 = get_tokens(data, part_2=True)

    extra_out = {'Number of blocks in input': len(data)}

    return result_part1, result_part2, extra_out


if __name__ == "__main__":
    run_day(run_all, [1])
