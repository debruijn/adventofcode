from itertools import combinations, product
from typing import Union
from util.util import ProcessInput, run_day


def run_all(example_run: Union[int, bool]):

    # Construct boss stats from input
    data = ProcessInput(example_run=example_run, day=21, year=2015).data
    boss = [int(x) for row in data for x in row.split()[-1:]]

    # All options for weapons, armor and rings. For armor, I add the 0 option with 0 cost. For rings, the same, and I
    # take all combinations, to construct all ways to buy 1 or 2 rings. Then I add a single option to buy 0 rings.
    weapons = [4, 5, 6, 7, 8]
    weapon_cost = [8, 10, 25, 40, 74]

    armor = [0, 1, 2, 3, 4, 5]
    armor_cost = [0, 13, 31, 53, 75, 102]

    rings = [0, 1, 2, 3, -1, -2, -3]
    rings_cost = [0, 25, 50, 100, 20, 40, 80]
    rings_options = list(combinations(range(len(rings)), 2)) + [(0, 0)]

    # Initialize target variables with some upper and lower bound
    best = max(weapon_cost) + max(armor_cost) + 2 * max(rings_cost)
    worst = 0
    for w, a, r in product(range(len(weapons)), armor, rings_options):
        cost = weapon_cost[w] + armor_cost[a] + rings_cost[r[0]] + rings_cost[r[1]]
        attack = weapons[w] + max(rings[r[0]], 0) + max(rings[r[1]], 0)
        defense = a - min(rings[r[0]], 0) - min(rings[r[1]], 0)
        player = [100, attack, defense]
        this_boss = boss.copy()
        turn = 0
        while player[0] > 0 and this_boss[0] > 0:
            if turn == 0:
                this_boss[0] -= max(1, player[1] - this_boss[2])
            else:
                player[0] -= max(1, this_boss[1] - player[2])
            turn = 1 - turn

        if player[0] > 0:
            best = cost if cost < best else best
        else:
            worst = cost if cost > worst else worst

    result_part1 = best
    result_part2 = worst

    extra_out = {'Stats of boss': boss,
                 'Number of combinations to loop over': len(weapons) * len(armor) * len(rings_options)}

    return result_part1, result_part2, extra_out


if __name__ == "__main__":
    run_day(run_all, [])
