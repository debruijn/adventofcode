from typing import Union
from util import timing


debug = False


@timing
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
    result_part2 = my_seat[0] if len(my_seat) > 0 else "It is not known what"

    print(f'\nResults for {f"example" if example_run else "my"} input{f" {example_run}" if example_run else ""}:')
    print(f' Result of part 1: {result_part1} is the highest seat number')
    print(f' Result of part 2: {result_part2} is still available')

    print(f'\nDescriptives: \n Number of seats: {len(seat_ids)} \n'
          f' Lowest seat number: {min(seat_ids)} \n'
          f' Highest seat number: {max(seat_ids)} \n')


if __name__ == "__main__":
    [run_all(example_run=i) for i in [1, 2]]
    run_all(example_run=False)
