from typing import Union
from util.util import ProcessInput, run_day


move_mapping = {'>': 1j, '<': -1j, 'v': 1, '^': -1}


def process_grid(data, mult=1):
    # Process grid for both parts
    boxes, free, robot = [], [], 0
    for i, row in enumerate(data):
        for j, el in enumerate(row):
            if el in '.O@':
                free.append(i + j*mult*1j)
                if mult > 1:
                    free.append(i + j*mult*1j + 1j)
                if el == 'O':
                    boxes.append(i + j*mult*1j) # Left side of same box
                if el == '@':
                    robot = i + j*mult*1j

    return boxes, free, robot


def get_gps(boxes):
    return int(sum(100 * x.real + x.imag for x in boxes))

def run_all(example_run: Union[int, bool]):

    data = ProcessInput(example_run=example_run, day=15, year=2024).as_list_of_strings_per_block().data

    boxes, free, robot = process_grid(data[0], mult=1)
    moves = "".join(data[1])

    for move in moves:
        move = move_mapping[move]
        stack, curr = [robot], robot
        stop = False
        while not stop:
            if curr+move in boxes:
                curr = curr + move
                stack.append(curr)
                continue
            if curr+move in free:
                robot += move
                if len(stack) > 1:
                    boxes.remove(stack[1])
                    boxes.append(curr+move)
            break

    result_part1 = get_gps(boxes)

    boxes, free, robot = process_grid(data[0], mult=2)

    for move in moves:
        move = move_mapping[move]
        stack, curr = {}, {robot}
        stop = False
        while not stop:
            # Keep checking if any of the current boxes have top neighbor(s) that can be pushed until you find frontier
            curr_before = curr.copy()
            for cr in curr_before:
                if cr+move in boxes:
                    curr.add(cr+move)
                if cr+move-1j in boxes:
                    curr.add(cr+move-1j)
                if cr != robot:
                    if cr+move+1j in boxes:
                        curr.add(cr+move+1j)
            if curr != curr_before:
                continue

            # Check if frontier is fully free to move -> if not, break
            if any(cr+move not in free for cr in curr) or any(cr+move+1j not in free for cr in curr if cr != robot):
                break

            # If move can be done, process it
            for cr in curr:
                if cr != robot:
                    boxes.remove(cr)
                    boxes.append(cr+move)
            robot += move
            break

    result_part2 = get_gps(boxes)

    extra_out = {'Dimension of grid in input': (len(data[0]), len(data[0][0])),
                 'Number of steps to take': len(moves)}

    return result_part1, result_part2, extra_out


if __name__ == "__main__":
    run_day(run_all, [3, 2, 1])
