from typing import Union
from util.util import ProcessInput, run_day
from operator import and_, or_, xor


def as_num(zs, values):
    return sum([2**i for i, z in enumerate(sorted(zs)) if values[z]])


def run_all(example_run: Union[int, bool]):

    starts, logic = ProcessInput(example_run=example_run, day=24, year=2024).as_list_of_strings_per_block().data

    # Processing of starting values and mappings into a usable format (e.g. process strings only once)
    values = {row.split(': ')[0]: True if row.split(': ')[1] == '1' else False for row in starts}
    mapping = {}
    zs = []
    for row in logic:
        v, k = row.split(' -> ')
        v = v.split(' ')
        mapping[k] = [v[0], v[2], and_ if v[1] == 'AND' else or_ if v[1] == 'OR' else xor]
        if k.startswith('z'):
            zs.append(k)

    # Part 1: keep updating all values until you have an answer in all z's
    while not all(z in values.keys() for z in zs):
        for k, v in mapping.items():
            if v[0] in values and v[1] in values:
                values[k] = v[2](values[v[0]], values[v[1]])

    # Part 2: use logic based around bit-adders
    z_max = sorted(zs)[-1]
    swapped = list()
    # After messing with it manually, mapping is wrong for 1 of 4 reasons:
    # 1. If result starts with z but operation is not an XOR (since: z00 = x00 ^ y00; z01 = x01 ^ y01 ^ (x00 & y00))
    #    (except for the "extra" z that would only carry the extra bit if needed, like in 10 + 10 = 100)
    # 2. Reverse: if it uses an XOR, it needs to involve an x, y or z. If not, it's wrong.
    # 3. If doing an A AND B == C, that is to represent the "carry the 1" in addition, which can be from two routes
    #    (the nums themselves, or one of them and the previous carry over) which can also be both true, so usage of C
    #    would have to involve an OR. So AND -> AND or AND -> XOR are wrong. (Exception for 1st step)
    # 4. An XOR is only used for one of the two routes above which results in an AND or another XOR but not an OR. So
    #    XOR -> OR is wrong.
    # These reasons can overlap, so make sure to break/continue to avoid double-counting (also, we could've used a set)
    for k, (v1, v2, op) in mapping.items():
        if k[0] == "z" and op != xor and k != z_max:
            swapped.append(k)  # Reason 1
            continue
        if op == xor and k[0] not in "xyz" and v1[0] not in "xyz" and v2[0] not in "xyz":
            swapped.append(k)  # Reason 2
            continue
        if op == and_ and "x00" not in [v1, v2]:
            for (nxt_v1, nxt_v2, nxt_op) in mapping.values():
                if (k == nxt_v1 or k == nxt_v2) and nxt_op != or_:
                    swapped.append(k)  # Reason 3
                    break
        if op == xor:
            for (nxt_v1, nxt_v2, nxt_op) in mapping.values():
                if (k == nxt_v1 or k == nxt_v2) and nxt_op == or_:
                    swapped.append(k)  # Reason 4
                    break

    result_part1 = as_num(zs, values)
    result_part2 = ",".join(sorted(swapped))

    extra_out = {'Number of givens in input': len(starts),
                 'Number of mapping in input': len(logic),
                 'Number of bits in z': len(zs)}

    return result_part1, result_part2, extra_out


if __name__ == "__main__":
    run_day(run_all, [1, 2])
