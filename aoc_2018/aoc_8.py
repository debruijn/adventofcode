from collections import defaultdict
from functools import partial
from typing import Union
from util.util import ProcessInput, run_day, run_rust
from aoc_rust import run_process

debug = False


def run_all(example_run: Union[int, bool], use_rust=False):

    data = ProcessInput(example_run=example_run, day=8, year=2018).as_list_of_ints().data[0]

    if use_rust:
        result_part1, result_part2, nodes = run_process(data)
    else:

        nodes = {}
        children = defaultdict(list)

        def get_metadata_sum(this_data, counter=0, depth=0):
            metadata_sum = 0
            value_list = []
            this_header = this_data[:2]
            this_data = this_data[2:]
            this_counter = counter

            for child in range(this_header[0]):
                children[this_counter].append(counter+1)
                child_metadata, child_value, this_data, counter = get_metadata_sum(this_data, counter+1, depth+1)
                metadata_sum += child_metadata
                value_list.append(child_value)

            nodes[this_counter] = this_header + [sum(this_data[:this_header[1]])] + [depth]
            metadata_sum += sum(this_data[:this_header[1]])
            if len(value_list) > 0:
                value = sum([value_list[x-1] for x in this_data[:this_header[1]] if x <= len(value_list)])
            else:
                value = sum(this_data[:this_header[1]])
            this_data = this_data[this_header[1]:]

            return metadata_sum, value, this_data, counter

        result_part1, result_part2, _, _ = get_metadata_sum(data.copy())

        if debug:
            print(nodes)
            print(children)

    extra_out = {'Number of numbers in input': len(data),
                 'Number of nodes': len(nodes),
                 'Max depth': nodes[max(nodes, key=lambda x: nodes[x][-1])][-1],
                 'Max number of direct children': nodes[max(nodes, key=lambda x: nodes[x][0])][0]}

    return result_part1, result_part2, extra_out


if __name__ == "__main__":
    run_day(partial(run_all, use_rust=False), [1])
    run_day(partial(run_all, use_rust=True), [1])
    run_rust(2018, 8)
