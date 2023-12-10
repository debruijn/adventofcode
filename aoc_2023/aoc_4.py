from typing import Union
from util.util import ProcessInput, run_day

debug = False


def run_all(example_run: Union[int, bool]):

    data = ProcessInput(example_run=example_run, day=4, year=2023).data
    data = [row.split(': ')[1].split(' | ') for row in data]

    points = 0
    total_matches = []
    for card in data:
        winning_nrs = [int(x) for x in card[0].split(' ') if x != '']
        my_nrs = [int(x) for x in card[1].split(' ') if x != '']

        card_match = sum([x in winning_nrs for x in my_nrs])
        if card_match > 0:
            points += 2**(card_match-1)
            total_matches.append(card_match)
        else:
            total_matches.append(0)

    total_card_count = 0
    nr_copies = [1] * len(total_matches)
    for i, card in enumerate(total_matches):
        total_card_count += nr_copies[i]
        for j in range(i+1, i+1+card):
            nr_copies[j] += nr_copies[i]

    result_part1 = points
    result_part2 = total_card_count

    extra_out = {'Number of cards in input': len(data)}

    return result_part1, result_part2, extra_out


if __name__ == "__main__":
    run_day(run_all, [1])
