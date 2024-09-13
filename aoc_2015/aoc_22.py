from typing import Union
from util.util import ProcessInput, run_day


def run_all(example_run: Union[int, bool]):

    if example_run:  # From text
        boss = [12 + example_run, 8]
        player = [10, 250]
    else:
        data = ProcessInput(example_run=example_run, day=22, year=2015).data
        boss = [int(x) for row in data for x in row.split()[-1:]]
        player = [50, 500]

    mana_cost = [53, 73, 113, 173, 229]

    def play_game(difficult=0):
        best_yet = 10000000000
        queue = [(0, boss[0], player[0], player[1], (0, 0, 0))]

        while len(queue) > 0:
            mana_done, hp_boss, hp_player, mana, effects = queue.pop()

            # Apply effects for start of player's turn
            if effects[1] > 0:
                hp_boss -= 3
            if effects[2] > 0:
                mana += 101
            effects = tuple(max(0, x - 1) for x in effects)
            hp_player -= difficult

            # Some checks to terminate (good or bad) which have to be done in this exact order
            if hp_player <= 0:
                continue
            if hp_boss <= 0:
                best_yet = mana_done if mana_done < best_yet else best_yet
                continue
            if mana < mana_cost[0] or mana_done + mana_cost[0] >= best_yet:
                continue

            # Available options based on cost and already-active effects
            options = [i for i in range(5) if mana_cost[i] <= mana and (i < 2 or effects[i - 2] == 0)]

            # Already do the effects of bosses turn since the available options are decided already -> avoids redoing
            armor = 7 if effects[0] > 0 else 0
            if effects[1] > 0:
                hp_boss -= 3
            if effects[2] > 0:
                mana += 101
            effects = tuple(max(0, x - 1) for x in effects)

            # Do Magic Missile
            if hp_boss <= 4:  # If boss will die due to poison and/or Magic Missile anyway, don't even try something else
                best_yet = mana_done + mana_cost[0] if mana_done + mana_cost[0] < best_yet else best_yet
                continue
            else: # We will always have mana for MM - no need to test
                boss_dmg = max(boss[1] - armor, 1)
                if hp_player > boss_dmg:
                    queue.append((mana_done + mana_cost[0], hp_boss - 4,
                                  hp_player - boss_dmg, mana - mana_cost[0], effects))

            # Do Drain
            if 1 in options:
                boss_dmg = max(boss[1] - armor, 1)
                if hp_player + 2 > boss_dmg:
                    queue.append((mana_done + mana_cost[1], hp_boss - 2,
                                  hp_player + 2 - boss_dmg, mana - mana_cost[1], effects))

            # Do Shield
            if 2 in options:
                boss_dmg = max(boss[1] - 7, 1)
                if hp_player > boss_dmg:
                    this_effects = (6-1,) + effects[1:]
                    queue.append((mana_done + mana_cost[2], hp_boss,
                                  hp_player - boss_dmg, mana - mana_cost[2], this_effects))

            # Do Poison
            if 3 in options:
                boss_dmg = max(boss[1] - armor, 1)
                if hp_player > boss_dmg:
                    this_effects = (effects[0], 6-1, effects[2])
                    queue.append((mana_done + mana_cost[3], hp_boss - 3,
                                  hp_player - boss_dmg, mana - mana_cost[3], this_effects))

            # Do Recharge
            if 4 in options:
                boss_dmg = max(boss[1] - armor, 1)
                if hp_player > boss_dmg:
                    this_effects = effects[:2] + (5-1,)
                    queue.append((mana_done + mana_cost[4], hp_boss,
                                  hp_player - boss_dmg, mana - mana_cost[4] + 101, this_effects))

        return best_yet

    result_part1 = play_game()
    result_part2 = play_game(difficult=1) if not example_run else "N/A"

    extra_out = {'Boss stats': boss}

    return result_part1, result_part2, extra_out


if __name__ == "__main__":
    run_day(run_all, [1, 2])
