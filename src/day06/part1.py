# -*- coding: utf-8 -*-

import utils
import re


@utils.timeit
def part1(input_f: str):
    data = open(input_f).readlines()
    time = utils.read_ints(data[0])
    distance = utils.read_ints(data[1])
    res = 1
    for t, d in zip(time, distance):
        wins = 0
        for speed in range(1, t):
            remaining_t = t - speed
            if remaining_t * speed > d:
                wins += 1
        print(wins)
        res *= wins

    return res


@utils.timeit
def part2(input_f: str):
    data = open(input_f).readlines()
    t = int("".join(i for i in re.findall("\d+", data[0])))
    d = int("".join(i for i in re.findall("\d+", data[1])))
    wins = 0
    for speed in range(1, t):
        remaining_t = t - speed
        if remaining_t * speed > d:
            wins += 1

    return wins


if __name__ == "__main__":
    # test_puzzle
    print("--------------PART-1--------------")
    print("test answer:", part1("test.txt"))
    print("part1 answer:", part1("input.txt"))

    print("--------------PART-2--------------")
    print("test answer: ", part2("test.txt"))
    print("part2 answer: ", part2("input.txt"))
