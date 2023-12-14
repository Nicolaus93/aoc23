# -*- coding: utf-8 -*-

import utils
import numpy as np
from copy import deepcopy


def is_reflected(pattern):

    for i in range(1, len(pattern) // 2 + 1):
        if np.array_equal(pattern[:i], np.flipud(pattern[i : 2 * i])):
            return i
        if np.array_equal(pattern[-i:], np.flipud(pattern[-2 * i : -i])):
            return len(pattern) - i

    return 0


@utils.timeit
def part1(input_f: str):
    data = open(input_f).readlines()
    pattern = []
    s = 0
    for pos, line in enumerate(data):
        if len(line) > 1:
            pattern.append([1 if i == "#" else 0 for i in line.strip()])
        else:
            arr = np.array(pattern)
            pattern = []
            rows = is_reflected(arr)
            if rows > 0:
                s += rows * 100
                continue
            cols = is_reflected(arr.T)
            if cols > 0:
                s += cols
                continue
    return s


def all_reflected(pattern):
    scores = set()
    for i in range(1, len(pattern) // 2 + 1):
        if np.array_equal(pattern[:i], np.flipud(pattern[i : 2 * i])):
            scores.add(i)
        if np.array_equal(pattern[-i:], np.flipud(pattern[-2 * i : -i])):
            scores.add(len(pattern) - i)

    return scores


def smudge(pattern):
    n, m = pattern.shape
    for i in range(n):
        for j in range(m):
            arr = deepcopy(pattern)
            # 0 to 1 and 1 to 0
            arr[i, j] = 1 - arr[i, j]
            yield arr, i, j


@utils.timeit
def part2(input_f: str):
    data = open(input_f).readlines()
    pattern = []
    s = 0
    for pos, line in enumerate(data):
        if len(line) > 1:
            pattern.append([1 if i == "#" else 0 for i in line.strip()])
        else:
            arr = np.array(pattern)
            pattern = []
            for swap, i, j in smudge(arr):
                old_score = is_reflected(arr)
                rows = all_reflected(swap) - {old_score}
                if rows:
                    if len(rows) > 1:
                        raise ValueError(f"more than one duplicate {rows}")
                    s += rows.pop() * 100
                    break

                old_score = is_reflected(arr.T)
                cols = all_reflected(swap.T) - {old_score}
                if cols:
                    if len(cols) > 1:
                        raise ValueError(f"more than one duplicate {cols}")
                    s += cols.pop()
                    break

    return s


if __name__ == "__main__":
    # test_puzzle
    print("--------------PART-1--------------")
    print("test answer:", part1("test2.txt"))
    print("part1 answer:", part1("input.txt"))

    print("--------------PART-2--------------")
    print("test answer: ", part2("test.txt"))
    print("part2 answer: ", part2("input.txt"))
