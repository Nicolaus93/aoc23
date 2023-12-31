# -*- coding: utf-8 -*-

from scipy import ndimage
import numpy as np
import utils
from tqdm import tqdm
from shapely import Polygon


def get_world(loop):
    min_x = min(loop, key=lambda x: x[1])[1]
    max_x = max(loop, key=lambda x: x[1])[1]
    min_y = min(loop, key=lambda x: x[0])[0]
    max_y = max(loop, key=lambda x: x[0])[0]
    a = np.zeros(shape=(max_y - min_y + 1, max_x - min_x + 1), dtype=bool)
    idxs = np.array(loop) - np.array([min_y, min_x])
    a[idxs[:, 0], idxs[:, 1]] = True
    return a


@utils.timeit
def part1(input_f: str):
    data = open(input_f).readlines()
    path = []
    for line in data:
        path.append([i for i in line.split()])

    loop = [(0, 0)]
    for p in path:
        dir = p[0]
        dist = int(p[1])
        if dir == "R":
            loop.extend([(loop[-1][0], loop[-1][1] + i) for i in range(1, dist + 1)])
        elif dir == "L":
            loop.extend([(loop[-1][0], loop[-1][1] - i) for i in range(1, dist + 1)])
        elif dir == "U":
            loop.extend([(loop[-1][0] - i, loop[-1][1]) for i in range(1, dist + 1)])
        elif dir == "D":
            loop.extend([(loop[-1][0] + i, loop[-1][1]) for i in range(1, dist + 1)])
        else:
            raise ValueError("Unknown direction")

    rows = [i[0] for i in loop]
    min_y = min(rows)
    cols = [i[1] for i in loop]
    min_x = min(cols)
    rows = [i - min_y for i in rows]
    cols = [i - min_x for i in cols]

    loop = [(i + min_y, j + min_x) for i, j in zip(rows, cols)]
    world = get_world(loop)

    b = ndimage.binary_fill_holes(world)
    return len(b.nonzero()[0])


@utils.timeit
def part2(input_f: str):
    data = open(input_f).readlines()
    path = []
    directions = {
        "0": "R",
        "1": "D",
        "2": "L",
        "3": "U",
    }
    for line in data:
        hex_code = line.split()[-1]
        hex_code = hex_code[1:-1]
        path.append([directions[hex_code[-1]], int(hex_code[1:6], 16)])

    x = y = 0
    pts = [(x, y)]
    for p in tqdm(path):
        d = p[0]
        dist = int(p[1])
        if d == "R":
            x += dist
        elif d == "L":
            x -= dist
        elif d == "U":
            y -= dist
        elif d == "D":
            y += dist
        else:
            raise ValueError("Unknown direction")
        pts.append((x, y))

    assert x == y == 0
    poly = Polygon(pts)
    p2 = poly.buffer(0.5, join_style=2)
    return int(p2.area)


if __name__ == "__main__":
    print("--------------PART-1--------------")
    print("test answer:", part1("test.txt"))
    print("part1 answer:", part1("input.txt"))

    print("--------------PART-2--------------")
    print("test answer: ", part2("test.txt"))
    print("part2 answer: ", part2("input.txt"))
