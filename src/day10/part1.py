# -*- coding: utf-8 -*-

import utils
from shapely import Polygon, Point


@utils.timeit
def solve(input_f: str):
    data = open(input_f).readlines()
    world = []
    start = None
    for pos, line in enumerate(data):
        world.append([i for i in line.strip()])
        if "S" in line:
            start = pos, line.index("S")

    loop = [start, (start[0] + 1, start[1])]  # go down
    for _ in range(100000):
        pos = loop[-1]
        
        if world[pos[0]][pos[1]] == "|":
            connected = [(pos[0] + 1, pos[1]), (pos[0] - 1, pos[1])]
        elif world[pos[0]][pos[1]] == "-":
            connected = [(pos[0], pos[1] + 1), (pos[0], pos[1] - 1)]
        elif world[pos[0]][pos[1]] == "7":
            connected = [(pos[0], pos[1] - 1), (pos[0] + 1, pos[1])]
        elif world[pos[0]][pos[1]] == "L":
            connected = [(pos[0] - 1, pos[1]), (pos[0], pos[1] + 1)]
        elif world[pos[0]][pos[1]] == "J":
            connected = [(pos[0], pos[1] - 1), (pos[0] - 1, pos[1])]
        elif world[pos[0]][pos[1]] == "F":
            connected = [(pos[0] + 1, pos[1]), (pos[0], pos[1] + 1)]
        elif world[pos[0]][pos[1]] == "S":
            break
        else:
            raise ValueError("unknown symbol")

        pos = connected[0] if connected[0] != loop[-2] else connected[1]
        loop.append(pos)

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
