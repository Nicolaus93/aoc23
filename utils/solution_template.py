# -*- coding: utf-8 -*-

import utils
from dataclasses import dataclass


@dataclass
class PlaceHolder:
    hello: str
    world: str


@utils.timeit
def part1(input_f: str):
    data = open(input_f).readlines()
    processed_data = []
    for line in data:
        processed_data.append([i for i in line.split()])

    return -1


@utils.timeit
def part2(input_f: str):
    data = open(input_f).readlines()
    processed_data = []
    for line in data:
        processed_data.append([i for i in line.split()])

    return -1


if __name__ == "__main__":
    print("--------------PART-1--------------")
    print("test answer:", part1("test.txt"))
    print("part1 answer:", part1("input.txt"))

    print("--------------PART-2--------------")
    print("test answer: ", part2("test.txt"))
    print("part2 answer: ", part2("input.txt"))
