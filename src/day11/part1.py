# -*- coding: utf-8 -*-

import utils
import numpy as np
from scipy.spatial.distance import pdist


@utils.timeit
def part1(input_f: str):
    data = open(input_f).readlines()
    processed_data = []
    for line in data:
        processed_data.append([1 if i == "#" else 0 for i in line.strip()])

    arr = np.array(processed_data)
    # find which rows are all 0s
    rows = np.where(~arr.any(axis=1))[0]
    # find which columns are all 0s
    cols = np.where(~arr.any(axis=0))[0]

    # insert new rows and columns based on zero rows and columns
    new_arr = np.insert(arr, rows, 0, axis=0)
    new_arr = np.insert(new_arr, cols, 0, axis=1)
    idxs = np.where(new_arr)
    # compute all pairwise distances
    pts = np.vstack(idxs).T
    dists = pdist(pts, metric="cityblock")
    return int(dists.sum())


@utils.timeit
def part2(input_f: str):
    data = open(input_f).readlines()
    processed_data = []
    for line in data:
        processed_data.append([1 if i == "#" else 0 for i in line.strip()])

    arr = np.array(processed_data)
    # find which rows are all 0s
    rows = np.where(~arr.any(axis=1))[0]
    # find which columns are all 0s
    cols = np.where(~arr.any(axis=0))[0]

    offset = 1000000 - 1
    pts = np.vstack(np.where(arr)).T
    for pnt in pts:
        if pnt[0] > rows[-1]:
            pnt[0] += offset * len(rows)
        else:
            for pos, value in enumerate(rows):
                if pnt[0] < value:
                    break
            pnt[0] += pos * offset

        if pnt[1] > cols[-1]:
            pnt[1] += offset * len(cols)
        else:
            for pos, value in enumerate(cols):
                if pnt[1] < value:
                    break
            pnt[1] += pos * offset

    # compute all pairwise distances
    dists = pdist(pts, metric="cityblock")
    return int(dists.sum())


if __name__ == "__main__":
    # test_puzzle
    print("--------------PART-1--------------")
    print("test answer:", part1("test.txt"))
    print("part1 answer:", part1("input.txt"))

    print("--------------PART-2--------------")
    print("test answer: ", part2("test.txt"))
    print("part2 answer: ", part2("input.txt"))
