from typing import Union
from util.util import ProcessInput, run_day
from intcode_pc import IntCodePC

debug = False

move_map = {x: [ord(y) for y in x] + [10] for x in ["north", "south", "east", "west"]}
inv = [ord(x) for x in "inv"] + [10]
take_map = [ord(x) for x in "take "]
drop_map = [ord(x) for x in "drop "]


def move(string):
    return move_map[string].copy()

def take(string):
    return take_map + [ord(x) for x in string] + [10]

def drop(string):
    return drop_map + [ord(x) for x in string] + [10]

def do_step(pc, command=None, print_out=True):
    output, nr = pc.run_until_end(command)
    pc.clean_out()
    output = "".join(chr(x) for x in output)
    if print_out:
        print(output)

    return output, nr


def run_all(example_run: Union[int, bool]):

    data = ProcessInput(example_run=example_run, day=25, year=2019).as_list_of_ints(',').data[0]

    pc = IntCodePC(data)

    do_step(pc, print_out=debug)
    do_step(pc, move('east'), print_out=debug)
    do_step(pc, take('sand'), print_out=debug)
    do_step(pc, move('west'), print_out=debug)
    do_step(pc, move('west'), print_out=debug)
    do_step(pc, move('west'), print_out=debug)
    do_step(pc, move('north'), print_out=debug)
    do_step(pc, take('wreath'), print_out=debug)
    do_step(pc, move('east'), print_out=debug)
    do_step(pc, take('fixed point'), print_out=debug)
    do_step(pc, move('west'), print_out=debug)
    do_step(pc, move('south'), print_out=debug)
    do_step(pc, move('south'), print_out=debug)
    do_step(pc, move('east'), print_out=debug)
    do_step(pc, move('east'), print_out=debug)
    do_step(pc, move('east'), print_out=debug)
    do_step(pc, take('space law space brochure'), print_out=debug)
    do_step(pc, move('south'), print_out=debug)
    do_step(pc, move('south'), print_out=debug)
    do_step(pc, inv, print_out=debug)
    output, nr = do_step(pc, move('west'), print_out=debug)

    result_part1 = int(output.split('by typing ')[1].split()[0])  # 16778274
    result_part2 = "Merry Christmas"

    extra_out = {'Length of original program': len(data),
                 'Number of items taken': 4,
                 'Number of movements made': 15}

    return result_part1, result_part2, extra_out


if __name__ == "__main__":
    run_day(run_all, [])
