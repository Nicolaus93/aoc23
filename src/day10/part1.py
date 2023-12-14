# -*- coding: utf-8 -*-

import utils
from shapely import Polygon, Point


@utils.timeit
def solve(input_f: str):
    data = open(input_f).readlines()
    world = []
    start = None
    for row, line in enumerate(data):
        world.append([i for i in line.strip()])
        if "S" in line:
            start = row, line.index("S")

    loop = [start, (start[0] + 1, start[1])]  # go down (it works on MY input)
    for _ in range(100000):
        p = loop[-1]
        current = world[p[0]][p[1]]
        if current == "|":
            connected = [(p[0] + 1, p[1]), (p[0] - 1, p[1])]
        elif current == "-":
            connected = [(p[0], p[1] + 1), (p[0], p[1] - 1)]
        elif current == "7":
            connected = [(p[0], p[1] - 1), (p[0] + 1, p[1])]
        elif current == "L":
            connected = [(p[0] - 1, p[1]), (p[0], p[1] + 1)]
        elif current == "J":
            connected = [(p[0], p[1] - 1), (p[0] - 1, p[1])]
        elif current == "F":
            connected = [(p[0] + 1, p[1]), (p[0], p[1] + 1)]
        elif current == "S":
            break
        else:
            raise ValueError("unknown symbol")

        p = connected[0] if connected[0] != loop[-2] else connected[1]
        loop.append(p)

    poly = Polygon(loop)
    bbox = poly.bounds
    in_tiles = 0
    for x in range(int(bbox[0]), int(bbox[2])):
        for y in range(int(bbox[1]), int(bbox[3])):
            if (x, y) in loop:
                continue
            if poly.contains(Point(x, y)):
                in_tiles += 1
    print("part2 answer:", in_tiles)
    return len(loop) // 2


if __name__ == "__main__":
    print("test answer:", solve("test.txt"))
    print("part1 answer:", solve("input.txt"))
