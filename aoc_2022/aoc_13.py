import functools


debug = False


def compare(packet1, packet2, prefix=""):
    if debug:
        print(f"{prefix}Compare: {packet1} vs {packet2}")

    if type(packet1) == int and type(packet2) == int:
        return 1 if packet1 < packet2 else 0 if packet1 == packet2 else -1
    elif type(packet1) == int and not type(packet2) == int:
        return compare([packet1], packet2, prefix=prefix)
    elif type(packet2) == int and not type(packet1) == int:
        return compare(packet1, [packet2], prefix=prefix)
    else:
        range_min_packet = int(min(len(packet1), len(packet2)))
        for j in range(range_min_packet):
            status_iter = compare(packet1[j], packet2[j], prefix=prefix + " ")
            if status_iter != 0:
                return status_iter
        if len(packet1) < len(packet2):
            return 1
        elif len(packet2) < len(packet1):
            return -1
        return 0


def run_all(example_run, distress_signals=None):
    if distress_signals is None:
        distress_signals = [[2], [6]]
    file = f'aoc_13_exampledata{example_run}' if example_run else 'aoc_13_data'
    with open(file) as f:
        data = f.readlines()
    adj_data = [row.rstrip('\n') for row in data]
    n_pairs = int((len(adj_data) + 1) / 3)

    sum_right_order = 0
    for i in range(n_pairs):
        packet1 = eval(adj_data[3 * i])
        packet2 = eval(adj_data[3 * i + 1])
        sum_right_order = sum_right_order + (i + 1) if compare(packet1, packet2) == 1 else sum_right_order

    result_part1 = sum_right_order

    adj_data = [eval(row) for row in adj_data if row != '']
    adj_data.append(distress_signals[0])
    adj_data.append(distress_signals[1])

    adj_data.sort(key=functools.cmp_to_key(compare), reverse=True)

    result_part2 = [i for i in range(len(adj_data)) if adj_data[i] in distress_signals]
    result_part2 = (result_part2[0] + 1) * (result_part2[1] + 1)
    # Alt: result_part2 = (adj_data.index(distress_signals[0]) + 1) * (adj_data.index(distress_signals[1]) + 1)

    print(f'Results for {f"example" if example_run else "my"} input{f" {example_run}" if example_run else ""}:')
    print(f' Result of part 1: {result_part1}')
    print(f' Result of part 2: {result_part2}')

    print(f'\nDescriptives: \n {n_pairs} pairs in part 1'
          f'\n {len(adj_data)} packets to sort in part 2'
          f'\n Biggest packet: {adj_data[-1]}'
          f'\n Smallest packet: {adj_data[0]} \n\n')


[run_all(example_run=i) for i in [1]]
run_all(example_run=False)
