from typing import Union
from util.util import ProcessInput, run_day
from collections import defaultdict

debug = False


def get_reqs(data, first_ind=5, second_ind=36):
    requirements = defaultdict(list)
    for row in data:
        first, second = row[first_ind], row[second_ind]  # Note: this can be swapped around and it still works (diff answer)
        requirements[second].append(first)
        if first not in requirements:  # Add to make sure steps that are immediately ready to go are included.
            requirements[first] = []
    return requirements


def run_all(example_run: Union[int, bool]):

    data = ProcessInput(example_run=example_run, day=7, year=2018).data

    # Part 1: take alpha-first that is ready, remove it from requirements; repeat
    requirements = get_reqs(data)
    order = ""
    nr_steps = len(requirements)
    while len(requirements) > 0:
        ready = [k for k, v in requirements.items() if len(v) == 0]
        take = sorted(ready)[0]  # Alphabetically first that is ready-to-go

        for k, v in requirements.items():
            if take in v:
                v.remove(take)
        del requirements[take]

        order += take

    result_part1 = order

    # Part 2:
    # - assign to available workers alpha-first tasks
    # - find next completed task; update other tasks and add worker to available workers


    requirements = get_reqs(data)
    n_workers = 2 if example_run else 5
    step_time = 0 if example_run else 60
    available_workers = [*range(n_workers)]
    current_tasks = {}  # worker: (task, time_left)
    time_taken = 0
    order = ""
    while len(requirements) > 0:
        ready = [k for k, v in requirements.items() if len(v) == 0]
        for worker in available_workers.copy():
            if len(ready) > 0:
                next_task = sorted(ready)[0]
                current_tasks[worker] = (next_task, step_time + ord(next_task) - ord('A') + 1)
                ready.remove(next_task)
                available_workers.remove(worker)
                del requirements[next_task]

        next_finished_worker = min(current_tasks, key=lambda x: current_tasks[x][1])
        next_finished_task, task_time = current_tasks[next_finished_worker]
        time_taken += task_time
        for k, v in requirements.items():
            if next_finished_task in v:
                v.remove(next_finished_task)
        del current_tasks[next_finished_worker]
        for other_worker in current_tasks:
            current_tasks[other_worker] = (current_tasks[other_worker][0], current_tasks[other_worker][1] - task_time)
        available_workers.append(next_finished_worker)

        if debug:
            order += next_finished_task
            print(f"{order} after {time_taken}s, with {available_workers} available and ongoing tasks: {current_tasks}")

    result_part2 = time_taken

    extra_out = {'Number of relations in input': len(data),
                 'Number of steps in input': nr_steps}

    return result_part1, result_part2, extra_out


if __name__ == "__main__":
    run_day(run_all, [1])
