from hashlib import md5
from typing import Union
from util.util import ProcessInput, run_day


def get_hashes(salt, nr_reps):
    # Approach:
    # - Find candidate keys (3-repeats) and add them to running candidate list. For the hashing, use `hashlib.md5()`
    # - Validate these against 1000 future keys (5-repeats), remove candidates if they get too old. Validated keys are
    #   added to `keys`, and their index to `num_keys` which is used to avoid counting the same key twice.
    # - When we have 64 valid keys, in theory we must continue checking current candidates, since the 64th 3-repeat
    #   might have a 5-repeat that happens later than the 65th 3-repeat (in theory). So we keep going until all
    #   candidates are trimmed away.
    # - Then we sort the num_keys (in case the above would happen) and take the 64th (index 63).

    keys = []  # In the end not needed, but during part 1 I didn't know what part 2 would be so I kept track of this
    num_keys = set()  # The integer index of each valid key
    candidate = []  # (num, char, key) -> Candidates (with 3 repeats) are added here to check them against 5 repeats
    nr_enough = 64  # Nr of required keys
    index = 0

    do_trim = False
    stop = False
    enough = False
    while not stop:
        # The md5 hashing, nr_reps times.
        this_cand = salt + str(index)
        for _ in range(nr_reps):
            this_cand = md5(this_cand.encode()).hexdigest()

        # Checking if this_cand contains one of the existing candidate-strings 5 times
        for num, char, key in candidate:
            if num < index - 1000:
                do_trim = True  # Flag that old candidates can be removed
                continue
            if char*5 in this_cand and num not in num_keys:
                num_keys.add(num)  # Used to avoid double-counting this candidate
                keys.append(key)

        # If we don't have 64 yet, add candidates to the candidate list if they have 3 repeated chars (only first)
        if not enough:
            repeated = [x for x in set(this_cand) if x * 3 in this_cand]
            if len(repeated) > 0:  # Only take the first
                candidate.append((index, min(repeated, key=lambda x: this_cand.index(x * 3)), this_cand))

        index += 1

        # Remove old candidates that are more than 1000 away -> quicker checking
        if do_trim:
            candidate = [x for x in candidate if x[0] >= index - 1000]
            do_trim = False

        # If we have enough valid keys, only check existing candidates, no new ones. (Existing candidates could have a
        # lower index but a later "5-check" so we find them later, but they are an earlier key)
        if not enough and len(keys) >= nr_enough:
            enough = True

        # If all candidates are trimmed away, and we have enough keys, we stop
        if len(candidate) == 0 and enough:
            stop = True

    return sorted(num_keys)[nr_enough-1]


def run_all(example_run: Union[int, bool]):

    data = ProcessInput(example_run=example_run, day=14, year=2016).data

    result_part1 = get_hashes(data[0], 1)
    result_part2 = get_hashes(data[0], 2017)

    extra_out = {'Salt in input': data[0]}

    return result_part1, result_part2, extra_out


if __name__ == "__main__":
    run_day(run_all, [1])
