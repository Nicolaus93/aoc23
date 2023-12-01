# -*- coding: utf-8 -*-

import utils
from dataclasses import dataclass
from pprint import pprint as pp


@dataclass
class PlaceHolder:
    hello: str
    world: str


@utils.timeit
def solve(input_f: str):
    data = open(input_f).readlines()
    processed_data = []
    for line in data:
        processed_data.append([i for i in line.split()])

    pp(processed_data)
    return -1


if __name__ == "__main__":
    # test_puzzle
    print("--------------TEST--------------")
    res = solve("test.txt")
    print("test answer: ", res)

    # real puzzle
    print("--------------PUZZLE--------------")
    res = solve()
    print("puzzle answer", res)
