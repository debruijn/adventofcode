from typing import Union
from util.util import ProcessInput, run_day

debug = False


def do_workflow(curr_wf, part, workflows):
    # Manual workflow application using eval - no further processing of the input strings needed
    x,m,a,s = part
    workflow = workflows[curr_wf]
    keys = [x for x in workflow.keys()]
    for k in keys:
        if eval(k):
            return workflow[k]
    raise BrokenPipeError


def apply_workflow(workflow, curr_range):
    # Apply workflow on ranges: split curr_range into pieces until going through the full process or curr_range is empty
    # Return list of new ranges for each new key
    out_ranges = {}

    for rule, dest in workflow.items():
        if rule != 'True':
            k = rule[0]
            if rule[1] == '<':
                new_range = curr_range.copy()
                new_range[k] = range(curr_range[k].start, min(curr_range[k].stop, int(rule[2:])))
                if new_range[k].start < new_range[k].stop:
                    if dest not in out_ranges:
                        out_ranges.update({dest: [new_range]})
                    else:
                        out_ranges.update({dest: [new_range] + out_ranges[dest]})
                curr_range[k] = range(int(rule[2:]), curr_range[k].stop)
                if curr_range[k].stop <= curr_range[k].start:
                    return out_ranges
            elif rule[1] == '>':
                new_range = curr_range.copy()
                new_range[k] = range(max(curr_range[k].start, int(rule[2:])+1), curr_range[k].stop)
                if new_range[k].start < new_range[k].stop:
                    if dest not in out_ranges:
                        out_ranges.update({dest: [new_range]})
                    else:
                        out_ranges.update({dest: [new_range] + out_ranges[dest]})
                curr_range[k] = range(curr_range[k].start, int(rule[2:]) + 1)
                if curr_range[k].stop <= curr_range[k].start:
                    return out_ranges
            else:
                raise ValueError
        else:
            if dest not in out_ranges:
                out_ranges.update({dest: [curr_range]})
            else:
                out_ranges.update({dest: [curr_range] + out_ranges[dest]})
            return out_ranges


def apply_workflows(curr_ranges, workflows):
    # Apply workflows for current ranges one by one, and aggregating the outputs together into a new linking of workflows & ranges.
    new_ranges = []
    for k, v in curr_ranges.items():
        if k not in ['A', 'R']:
            for iter_v in v:
                tmp = apply_workflow(workflows[k], iter_v)
                new_ranges.append(tmp)

    out_ranges = {}
    if 'A' in curr_ranges:
        out_ranges['A'] = curr_ranges['A']
    if 'R' in curr_ranges:
        out_ranges['R'] = curr_ranges['R']
    for el in new_ranges:
        for k,v in el.items():
            if k not in out_ranges:
                out_ranges[k] = v
            else:
                out_ranges[k].extend(v)

    return out_ranges


def get_totals(curr_ranges, only=None):
    # Get totals across all ranges in an iteration - useful for debugging purposes.
    # Can also only process a subset of keys, useful for getting final result.
    totals = {}
    super_total = 0
    for k in curr_ranges.keys():
        if not only or k  in only:
            total_options = 0
            for this_range in curr_ranges[k]:
                if type(this_range) == list:
                    for i_range in this_range:
                        total_options += get_total(i_range)
                else:
                    total_options += get_total(this_range)
            totals[k] = total_options
            super_total += total_options
    return totals, super_total


def get_total(curr_range):
    # Get total options for a single range across all XMAS ratings.
    this_options = 1
    for v in curr_range.values():
        this_options *= (v.stop - v.start)
    return this_options


def run_all(example_run: Union[int, bool]):

    data = ProcessInput(example_run=example_run, day=19, year=2023).as_list_of_strings_per_block().data

    # Process workflows and parts
    workflows = {}
    for row in data[0]:
        key, val = row.replace('}', '').split('{')
        rules = [x.split(':') for x in val.split(',')]
        rules = {rule[0]:rule[1] for rule in rules if len(rule)>1}
        rules['True'] = val.split(',')[-1]
        workflows[key] = rules
    parts = [[int(x[2:]) for x in row.replace('{', '').replace('}', '').split(',')] for row in data[1]]

    # Part 1: manually letting parts go through the system
    running_sum = 0
    for part in parts:
        curr_rule = 'in'
        stop = False
        while not stop:
            curr_rule = do_workflow(curr_rule, part, workflows)
            if curr_rule in ['R', 'A']:
                stop = True
        running_sum += sum(part) if curr_rule == 'A' else 0
    result_part1 = running_sum

    # Part 2: split ranges when applying the workflows
    M = 4000
    curr_ranges = {'in': [{x: range(1, M+1) for x in ['x', 'm', 'a', 's']}]}
    while any([k not in ['R', 'A'] for k in curr_ranges]):
        curr_ranges = apply_workflows(curr_ranges, workflows)
        if debug:
            print(get_totals(curr_ranges))

    result_part2 = get_totals(curr_ranges, only=('A',))[0]['A']

    extra_out = {'Number of workflows in input': len(data[0]),
                 'Number of parts in input': len(data[1]),
                 'Number of options in total:': M**4}

    return result_part1, result_part2, extra_out


if __name__ == "__main__":
    run_day(run_all, [1])
