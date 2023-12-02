# -*- coding: utf-8 -*-

import utils
from collections import Counter


def subroutine(line):
    line = line.split(":")[1]
    rounds = line.split(";")
    for game_round in rounds:
        colors = Counter()
        game_round = game_round.split(",")
        for color in game_round:
            num, color = color.split()
            num = int(num)
            colors[color] += num
            if colors["red"] > 12 or colors["blue"] > 14 or colors["green"] > 13:
                return False
    return True


@utils.timeit
def part1(input_f: str):
    data = open(input_f).readlines()
    ids = 0
    for pos, line in enumerate(data):
        is_possible = subroutine(line)
        if is_possible:
            ids += pos + 1

    return ids


@utils.timeit
def part2(input_f: str):
    data = open(input_f).readlines()
    powers = 0
    for pos, line in enumerate(data):
        line = line.split(":")[1]
        rounds = line.split(";")
        colors = dict(red=1, blue=1, green=1)
        for game_round in rounds:
            game_round = game_round.split(",")
            for color in game_round:
                num, color = color.split()
                num = int(num)
                colors[color] = max(num, colors[color]) if color in colors else num
        powers += colors["red"] * colors["blue"] * colors["green"]

    return powers


if __name__ == "__main__":
    # test_puzzle
    print("--------------PART-1--------------")
    print("test answer:", part1("test.txt"))
    print("part1 answer:", part1("input.txt"))

    print("--------------PART-2--------------")
    print("test asnwer: ", part2("test.txt"))
    print("part2 answer: ", part2("input.txt"))
