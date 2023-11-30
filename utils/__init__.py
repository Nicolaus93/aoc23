# -*- coding: utf-8 -*-

from time import time
import re
from itertools import product


def timeit(func):
    def wrap_func(*args, **kwargs):
        t1 = time()
        result = func(*args, **kwargs)
        print(f"Run in {(time() - t1):.3f}s")
        return result

    return wrap_func


def read_ints(line: str) -> list[int]:
    return [int(i) for i in re.findall("[-]?\d+", line)]


def read_floats(line: str) -> list[float]:
    return [float(i) for i in re.findall("[+-]?([0-9]*[.])?[0-9]+", line)]


def neighbors_2d(x, y, diagonal=True):
    dirs = [(1, 0), (0, 1), (-1, 0), (0, -1)]
    if diagonal:
        diags = [(1, 1), (1, -1), (-1, -1), (-1, 1)]
        dirs.extend(diags)
    for d in dirs:
        yield x + d[0], y + d[1]


def neighbors_3d(x, y, z):
    span = (1, 0, -1)
    for comb in product(span, span, span):
        # if not diagonal and sum(np.abs(comb)) > 2:
        #     continue
        yield x + comb[0], y + comb[1], z + comb[2]


if __name__ == "__main__":
    for i in neighbors_3d(0, 0, 0):
        print(i)
