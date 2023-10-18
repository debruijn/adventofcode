from typing import Union
from util.util import run_day


debug = False


def run_all(example_run: Union[int, bool]):

    file = f'aoc_5_exampledata{example_run}' if example_run else 'aoc_5_data'
    with open(file) as f:
        data = f.readlines()
    adj_data = [row.rstrip('\n') for row in data]

    def pass_to_seat(pass_str):
        return int(pass_str.replace('F', '0').replace('B', '1').replace('L', '0').replace('R', '1'), 2)

    seat_ids = [pass_to_seat(row) for row in adj_data]
    my_seat = [seat for seat in range(min(seat_ids), max(seat_ids)) if seat not in seat_ids]

    result_part1 = max(seat_ids)
    result_part2 = my_seat[0] if len(my_seat) > 0 else "NA"

    extra_out = {'Number of seats': len(seat_ids),
                 'Lowest seat number': min(seat_ids),
                 'Highest seat number': max(seat_ids)}
    return result_part1, result_part2, extra_out


if __name__ == "__main__":
    run_day(run_all, [1, 2])
