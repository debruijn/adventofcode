from typing import Union
from util.util import ProcessInput, run_day

debug = False


# Note: there are a lot of tuple/list calls because I wanted to make get_next_step() cachable, so I needed tuples as
# input instead of lists. I was too lazy for this AoC day to revert it.


def is_reachable(loc1, loc2):
    return ((abs(loc1[0] - loc2[0]) == 1 and loc1[1] == loc2[1]) or
            (abs(loc1[1] - loc2[1]) == 1 and loc1[0] == loc2[0]))


def neighbors(loc):
    return [(loc[0], loc[1] - 1), (loc[0], loc[1] + 1), (loc[0] - 1, loc[1]), (loc[0] + 1, loc[1])]


def get_next_step(player, candidates, free, checked):
    options = [loc for loc in candidates if is_reachable(player, loc)]
    if len(options) > 0:
        return sorted(options)[0], True

    checked += candidates
    new_candidates = tuple(set([x for loc in candidates for x in neighbors(loc) if x in free and x not in checked]))
    if len(new_candidates) > 0:
        return get_next_step(player, new_candidates, free, checked)
    return (0, 0), False


def create_initial_players(data, attack=3):
    # Create elves, goblins, free
    elves, goblins, free = [], [], []
    for i, row in enumerate(data):
        for j, char in enumerate(row):
            if char == '.':
                free.append((i, j))
            elif char == 'G':
                goblins.append([i, j, 200, 3, 0, len(goblins)])
            elif char == 'E':
                elves.append([i, j, 200, attack, 1, len(elves)])

    return elves, goblins, free


def do_one_game(goblins, elves, free, part2=False):
    game_round = 0
    stop = False
    players = sorted(goblins + elves)

    while not stop:
        players = sorted(goblins + elves)

        for player in players:
            if player[2] <= 0:
                continue

            # Identify enemies and combat locations
            enemies = [other_player for other_player in players if player[4] != other_player[4] and other_player[2] > 0]
            reachable = [tuple(loc) for loc in free + [player[:2]] if
                         any(is_reachable(loc, enemy) for enemy in enemies)]

            # Moving step - if needed
            if tuple(player[:2]) not in reachable:
                next_step, success = get_next_step(tuple(player[:2]), tuple(reachable), tuple(free), ())
                if success:
                    next_step = list(next_step)
                    if debug:
                        print(f"{player} moves to {next_step}")
                    free.append(tuple(player[:2]))
                    player[:2] = next_step
                    free.remove(tuple(next_step))

            # Combat step - if possible
            if tuple(player[:2]) in reachable:
                targets = [enemy for enemy in enemies if is_reachable(enemy, player[:2])]
                targets = [enemy for enemy in targets if enemy[2] == min(targets, key=lambda x: x[2])[2]]
                target = sorted(targets)[0]
                if debug:
                    print(f"{player} attacks {target}")
                target[2] -= player[3]
                if target[2] <= 0:
                    free.append(tuple(target[:2]))
                    if debug:
                        print(f"{target} dies")
                    if sum(enemy[2] > 0 for enemy in enemies) == 0:
                        stop = True
                        if player != [iter_player for iter_player in players if iter_player[2] > 0][-1]:
                            game_round -= 1  # Adjust in case the player was not the last player (so no full round)
                        break

        if part2 and any(elf[2] <= 0 for elf in elves):  # For part 2: no elves can die, so we can stop if that happens
            break

        players = [player for player in players if player[2] > 0]
        game_round += 1

        if debug:
            print(f"Round {game_round}: {len(players)} left: {sum(x[2] for x in players)}/{sum(x[2] for x in goblins)}/"
                  f"{sum(x[2] for x in elves)} -- {players}")

    return game_round, players, all(elf[2] > 0 for elf in elves)


def run_all(example_run: Union[int, bool]):
    data = ProcessInput(example_run=example_run, day=15, year=2018).data

    if debug:
        [print(row) for row in data]

    # Part 1
    elves, goblins, free = create_initial_players(data)
    round_part1, players, _ = do_one_game(goblins, elves, free)
    result_part1 = sum(player[2] for player in players) * round_part1

    # Part 2
    attack_stop = False
    attack = 3
    round_part2 = 0
    while not attack_stop:
        attack += 1
        elves, goblins, free = create_initial_players(data, attack=attack)
        round_part2, players, attack_stop = do_one_game(goblins, elves, free)

    result_part2 = sum(player[2] for player in players) * round_part2

    extra_out = {'Initial team sizes': f"{len(goblins)} goblins vs {len(elves)} elves",
                 'Rounds needed for battle in part 1': round_part1,
                 'Total players left in part 2': len(players),
                 'Total health left in part 2': sum(player[2] for player in players),
                 'Attack of elves needed in part 2': attack,
                 'Rounds needed for battle in part 2': round_part2}

    return result_part1, result_part2, extra_out


if __name__ == "__main__":
    run_day(run_all, [1, 2, 3, 4, 5, 6])
