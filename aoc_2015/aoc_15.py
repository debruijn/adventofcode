from math import prod
from typing import Union
from util.util import ProcessInput, run_day, isnumeric
import z3


def get_score(ingredients, dist):
    # Calculate score for part 1
    return prod(max(sum(dist[j] * ingredients[j][x] for j in range(len(ingredients))), 0)
                for x in range(len(ingredients[0]) - 1))


def find_dist_greedy(ingredients, total=100):
    # Greedy approach: initialize all with 1 (needed due to 0s in input), and then assign the next tablespoon to the
    # one that improves the score the most, until all 100 are assigned.
    curr = [1 for _ in ingredients]
    while sum(curr) < total:
        new = []
        for i in range(len(ingredients)):
            try_dist = curr.copy()
            try_dist[i] += 1
            try_val = get_score(ingredients, try_dist)
            new.append(try_val)
        pick = max(range(len(ingredients)), key=lambda x: new[x])
        curr[pick] += 1

    return get_score(ingredients, curr)


def find_dist_z3(ingredients, total=100):
    opt = z3.Optimize()
    x_vec = [z3.Int(f'x_{i}') for i in range(len(ingredients))]
    [opt.add(x > 0) for x in x_vec]
    opt.add(z3.Sum(x_vec) <= total)
    qualities = []
    for q in range(len(ingredients[0][:-1])):
        this_q = x_vec[0] * ingredients[0][q]  # z3.Int(f'q_{q}')
        for i, r in enumerate(ingredients[1:]):
            this_q += x_vec[i+1] * r[q]
        this_int = z3.Int(f"q_{q}")
        opt.add(this_int == this_q)
        opt.add(this_int > 0)
        qualities.append(this_int)
    total = z3.Int("total")
    opt.add(500 >= sum(ingredients[i][-1] * x_vec[i] for i in range(len(ingredients))))
    opt.add(z3.Product(qualities) == total)
    debug = True
    if debug:
        print(opt)
    opt.maximize(total)
    opt.check()
    model = opt.model()

    if debug:
        for d in model.decls():
            if model[d].as_long() > 0:
                print(f"{d.name()}: {model[d].as_long()}")

    return model[total].as_long()


def find_dist_naive(ingredients, total=100, example_run=True):
    best = 0
    best_500cals = 0
    for i in range(0, total+1):
        if example_run:
            inds = (i, total-i)
            nums = [sum(inds[x] * ingredients[x][y] for x in range(len(inds))) for y in range(len(ingredients[0]))]
            if any(x <= 0 for x in nums):
                continue
            this_score = get_score(ingredients, inds)
            best = this_score if this_score > best else best
            if nums[-1] == 500:
                best_500cals = max(this_score, best_500cals)
            continue
        for j in range(0, total+1 - i):
            for k in range(0, total+1 - i - j):
                inds = (i, j, k, total - i - j - k)
                nums = [sum(inds[x] * ingredients[x][y] for x in range(len(inds))) for y in range(len(ingredients[0]))]
                if any(x <= 0 for x in nums):
                    continue
                this_score = get_score(ingredients, inds)
                best = this_score if this_score > best else best
                if nums[-1] == 500:
                    best_500cals = max(this_score, best_500cals)

    return best, best_500cals

def run_all(example_run: Union[int, bool]):

    data = ProcessInput(example_run=example_run, day=15, year=2015).data
    ingr = [[int(x) for x in row.replace(',','').split() if isnumeric(x)] for row in data]

    # Multiple solutions: using a greedy approach (part 1), using Z3 (part 2), and a direct naive approach for both
    naive = True
    if naive:
        result_part1, result_part2 = find_dist_naive(ingr, 100, example_run)
    else:
        result_part1 = find_dist_greedy(ingr, 100)
        result_part2 = find_dist_z3(ingr, 100)  # Very slow even for the example, so be patient..
        # I think it should be able to go faster, so I might look into that in the future (or not)

    extra_out = {'Number of ingredients in input': len(data),
                 'Number of qualities in input': len(ingr[0])}

    return result_part1, result_part2, extra_out


if __name__ == "__main__":
    run_day(run_all, [1])
