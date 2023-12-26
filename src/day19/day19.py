# -*- coding: utf-8 -*-

from collections import defaultdict
import operator
import utils
from dataclasses import dataclass


@dataclass
class Part:
    x: int
    m: int
    a: int
    s: int

    def sum(self):
        return self.x + self.m + self.a + self.s


@dataclass
class PartRange:
    x: range
    m: range
    a: range
    s: range
    state: str


def read_input(input_f: str):
    data = open(input_f).readlines()
    workflows = defaultdict(list)
    parts = []
    for line in data:
        line = line.strip()
        if not line:
            continue
        if line.startswith("{"):
            coords = utils.read_ints(line)
            parts.append(Part(*coords))
        # check if line starts with any lowercase letter
        elif line[0].islower():
            split = line[:-1].split("{")
            steps = split[1].split(",")
            name = split[0]
            for s in steps:
                if ":" in s:
                    condition, out = s.split(":")
                    in_arg = condition[0]
                    op = operator.gt if condition[1] == ">" else operator.lt
                    val = int(condition[2:])
                    workflows[name].append(([in_arg, op, val], out))
                else:
                    workflows[name].append((s,))
    return parts, workflows


@utils.timeit
def part1(input_f: str) -> int:
    parts, workflows = read_input(input_f)

    s = 0
    for p in parts:
        steps = workflows["in"]
        next_step = -1
        while steps:
            for step in steps:
                if len(step) == 1:
                    next_step = step[0]
                    break
                elif len(step) == 2:
                    condition, next_step = step
                    attr, op, val = condition
                    if op(getattr(p, attr), val):
                        break
                else:
                    raise ValueError("Invalid step")
            steps = workflows[next_step]

        if next_step == -1:
            raise ValueError("Invalid workflow")

        if next_step == "A":
            s += p.sum()

    return s


@utils.timeit
def part2(input_f: str):
    _, workflows = read_input(input_f)

    s = 0
    ranges = [PartRange(*[range(1, 4001)]*4, "in")]
    while ranges:
        r = ranges.pop()
        steps = workflows[r.state]
        for step in steps:
            if len(step) == 1:
                next_step = step[0]
                if next_step == "A":
                    s += len(r.x) * len(r.m) * len(r.a) * len(r.s)
                elif next_step == "R":
                    pass
                else:
                    r.state = next_step
                    ranges.append(r)
            elif len(step) == 2:
                condition, next_step = step
                attr, op, val = condition
                r_pass, r_reject = split_range(
                    part_range=r,
                    attr=attr,
                    val=val,
                    op=op,
                    next_state=next_step,
                )
                if r_pass is not None:
                    if r_pass.state == "A":
                        s += len(r_pass.x) * len(r_pass.m) * len(r_pass.a) * len(r_pass.s)
                    else:
                        ranges.append(r_pass)
                if r_reject is not None:
                    r = r_reject
    return s


def split_range(part_range: PartRange, attr: str, val: int, op: operator, next_state: str) -> tuple[PartRange, PartRange]:
    p_range = getattr(part_range, attr)
    # split ranges
    if op == operator.lt:
        r_pass = range(p_range.start, val)  # val not included
        r_reject = range(val, p_range.stop)
    else:
        r_reject = range(p_range.start, val + 1)
        r_pass = range(val + 1, p_range.stop)

    if len(r_pass) > 0:
        part_range_pass = PartRange(*[r_pass if a == attr else getattr(part_range, a) for a in "xmas"], next_state)
    else:
        part_range_pass = None

    if len(r_reject) > 0:
        part_range_reject = PartRange(*[r_reject if a == attr else getattr(part_range, a) for a in "xmas"], part_range.state)
    else:
        part_range_reject = None

    return part_range_pass, part_range_reject


if __name__ == "__main__":
    print("--------------PART-1--------------")
    print("test answer:", part1("test.txt"))
    print("part1 answer:", part1("input.txt"))

    print("--------------PART-2--------------")
    print("test answer: ", part2("test.txt"))
    print("part2 answer: ", part2("input.txt"))
