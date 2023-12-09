# -*- coding: utf-8 -*-

from itertools import cycle
import utils
import numpy as np


@utils.timeit
def part1(input_f: str):
    data = open(input_f).readlines()
    graph = dict()
    for line in data[2:]:
        graph[line[:3]] = (line[7:10], line[12:15])

    start = "AAA"
    for step, val in enumerate(cycle(data[0].strip())):
        start = graph[start][0] if val == "L" else graph[start][1]
        if start == "ZZZ":
            return step + 1
    return -1


@utils.timeit
def part2(input_f: str):
    data = open(input_f).readlines()
    graph = dict()
    for line in data[2:]:
        graph[line[:3]] = line[7:10], line[12:15]

    starts = [i for i in graph if i[-1] == "A"]
    arrive_at_z = []
    for s in starts:
        for step, val in enumerate(cycle(data[0].strip())):
            s = graph[s][0] if val == "L" else graph[s][1]
            if s[-1] == "Z":
                arrive_at_z.append(step + 1)
                break

    return np.lcm.reduce(arrive_at_z)


if __name__ == "__main__":
    # test_puzzle
    print("--------------PART-1--------------")
    print("test answer:", part1("test1.txt"))
    print("part1 answer:", part1("input.txt"))

    print("--------------PART-2--------------")
    print("test answer: ", part2("test.txt"))
    print("part2 answer: ", part2("input.txt"))
