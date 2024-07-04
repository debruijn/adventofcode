from typing import Union
from util.util import ProcessInput, run_day

use_strings = False
accelerate_loop = True
k = 4  # For use in acceleration
# Three implementations based on the above: encode recipe in string [use_strings:True] or in list of ints [False];
#   if [False] and [accelerate_loop:True] then skip string construction for proportion of iterations.
# - I first did the [False/False] implementation, which is faster than [True]
# - I wondered if avoiding the string-join step would be worth it to then having to convert strings to ints (it is not)
# - The fastest is the [False/True] implementation, with k=4. This does the string construction after R new iterations
#   have been done with R equal to 1/4th of the length of the recipe for the previous strict construction.
# - Of course, [True/True] could also be implemented but I expect that to be slower than [False/True] like [True/False]
#   is compared to [False/False]


def run_all(example_run: Union[int, bool]):

    data = ProcessInput(example_run=example_run, day=14, year=2018).as_int().data

    nr_skip = str(data[0]) if use_strings else data[0]
    nr_take = 10
    recipe = "37" if use_strings else [3, 7]
    locs = [0, 1]

    if use_strings:  # Second implementation
        while len(recipe) < int(nr_skip) + nr_take or nr_skip not in recipe:
            new = str(int(recipe[locs[0]]) + int(recipe[locs[1]]))
            recipe += new
            locs = [(locs[0] + 1 + int(recipe[locs[0]])) % len(recipe),
                    (locs[1] + 1 + int(recipe[locs[1]])) % len(recipe)]

        result_part1 = recipe[int(nr_skip):int(nr_skip) + nr_take]
        result_part2 = recipe.index(nr_skip)
    else:
        if accelerate_loop:  # Third implementation
            while (len(recipe) < nr_skip + nr_take or
                   str(nr_skip) not in "".join(str(x) for x in recipe[-7 - int(len(recipe)/k):])):
                for _ in range(1+int(len(recipe)/k)):
                    new = [int(x) for x in str(recipe[locs[0]] + recipe[locs[1]])]
                    recipe.extend(new)
                    locs = [(locs[0] + 1 + recipe[locs[0]]) % len(recipe), (locs[1] + 1 + recipe[locs[1]]) % len(recipe)]
        else:  # First implementation
            while len(recipe) < nr_skip + nr_take or str(nr_skip) not in "".join(str(x) for x in recipe[-7:]):
                new = [int(x) for x in str(recipe[locs[0]] + recipe[locs[1]])]
                recipe.extend(new)
                locs = [(locs[0] + 1 + recipe[locs[0]]) % len(recipe), (locs[1] + 1 + recipe[locs[1]]) % len(recipe)]

        result_part1 = "".join(str(x) for x in recipe[nr_skip:nr_skip+nr_take])
        result_part2 = "".join(str(x) for x in recipe).index(str(nr_skip))

    extra_out = {'Number of digits to skip': nr_skip,
                 'Final length of recipe': len(recipe)}

    return result_part1, result_part2, extra_out


if __name__ == "__main__":
    run_day(run_all, [1, 2, 3, 4])
