from typing import Union
from util.util import ProcessInput, run_day

debug = False


# As part of me trying to guess part 2, I have actually found a loop: after about 2000 to 3000 iters (for part 1), you
# are in the same situation as sometime before again, so you can "calculate" future iterations quickly from that history
# Totally useless for the actual part 2, though... :( (it is the code related to 'hist' below in part_1)


def part_1(label, n_moves=100):
    len_label = len(label)

    def get_dest(label_f, curr_val):
        curr_val = len_label + 1 if curr_val == 1 else curr_val
        return label_f.index(curr_val - 1) if curr_val - 1 in label_f else get_dest(label_f, curr_val - 1)

    curr_cup_ind = 0
    hist = []
    i = 0
    for i in range(n_moves):
        curr_cup_val = label[curr_cup_ind]

        pick_up = [label[x] for x in [(curr_cup_ind + i) % len_label for i in range(1, 4)]]
        [label.remove(x) for x in pick_up]

        dest = get_dest(label, curr_cup_val)
        pick_up.reverse()
        [label.insert(dest+1, cup) for cup in pick_up]

        curr_cup_ind = label.index(curr_cup_val)
        if debug:
            print(f"{i}: {label[:100]}; {curr_cup_ind}/{curr_cup_val}; {dest}")

        curr_cup_ind = (curr_cup_ind + 1) % len_label

        index_1 = label.index(1)
        res = [curr_cup_val] + [label[x] for x in [(index_1 + i) % len_label for i in range(1, len_label)]]

        if res not in hist:
            hist.append(res)
        else:
            print(f"{i}: {hist.index(res)}")
            break
    if n_moves > i+1:
        label = hist[((n_moves - i) % (i - hist.index(res))) + hist.index(res) - 1][1:]

    index_1 = label.index(1)
    res = [label[x] for x in [(index_1 + i) % len_label for i in range(1, len_label)]]
    return int("".join([str(x) for x in res]))


def part_2(label, nr_items=1000000, n_moves=10000000, n_take=2):
    # Map all "extra" cups to the next cup
    mapping = [i + 1 for i in range(nr_items + 1)]
    # Remap "original" cups to the original "next cup", so 3 to 8, 8 to 9 etc in example
    for i, cup in enumerate(label[:-1]):  # Map
        mapping[cup] = label[i+1]

    curr = label[0]
    if nr_items > len(label):
        mapping[-1] = curr  # Fix mapping from final element to first (curr) element (e.g. 1000000 to 3 in example)
        mapping[label[-1]] = max(label) + 1  # Fix mapping from final original element to first new one (e.g. 7 to 10)
    else:
        mapping[label[-1]] = curr  # Fix mapping for 7 to 3 in example (last to first element)

    # Result of the above: a mapping from each cup to what is the next: mapping[5] gives the cup after cup 5

    for i in range(n_moves):
        # Pick up 3 cups; save the first for later
        first_pickup = mapping[curr]
        mapping[curr] = mapping[mapping[mapping[first_pickup]]]  # Update mapping to whatever the final pick-up mapped
        pick_up = [first_pickup, mapping[first_pickup], mapping[mapping[first_pickup]]]

        # Function get_dest() from part 1 is not useful anymore, since mapping != label. Perhaps also simpler:
        dest = curr - 1 if curr > 1 else nr_items
        while dest in pick_up:
            dest = nr_items if dest == 1 else dest - 1

        # Update mapping from final pickup to the one after dest, and mapping from dest to first of pickup
        mapping[pick_up[-1]] = mapping[dest]
        mapping[dest] = first_pickup

        # Take the next cup
        curr = mapping[curr]

    # To take items after 1, look them up in mapping:
    final_cup = 1
    to_return = []
    for _ in range(n_take):
        final_cup = mapping[final_cup]
        to_return.append(final_cup)

    return to_return


def run_all(example_run: Union[int, bool]):

    data = ProcessInput(example_run=example_run, day=23, year=2020).data

    # Part 1, original approach
    label = [int(x) for x in data[0]]
    result_part1 = part_1(label, n_moves=100)

    # Part 1, faster approach from part 2
    if debug:
        label = [int(x) for x in data[0]]
        print(part_2(label, nr_items=9, n_moves=10, n_take=8))

    # Actual part 2
    label = [int(x) for x in data[0]]
    next_items = part_2(label, nr_items=1000000, n_moves=10000000, n_take=2)
    result_part2 = next_items[0] * next_items[1]

    extra_out = {'Number of rows in input': len(data)}  # TODO: create dict of additional things to have them printed

    return result_part1, result_part2, extra_out


if __name__ == "__main__":
    run_day(run_all, [1])
