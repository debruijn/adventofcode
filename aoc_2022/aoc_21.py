import z3
from typing import Union
from util.util import timing

debug = False


def part1(data):

    monkeys = [row.split(': ') for row in data]

    monkey_nrs = {}
    result = "Did not find"
    while monkeys:
        monkey = monkeys.pop(0)
        if monkey[1].find(' ') == -1:
            monkey_nrs.update({monkey[0]: int(monkey[1])})
        else:
            monkeys_iter = monkey[1].split(' ')
            if monkeys_iter[0] in monkey_nrs and monkeys_iter[2] in monkey_nrs:
                monkey_nrs.update(
                    {monkey[0]: int(eval(f"{monkey_nrs[monkeys_iter[0]]} {monkeys_iter[1]} "
                                         f"{monkey_nrs[monkeys_iter[2]]}"))})
                if monkey[0] == 'root':
                    result = monkey_nrs['root']
                    monkeys = False
            else:
                monkeys.append(monkey)

    return result


def part2(data):

    s = z3.Solver()
    humn = z3.Int('humn')
    monkeys = [row.split(': ') for row in data]

    monkey_nrs = {}
    result = "Did not find"

    while monkeys:
        monkey = monkeys.pop(0)
        if monkey[1].find(' ') == -1:
            if monkey[0] == 'humn':
                monkey_nrs.update({'humn': humn})
            else:
                monkey_nrs.update({monkey[0]: int(monkey[1])})
        else:
            monkeys_iter = monkey[1].split(' ')
            if monkeys_iter[0] in monkey_nrs and monkeys_iter[2] in monkey_nrs:
                if monkey[0] == 'root':
                    s.add(eval(monkey_nrs[monkeys_iter[0]] + "==" + monkey_nrs[monkeys_iter[2]]))
                    assert s.check() == z3.sat
                    model = s.model()
                    result = model[humn]
                    # Or simply: z3.solve(eval(monkey_nrs[monkeys_iter[0]] + "==" + monkey_nrs[monkeys_iter[2]]))
                    monkeys = False
                else:
                    monkey_nrs.update({monkey[0]: f"({monkey_nrs[monkeys_iter[0]]}) "
                                                  f"{monkeys_iter[1]} ({monkey_nrs[monkeys_iter[2]]})"})
            else:
                monkeys.append(monkey)

    return result


@timing
def run_all(example_run: Union[int, bool]):
    file = f'aoc_21_exampledata{example_run}' if example_run else 'aoc_21_data'
    with open(file) as f:
        data = f.readlines()
    adj_data = [row.rstrip('\n') for row in data]

    result_part1 = part1(adj_data)
    result_part2 = part2(adj_data)

    print(f'\nResults for {f"example" if example_run else "my"} input{f" {example_run}" if example_run else ""}:')
    print(f' Result of part 1: {result_part1}')
    print(f' Result of part 2: {result_part2}')

    print(f'\nDescriptives: \n Number of monkeys: {len(adj_data)} \n')


if __name__ == "__main__":
    [run_all(example_run=i) for i in [1]]
    run_all(example_run=False)
