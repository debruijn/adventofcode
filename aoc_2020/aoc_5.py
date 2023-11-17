from typing import Union
from util.util import run_day, get_example_data
from aocd import get_data


debug = False


def run_all(example_run: Union[int, bool]):

    if example_run:
        adj_data = get_example_data(2020, 5, example_run-1)
    else:
        data_raw = get_data(day=5, year=2020)
        adj_data = [x for x in data_raw.split('\n')]

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
