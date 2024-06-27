from collections import defaultdict
from typing import Union
from util.util import ProcessInput, run_day

debug = False


def run_all(example_run: Union[int, bool]):

    data = ProcessInput(example_run=example_run, day=8, year=2018).as_list_of_ints().data[0]
    nodes = {}
    childs = defaultdict(list)

    def get_metadata_sum(this_data, counter=0, depth=0):
        metadata_sum = 0
        this_header = this_data[:2]
        this_data = this_data[2:]

        this_counter = counter

        for child in range(this_header[0]):
            childs[this_counter].append(counter+1)
            child_metadata, this_data, counter = get_metadata_sum(this_data, counter+1, depth+1)
            metadata_sum += child_metadata

        nodes[this_counter] = this_header + [sum(this_data[:this_header[1]])] + [depth]
        metadata_sum += sum(this_data[:this_header[1]])
        this_data = this_data[this_header[1]:]

        return metadata_sum, this_data, counter

    metadata_sum, _, counter = get_metadata_sum(data.copy())

    if debug:
        print(nodes)
        print(childs)

    result_part1 = metadata_sum

    def get_value(this_data, counter=0, depth=0):
        value = []
        this_header = this_data[:2]
        this_data = this_data[2:]

        this_counter = counter

        for child in range(this_header[0]):
            childs[this_counter].append(counter+1)
            child_value, this_data, counter = get_value(this_data, counter+1, depth+1)
            value.append(child_value)

        if len(value) > 0:
            value = sum([value[x-1] for x in this_data[:this_header[1]] if x <= len(value)])
        else:
            value = sum(this_data[:this_header[1]])
        this_data = this_data[this_header[1]:]

        return value, this_data, counter

    value = get_value(data)

    result_part2 = value[0]

    extra_out = {'Number of numbers in input': len(data),
                 'Number of nodes': len(nodes),
                 'Max depth': nodes[max(nodes, key=lambda x: nodes[x][-1])][-1]}

    return result_part1, result_part2, extra_out


if __name__ == "__main__":
    run_day(run_all, [1])
