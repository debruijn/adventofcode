from typing import Union
from util.util import ProcessInput, run_day

debug = False


def run_all(example_run: Union[int, bool]):

    if example_run:
        data = ["deal into new stack",
                "cut -2",
                "deal with increment 7",
                "cut 8",
                "cut -4",
                "deal with increment 7",
                "cut 3",
                "deal with increment 9",
                "deal with increment 3",
                "cut -1"]
        N = 10
    else:
        data = ProcessInput(example_run=example_run, day=22, year=2019).data
        N = 10007

    stack = list(range(N))
    for row in data:
        if row == 'deal into new stack':
            stack.reverse()
        elif row.startswith('cut '):
            cut = int(row[4:])
            if debug:
                print("cut: ", cut)
            stack = stack[cut:] + stack[:cut]
        elif row.startswith('deal with increment '):
            incr = int(row[20:])
            if debug:
                print("incr: ", incr)
            index = [x % len(stack) for x in range(0, incr * len(stack), incr)]
            new_stack = stack.copy()
            for i, ind in enumerate(index):
                new_stack[ind] = stack[i]
            stack = new_stack
        else:
            ValueError(row)

    target = 2019 if not example_run else 8

    result_part1 = stack.index(target)  # < 5497, > 2227

    N = 119315717514047 if not example_run else N
    R = 101741582076661

    target_pos = 2020 if not example_run else 6

    # Mathematics of shuffling: card x will be in position (a*x+b) % N for some a,b.
    # - Go through process once to detect a and b
    # - Then use matrix multiplication to find it after R times.
    a = 1
    b = 0

    for row in data:
        if row == 'deal into new stack':
            b = (-b-1) % N
            a = (-a) % N
        elif row.startswith('cut '):
            cut = int(row[4:])
            b = (b - cut) % N
        elif row.startswith('deal with increment '):
            incr = int(row[20:])
            a = (a * incr) % N
            b = (b * incr) % N
        else:
            ValueError(row)

    def matrix_mult(matA, matB):
        # Doing matrix multiplication without numpy :)
        return ((matA[0] * matB[0] + matA[1] * matB[2]) % N,
                (matA[0] * matB[1] + matA[1] * matB[3]) % N,
                (matA[2] * matB[0] + matA[3] * matB[2]) % N,
                (matA[2] * matB[1] + matA[3] * matB[3]) % N)

    def matrix_power(mat, exp):
        # Matrix power: mat to the power exp.
        # Keep dividing exp by 2, and round down. If it was odd before, do an additional multiplication.
        # So X^13 = X * (X^6)^2 = X * X^6 * X^6 = X * (X^3)^2 * (X^3)^2 = ...
        ans = (1, 0, 0, 1)
        while exp > 0:
            if exp % 2 == 1:
                ans = matrix_mult(mat, ans)
            exp = int(exp/2)
            mat = matrix_mult(mat, mat)
        return ans

    a, b, _ ,_ =  matrix_power((a, b, 0, 1), R)
    result_part2 = (pow(a, -1, N) * (target_pos - b)) % N

    extra_out = {'Number of actions in input': len(data)}

    return result_part1, result_part2, extra_out


if __name__ == "__main__":
    run_day(run_all, [1])
