from typing import Union
from util.util import ProcessInput, run_day

debug = False


def run_all(example_run: Union[int, bool]):

    data = ProcessInput(example_run=example_run, day=2, year=2023).data

    adj_data = [[[col.strip() for col in reveal.split(', ')] for reveal in game.split(':')[1].split(';')] for game in data]

    check_cols = {'red': 12, 'green': 13, 'blue': 14}
    sum_ids = 0
    for i, game in enumerate(adj_data):
        check = True
        for reveal in game:
            for color in reveal:
                num, col = color.split(' ')
                if int(num) > check_cols[col]:
                    check = False
        if check:
            sum_ids += (i+1)

    power_sum = 0
    for i, game in enumerate(adj_data):
        min_rgb = {'red': 0, 'green': 0, 'blue': 0}
        for reveal in game:
            for color in reveal:
                num, col = color.split(' ')
                if int(num) > min_rgb[col]:
                    min_rgb[col] = int(num)
        power_sum += min_rgb['red'] * min_rgb['blue'] * min_rgb['green']

    result_part1 = sum_ids
    result_part2 = power_sum

    extra_out = {'Number of games': len(data)}

    return result_part1, result_part2, extra_out


if __name__ == "__main__":
    run_day(run_all, [1])
