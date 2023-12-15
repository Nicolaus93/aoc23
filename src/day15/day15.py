# -*- coding: utf-8 -*-

import contextlib
from collections import defaultdict
import utils


def hash(s):
    res = 0
    for c in s:
        res += ord(c)
        res *= 17
        res %= 256
    return res


@utils.timeit
def part1(input_f: str):
    data = open(input_f).readlines()
    s = 0
    for line in data:
        steps = [i for i in line.strip().split(",")]
        for step in steps:
            s += hash(step)

    return s


@utils.timeit
def part2(input_f: str):
    data = open(input_f).readlines()
    s = 0
    boxes = defaultdict(list)
    for line in data:
        steps = [i for i in line.strip().split(",")]
        for step in steps:
            if "=" in step:
                idx = step.index("=")
                op = "="
                val = int(step[idx + 1:])
            else:
                idx = step.index("-")
                op = '-'
            label = step[:idx]
            box_num = hash(label)
            if op == "=":
                try:
                    labels = [i[0] for i in boxes[box_num]]
                    idx = labels.index(label)
                    boxes[box_num][idx] = (label, val)
                except ValueError:
                    boxes[box_num].append((label, val))
            elif op == "-":
                with contextlib.suppress(ValueError):
                    labels = [i[0] for i in boxes[box_num]]
                    idx = labels.index(label)
                    boxes[box_num].pop(idx)
            else:
                raise ValueError

    for box_num, box in boxes.items():
        for pos, lens in enumerate(box):
            s += (box_num + 1) * (pos + 1) * int(lens[1])

    return s


if __name__ == "__main__":
    print("--------------PART-1--------------")
    print("test answer:", part1("test.txt"))
    print("part1 answer:", part1("input.txt"))

    print("--------------PART-2--------------")
    print("test answer: ", part2("test.txt"))
    print("part2 answer: ", part2("input.txt"))
