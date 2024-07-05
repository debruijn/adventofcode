import math
from functools import lru_cache
from typing import Union
from util.util import ProcessInput, run_day

debug = True


def is_reachable(loc, enemy):
    return ((abs(loc[0] - enemy[0]) == 1 and loc[1] == enemy[1]) or
            (abs(loc[1] - enemy[1]) == 1 and loc[0] == enemy[0]))

@lru_cache(maxsize=1000000)
def get_next_step(player, candidates, free, checked):
    options = [loc for loc in candidates if is_reachable(player, loc)]
    if len(options) > 0:
        return sorted(options)[0]

    checked += candidates

    def new(loc):
        return [(loc[0], loc[1] - 1), (loc[0], loc[1] + 1), (loc[0] - 1, loc[1]), (loc[0] + 1, loc[1])]

    new_candidates = tuple([x for loc in candidates for x in new(loc) if x in free and x not in checked])
    if len(new_candidates) > 0:
        return get_next_step(player, new_candidates, free, checked)
    return None


def run_all(example_run: Union[int, bool]):

    data = ProcessInput(example_run=example_run, day=15, year=2018).data

    if debug:
        [print(row) for row in data]

    # Create all_locs, elves, goblins, free
    all_locs, elves, goblins, free = [], [], [], []
    for i, row in enumerate(data):
        for j, char in enumerate(row):
            if char != '#':
                all_locs.append((i, j))
                if char == '.':
                    free.append((i, j))
                elif char == 'G':
                    goblins.append([i, j, 200, 3, 0, len(goblins)])
                else:
                    elves.append([i, j, 200, 3, 1, len(elves)])

    round = 0
    stop = False

    while not stop:
        players = sorted(goblins + elves)

        for player in players:
            if player[2] <= 0:
                continue
            enemies = [other_player for other_player in players if player[4] != other_player[4] and other_player[2] > 0]
            reachable = [tuple(loc) for loc in free + [player[:2]] if any(is_reachable(loc, enemy) for enemy in enemies)]

            if tuple(player[:2]) not in reachable:
                next_step = get_next_step(tuple(player[:2]), tuple(reachable), tuple(free), ())
                if next_step is not None:
                    next_step = list(next_step)
                    if debug:
                        print(f"{player} moves to {next_step}")
                    free.append(tuple(player[:2]))
                    player[:2] = next_step
                    free.remove(tuple(next_step))


            if tuple(player[:2]) in reachable:
                targets = [enemy for enemy in enemies if is_reachable(enemy, player[:2])]
                targets = [enemy for enemy in targets if enemy[2] == min(targets, key=lambda x:x[2])[2]]
                target = sorted(targets)[0]
                if debug:
                    print(f"{player} attacks {target}")
                target[2] -= player[3]
                if target[2] <= 0:
                    free.append(tuple(target[:2]))
                    if debug:
                        print(f"{target} dies")
                    if sum(enemy[2]>0 for enemy in enemies) == 0:
                        stop = True
                        if player != [iter_player for iter_player in players if iter_player[2]>0][-1]:
                            round -= 1
                        break

        players = [player for player in players if player[2]>0]
        round += 1

        if debug:
            print(f"Round {round}: {len(players)} left: {sum(x[2] for x in players)}/{sum(x[2] for x in goblins)}/{sum(x[2] for x in elves)} -- {players}")
        print(
            f"Round {round}: {len(players)} left: {sum(x[2] for x in players)}/{sum(x[2] for x in goblins)}/{sum(x[2] for x in elves)}")

    result_part1 = sum(player[2] for player in players) * round
    result_part2 = "TODO"

    extra_out = {'Initial team size': f"{len(goblins)} goblins vs {len(elves)} elves",
                 'Rounds needed for battle': round,
                 'Total players left': len(players),
                 'Total health left': sum(player[2] for player in players)}

    return result_part1, result_part2, extra_out


if __name__ == "__main__":
    run_day(run_all, [1, 2, 3, 4, 5, 6])
