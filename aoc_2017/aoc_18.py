from collections import defaultdict
from typing import Union
from util.util import ProcessInput, run_day, isnumeric


def run_all(example_run: Union[int, bool]):

    if example_run == 2:
        data = ["snd 1", "snd 2", "snd p", "rcv a", "rcv b", "rcv c", "rcv d"]
    else:
        data = ProcessInput(example_run=example_run, day=18, year=2017).data

    # Part 1: directly go through all instructions, use a defaultdict to initialize new register entries at 0
    register = defaultdict(int)
    most_recent_sound = -1  # Keep track of the most recent output to "sound" in this variable
    curr_instr = 0
    n_instr1 = 0
    while 0 <= curr_instr < len(data):
        row = data[curr_instr].split(' ')
        n_instr1 += 1
        if row[0] == 'snd':
            most_recent_sound = register[row[1]]
            curr_instr += 1
        elif row[0] == 'set':
            register[row[1]] = int(row[2]) if isnumeric(row[2]) else register[row[2]]
            curr_instr += 1
        elif row[0] == 'add':
            register[row[1]] += int(row[2]) if isnumeric(row[2]) else register[row[2]]
            curr_instr += 1
        elif row[0] == 'mul':
            register[row[1]] *= int(row[2]) if isnumeric(row[2]) else register[row[2]]
            curr_instr += 1
        elif row[0] == 'mod':
            register[row[1]] %= int(row[2]) if isnumeric(row[2]) else register[row[2]]
            curr_instr += 1
        elif row[0] == 'rcv':
            if register[row[1]] != 0:
                break
            curr_instr += 1
        elif row[0] == 'jgz':
            curr_instr += int(row[2]) if register[row[1]] > 0 else 1

    result_part1 = most_recent_sound

    # Part 2: 2 registers, defaulting to 0 and 1; 2 queues; 2 current instructions, etc.
    # Utility variables: "waiting" and "done" to indicate whether a program is:
    # - waiting for the other (and not doing anything in the mean time)
    # - done, because it's instruction number is outside the valid range
    # When adding an entry to the other program's queue, the other's "waiting" is reset to False
    register = [defaultdict(int), defaultdict(lambda: 1)]
    queue = [[], []]
    curr_instr = [0, 0]
    n_instr2 = 0
    waiting = [False, False]
    done = [False, False]
    count_send_by_1 = 0
    while not all(waiting[i] or done[i] for i in (0, 1)):
        for i in (0, 1):
            if waiting[i] or done[i]:
                continue
            row = data[curr_instr[i]].split(' ')
            n_instr2 += 1
            if row[0] == 'snd':
                if len(queue[1-i]) == 0:
                    waiting[1-i] = False  # If we send something, the other can stop waiting
                queue[1-i].append(int(row[1]) if isnumeric(row[1]) else register[i][row[1]])
                curr_instr[i] += 1
                if i == 1:
                    count_send_by_1 += 1
            elif row[0] == 'set':
                register[i][row[1]] = int(row[2]) if isnumeric(row[2]) else register[i][row[2]]
                curr_instr[i] += 1
            elif row[0] == 'add':
                register[i][row[1]] += int(row[2]) if isnumeric(row[2]) else register[i][row[2]]
                curr_instr[i] += 1
            elif row[0] == 'mul':
                register[i][row[1]] *= int(row[2]) if isnumeric(row[2]) else register[i][row[2]]
                curr_instr[i] += 1
            elif row[0] == 'mod':
                register[i][row[1]] %= int(row[2]) if isnumeric(row[2]) else register[i][row[2]]
                curr_instr[i] += 1
            elif row[0] == 'rcv':
                if len(queue[i]) > 0:
                    register[i][row[1]] = queue[i].pop(0)
                    curr_instr[i] += 1
                else:
                    waiting[i] = True
            elif row[0] == 'jgz':
                curr_instr[i] += (int(row[2]) if isnumeric(row[2]) else register[i][row[2]])\
                    if (int(row[1]) if isnumeric(row[1]) else register[i][row[1]]) > 0 else 1
            if not (0 <= curr_instr[i] < len(data)):
                done[i] = True

    result_part2 = count_send_by_1

    extra_out = {'Number of instructions in input': len(data),
                 'Number of instructions executed': (n_instr1, n_instr2),
                 'Number of elements in registries at the end': (len(register[0]), len(register[1]))}

    return result_part1, result_part2, extra_out


if __name__ == "__main__":
    run_day(run_all, [1, 2])
