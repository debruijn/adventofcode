from typing import Union
from util.util import ProcessInput, run_day

debug = False


def combat(stacks, simple=True):
    history = []
    while len(stacks[0]) * len(stacks[1]) > 0:
        # Check if current card order has happened already in this game (-1 as divider between stacks)
        this_order = stacks[0] + [-1,] + stacks[1]
        if this_order in history:  # Player 1 wins if this card order has occurred already in this game
            return 0
        else:
            history.append(this_order)

        # Find winner of round; either by comparing top_cards or by playing subgame (if not simple and we can recurse)
        top_cards = [stack.pop(0) for stack in stacks]
        if simple or not (len(stacks[0]) >= top_cards[0] and len(stacks[1]) >= top_cards[1]):
            winner = 0 if top_cards[0] > top_cards[1] else 1
        else:
            winner = combat([stacks[0][:top_cards[0]].copy(), stacks[1][:top_cards[1]].copy()], simple=simple)

        if winner == 0:
            stacks[0].extend(top_cards)
        else:
            stacks[1].extend([top_cards[1], top_cards[0]])
    return 0 if len(stacks[1]) == 0 else 1


def run_all(example_run: Union[int, bool]):
    data = ProcessInput(example_run=example_run, day=22).as_list_of_strings_per_block().data

    stacks_p1 = [[int(x) for x in stack[1:]] for stack in data]
    winner_p1 = combat(stacks_p1)
    score_p1 = sum([sum([(len(stack) - i) * x for i, x in enumerate(stack)]) for stack in stacks_p1])

    stacks_p2 = [[int(x) for x in stack[1:]] for stack in data]
    winner_p2 = combat(stacks_p2, simple=False)
    score_p2 = sum([sum([(len(stack) - i) * x for i, x in enumerate(stack)]) for stack in stacks_p2])

    result_part1 = score_p1
    result_part2 = score_p2

    extra_out = {'Number of players': len(data),
                 'Number of cards:': sum([len(stack) for stack in stacks_p1]),
                 'Winning player game 1': winner_p1 + 1,
                 'Winning player game 2': winner_p2 + 1}

    return result_part1, result_part2, extra_out


if __name__ == "__main__":
    run_day(run_all, [1, 2])
