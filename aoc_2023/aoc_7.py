from typing import Union
from util.util import ProcessInput, run_day

debug = False


def hand_value_jacks(hand):
    # Return value of hand:
    # - 1st digit 0 to 6 for hand type
    # - remainder of digits consists if individual cards converted to 2-digit integers based on their value

    counts = [hand.count(x) for x in set(hand)]
    if 5 in counts:
        val = 6
    elif 4 in counts:
        val = 5
    elif 3 in counts and 2 in counts:
        val = 4
    elif 3 in counts:
        val = 3
    elif counts.count(2) == 2:
        val = 2
    elif 2 in counts:
        val = 1
    else:
        val = 0

    numeric = ""
    for card in hand:
        if card.isnumeric():
            numeric += ('0'+str(card))
        elif card == 'T':
            numeric += '10'
        elif card == 'J':
            numeric += '11'
        elif card == 'Q':
            numeric +='12'
        elif card == 'K':
            numeric +='13'
        elif card == 'A':
            numeric += '14'
        else:
            raise ValueError(f"Unknown card {card}")

    return int(str(val) + numeric)


def hand_value_jokers(hand):
    # Same setup as above, but separate out Js from hand.
    # With >= 3 Js, you are guaranteed 4 or 5 of a kind, so you can forget about that option for lower scores
    # Same for 2 Js: you are guaranteed 3 of a kind, so below that we can ignore Js at all

    count_Js = hand.count('J')
    counts = [hand.count(x) for x in set(hand) if x != 'J']
    if 5 - count_Js in counts or count_Js == 5:
        val = 6
    elif 4 - count_Js in counts:
        val = 5
    elif counts.count(2) == 2 and count_Js == 1:
        val = 4
    elif 3 in counts and 2 in counts:
        val = 4
    elif 3 - count_Js in counts:
        val = 3
    elif counts.count(2) == 2:
        val = 2
    elif 2 - count_Js in counts:
        val = 1
    else:
        val = 0

    numeric = ""
    for card in hand:
        if card.isnumeric():
            numeric += ('0'+str(card))
        elif card == 'T':
            numeric += '10'
        elif card == 'J':
            numeric += '01'
        elif card == 'Q':
            numeric +='12'
        elif card == 'K':
            numeric +='13'
        elif card == 'A':
            numeric += '14'
        else:
            raise ValueError(f"Unknown card {card}")

    return int(str(val) + numeric)


def run_all(example_run: Union[int, bool]):

    data = ProcessInput(example_run=example_run, day=7, year=2023).data
    data = {row[:5]: int(row[6:]) for row in data}
    keys = data.keys()

    # Part 1
    sorted_keys = sorted(list(keys), key=hand_value_jacks)
    winnings = 0
    for i, key in enumerate(sorted_keys):
        winnings += (i+1) * data[key]
    result_part1 = winnings

    # Part 2
    sorted_keys = sorted(list(keys), key=hand_value_jokers)
    winnings = 0
    for i, key in enumerate(sorted_keys):
        winnings += (i+1) * data[key]
    result_part2 = winnings

    extra_out = {'Number of hands in input': len(data),
                 'Number of hands with Js in them': sum('J' in x for x in keys)}

    return result_part1, result_part2, extra_out


if __name__ == "__main__":
    run_day(run_all, [1])
