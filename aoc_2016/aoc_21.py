from typing import Union
from util.util import ProcessInput, run_day, isnumeric


def run_all(example_run: Union[int, bool]):

    data = ProcessInput(example_run=example_run, day=21, year=2016).data

    text = 'abcde' if example_run else 'abcdefgh'
    text = [x for x in text]

    for row in data:
        if row.startswith('swap position'):
            locs = [int(x) for x in row.split() if isnumeric(x)]
            text[locs[0]], text[locs[1]] = text[locs[1]], text[locs[0]]
        elif row.startswith('swap letter'):
            locs = [text.index(x) for x in row.split()[2:6:3]]
            text[locs[0]], text[locs[1]] = text[locs[1]], text[locs[0]]
        elif row.startswith('reverse'):
            locs = [int(x) for x in row.split() if isnumeric(x)]
            text[locs[0]:locs[1]+1] = [x for x in reversed(text[locs[0]:locs[1]+1])]
        elif row.startswith('rotate based'):
            letter = row.split()[-1]
            steps = text.index(letter)
            steps = steps + 1 if steps < 4 else steps + 2
            steps %= len(text)
            text = text[-steps:] + text[:-steps]
        elif row.startswith('rotate'):
            direction, steps = row.split()[1:3]
            steps = -int(steps) if direction == 'left' else int(steps)
            steps %= len(text)
            text = text[-steps:] + text[:-steps]
        elif row.startswith('move'):
            move_from, move_to = int(row.split()[2]), int(row.split()[5])
            if move_from > move_to:
                text = text[:move_to] + [text[move_from]] + text[move_to:move_from] + text[move_from+1:]
            else:
                text = text[:move_from] + text[move_from+1:move_to+1] + [text[move_from]] + text[move_to+1:]

    result_part1 = "".join(text)

    text = [x for x in 'fbgdceah']
    for row in reversed(data):  # Loop in reverse direction
        if row.startswith('swap position'):  # Reversed same as original
            locs = [int(x) for x in row.split() if isnumeric(x)]
            text[locs[0]], text[locs[1]] = text[locs[1]], text[locs[0]]
        elif row.startswith('swap letter'):  # Reversed same as original
            locs = [text.index(x) for x in row.split()[2:6:3]]
            text[locs[0]], text[locs[1]] = text[locs[1]], text[locs[0]]
        elif row.startswith('reverse'):  # Reversed same as original
            locs = [int(x) for x in row.split() if isnumeric(x)]
            text[locs[0]:locs[1]+1] = [x for x in reversed(text[locs[0]:locs[1]+1])]
        elif row.startswith('rotate based'):
            # Most complicated reverse since it depends on whether letter came from an index < 4 or not.
            # Solution implemented here: go over all possible original locations and see if they work
            letter = row.split()[-1]
            allowed_texts = []  # Keep track of what works
            for try_rotate in range(len(text)):  # Try all possible starting positions for letter
                to_rotate = (try_rotate - text.index(letter)) % len(text)
                try_text = text[-to_rotate:] + text[:-to_rotate]  # Rotate text such that letter would've started there
                try_steps = try_rotate + 1 if try_rotate < 4 else try_rotate + 2  # Calcs from part 1
                try_steps %= len(text)
                if try_text[-try_steps:] + try_text[:-try_steps] == text:  # If result is same as target, then append
                    allowed_texts.append(try_text)
            if len(allowed_texts) == 1:  # Only one allowed_text as possible starting point? Then that one is it!
                text = allowed_texts[0]
            else:
                raise ValueError("Multiple options work - we need to investigate a split path!")  # Not needed for input
        elif row.startswith('rotate'):  # Reversed is original but with -steps (left=right and right=left)
            direction, steps = row.split()[1:3]
            steps = int(steps) if direction == 'left' else -int(steps)
            steps %= len(text)
            text = text[-steps:] + text[:-steps]
        elif row.startswith('move'):   # Reversed is original but with move_to/move_from swapped
            move_to, move_from = int(row.split()[2]), int(row.split()[5])
            if move_from > move_to:
                text = text[:move_to] + [text[move_from]] + text[move_to:move_from] + text[move_from+1:]
            else:
                text = text[:move_from] + text[move_from+1:move_to+1] + [text[move_from]] + text[move_to+1:]

    result_part2 = "".join(text)

    extra_out = {'Number of instructions in input': len(data)}

    return result_part1, result_part2, extra_out


if __name__ == "__main__":
    run_day(run_all, [1])
