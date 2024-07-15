from typing import Union
from util.util import ProcessInput, run_day, multisplit


def attack_multiplier(attacker, defender):
    return 2 if attacker['attack_type'] in defender['weak'] else \
        0 if attacker['attack_type'] in defender['immune'] else 1


def target_selection(attackers, defenders):
    potential_targets = defenders.copy()
    targets = {}
    for group in attackers:
        if len(potential_targets) == 0:
            continue
        max_multiplier = attack_multiplier(group, max(potential_targets, key=lambda x: attack_multiplier(group, x),
                                                      default=0))  # group['units'] * group['attack']
        if max_multiplier == 0:
            continue
        this_targets = [x for x in potential_targets if attack_multiplier(group, x) == max_multiplier]
        this_target = sorted(sorted(this_targets, key=lambda x: x['initiative'], reverse=True),
                             key=lambda x: x['units'] * x['attack'], reverse=True)[0]
        potential_targets.remove(this_target)
        targets[group['initiative']] = this_target['initiative']
    return targets


def process_team(team, example_run=False, team_name='immune', boost=0):
    if example_run:  # In example the input is split across multiple lines; combine them for compatibility
        team = [team[0] + team[1], team[2] + team[3]]

    proc_team = []
    for i, group in enumerate(team):
        units = int(group.split(' ', 1)[0])
        hp = int(multisplit(group, ['with ', ' hit points'])[1])
        weak = []
        immune = []
        if '(' in group:
            weak_immune = multisplit(group, ['(', ')'])[1]
            if 'weak' in weak_immune:
                weak = weak_immune.split('weak to ')[1].split('; ')[0].split(', ')
            if 'immune' in weak_immune:
                immune = weak_immune.split('immune to ')[1].split('; ')[0].split(', ')

        attack = int(group.split('that does ')[1].split(' ')[0]) + boost
        attack_type = group.split('that does ')[1].split('damage')[0].split(' ')[1]
        initiative = int(group.split(' ')[-1])

        this_proc = {"units": units, "hp": hp, "weak": weak, "immune": immune, "attack": attack,
                     "attack_type": attack_type, "initiative": initiative, "name": f"{team_name}_{i}"}
        proc_team.append(this_proc)

    return proc_team


def run_for_boost(data, example_run, boost):

    # Processing, potentially taking boost into account
    immune_team = process_team(data[0][1:], example_run, boost=boost)
    infection_team = process_team(data[1][1:], example_run, team_name='infection')
    all_groups = immune_team + infection_team
    all_groups_by_initiative = {x['initiative']: x for x in all_groups}

    round, prev_sum, this_sum = 0, 0, 1
    while len(immune_team) * len(infection_team) > 0 and prev_sum != this_sum:  # One team is dead, or there is a draw

        # Sort both teams by effective power and initiative (reverse order to account for priority)
        immune_team.sort(key=lambda x: x['initiative'], reverse=True)
        immune_team.sort(key=lambda x: x['units'] * x['attack'], reverse=True)
        infection_team.sort(key=lambda x: x['initiative'], reverse=True)
        infection_team.sort(key=lambda x: x['units'] * x['attack'], reverse=True)

        # Target selection
        targets = {}
        targets.update(target_selection(immune_team, infection_team))
        targets.update(target_selection(infection_team, immune_team))

        # Fighting
        attack_order = sorted(list(targets.keys()), reverse=True)
        for group in attack_order:
            attacker = all_groups_by_initiative[group]
            if attacker['units'] <= 0:
                continue
            defender = all_groups_by_initiative[targets[group]]
            damage = attack_multiplier(attacker, defender) * attacker['units'] * attacker['attack']
            units_killed = damage // defender['hp']
            defender['units'] = defender['units'] - units_killed
            if defender['units'] <= 0:
                if defender in immune_team:
                    immune_team.remove(defender)
                else:
                    infection_team.remove(defender)

        round += 1
        prev_sum = this_sum
        this_sum = sum([x['units'] for x in immune_team]) + sum([x['units'] for x in infection_team])

    return (sum([x['units'] for x in immune_team]) + sum([x['units'] for x in infection_team]), len(immune_team),
            len(infection_team), round)


def run_all(example_run: Union[int, bool]):

    data = ProcessInput(example_run=example_run, day=24, year=2018).as_list_of_strings_per_block().data

    result_part1 = run_for_boost(data, example_run, 0)

    step_size = 1000
    curr_boost = step_size  # We don't need to try boost=0, so we immediately apply step_size
    lb = 0  # Lowerbound of solution, e.g. we know the solution is higher than this
    while True:
        try_boost = run_for_boost(data, example_run, curr_boost)
        if try_boost[2] != 0:
            curr_boost += step_size
        if try_boost[2] == 0:
            lb = max(lb, curr_boost - step_size)
            step_size //= 10
            if step_size == 0:
                break
            curr_boost = lb + step_size

    result_part2 = try_boost[0]

    extra_out = {'Number of groups in immune team': len(data[0]) - 1,
                 'Number of groups in infection team': len(data[1]) - 1,
                 'Number of rounds in part 1': result_part1[3],
                 'Number of rounds in part 2': try_boost[3],
                 'Required boost in part 2': curr_boost}

    return result_part1[0], result_part2, extra_out


if __name__ == "__main__":
    run_day(run_all, [1])
