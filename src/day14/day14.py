# -*- coding: utf-8 -*-

import utils


def move_north(rocks):
    n = len(rocks)
    m = len(rocks[0])

    for i in range(n):
        for j in range(m):
            if rocks[i][j] == "O":
                north(i, j, rocks)


def north(i, j, rocks):
    if i == 0:
        return

    hit = False
    for y in reversed(range(i)):
        if rocks[y][j] in ("#", "O"):
            hit = True
            break

    rocks[i][j] = "."
    if not hit:
        rocks[y][j] = "O"
    else:
        rocks[y + 1][j] = "O"
    return


def move_south(rocks):
    n = len(rocks)
    m = len(rocks[0])

    # for south we have to start from the bottom and go up
    for i in reversed(range(n)):
        for j in range(m):
            if rocks[i][j] == "O":
                south(i, j, rocks)


def south(i, j, rocks):
    if i == len(rocks) - 1:
        return

    hit = False
    for y in range(i + 1, len(rocks)):
        if rocks[y][j] in ("#", "O"):
            hit = True
            break

    rocks[i][j] = "."
    if not hit:
        rocks[y][j] = "O"
    else:
        rocks[y - 1][j] = "O"
    return


def move_east(rocks):
    n = len(rocks)
    m = len(rocks[0])

    for i in range(n):
        for j in reversed(range(m)):
            if rocks[i][j] == "O":
                east(i, j, rocks)


def east(i, j, rocks):
    if j == len(rocks[0]) - 1:
        return

    hit = False
    for x in range(j + 1, len(rocks[0])):
        if rocks[i][x] in ("#", "O"):
            hit = True
            break

    rocks[i][j] = "."
    if not hit:
        rocks[i][x] = "O"
    else:
        rocks[i][x - 1] = "O"
    return


def move_west(rocks):
    n = len(rocks)
    m = len(rocks[0])

    for i in range(n):
        for j in range(m):
            if rocks[i][j] == "O":
                west(i, j, rocks)


def west(i, j, rocks):
    if j == 0:
        return

    hit = False
    for x in reversed(range(j)):
        if rocks[i][x] in ("#", "O"):
            hit = True
            break

    rocks[i][j] = "."
    if not hit:
        rocks[i][x] = "O"
    else:
        rocks[i][x + 1] = "O"
    return


def get_load(rocks):
    rows = len(rocks)
    load = 0
    for i, row in enumerate(rocks):
        for j, val in enumerate(row):
            if val == "O":
                load += rows - i
    return load


@utils.timeit
def part1(input_f: str):
    data = open(input_f).readlines()
    rocks = []
    for line in data:
        rocks.append([i for i in line.strip()])

    move_north(rocks)
    return get_load(rocks)


def cycle(rocks):
    move_north(rocks)
    move_west(rocks)
    move_south(rocks)
    move_east(rocks)


@utils.timeit
def part2(input_f: str):
    data = open(input_f).readlines()
    rocks = []
    for line in data:
        rocks.append([i for i in line.strip()])

    visited = []
    cycles = 1000000000
    c = 0
    found = False
    while c < cycles:
        hashed = "".join("".join(r) for r in rocks)
        if hashed in visited and not found:
            cycle_len = c - visited.index(hashed)
            c = cycles - (cycles - c) % cycle_len
            found = True
            continue

        visited.append(hashed)
        cycle(rocks)
        c += 1

    return get_load(rocks)


if __name__ == "__main__":
    print("--------------PART-1--------------")
    print("test answer:", part1("test.txt"))
    print("part1 answer:", part1("input.txt"))

    print("--------------PART-2--------------")
    print("test answer:", part2("test.txt"))
    print("part2 answer:", part2("input.txt"))
