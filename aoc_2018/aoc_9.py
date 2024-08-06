from typing import Union
from util.util import ProcessInput, run_day
from collections import deque


def run_all(example_run: Union[int, bool]):

    data = ProcessInput(example_run=example_run, day=9, year=2018).as_list_of_ints().data
    nr_players, last_ball = data[0]

    # Part 1: naive implementation
    points = [0]*nr_players
    circle = [0]
    curr_ind = 0
    curr_player = 0

    for new_ball in range(1, last_ball + 1):

        if new_ball % 23 == 0:
            points[curr_player] += new_ball
            curr_ind = (curr_ind - 7) % len(circle)
            points[curr_player] += circle.pop(curr_ind)
            curr_player = (curr_player + 1) % nr_players
        else:
            curr_ind = (curr_ind + 2) % len(circle)
            circle.insert(curr_ind, new_ball)
            curr_player = (curr_player + 1) % nr_players

    result_part1 = max(points)

    # Part 2: deque implementation - to stop inserting etc. Also: calculate current player from which ball we are at.
    last_ball *= 100
    points = [0]*nr_players
    circle = deque([0])

    for new_ball in range(1, last_ball + 1):
        if new_ball % 23 == 0:
            circle.rotate(-7)
            points[new_ball % nr_players] += new_ball + circle.pop()
        else:
            circle.rotate(2)
            circle.append(new_ball)

    result_part2 = max(points)

    extra_out = {'Number of players in game': nr_players,
                 'Number of balls played (in game 1)': int(last_ball / 100)}

    return result_part1, result_part2, extra_out


if __name__ == "__main__":
    run_day(run_all, [1, 2, 3, 4, 5, 6])
