from functools import wraps
from time import time


def timing(f):
    @wraps(f)
    def wrap(*args, **kw):
        ts = time()
        result = f(*args, **kw)
        te = time()
        print(f'Runtime for function {f.__name__}: {te-ts:2.4f} sec\n\n')
        return result
    return wrap


def rows_to_chunks(rows, break_str=""):
    inds = [-1] + [i for i in range(len(rows)) if rows[i] == break_str] + [len(rows)]
    return [rows[inds[i] + 1:inds[i + 1]] for i in range(len(inds) - 1)]


def list_set(list_list):
    # Returns a list of set from a list of lists
    return [set(x) for x in list_list]
