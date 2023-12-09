# -*- coding: utf-8 -*-

from copy import deepcopy
import utils
from dataclasses import dataclass


@dataclass
class MapRange:
    dest: int
    source: int
    length: int

    @property
    def stop(self):
        return self.source + self.length - 1

    @property
    def shift(self):
        return self.dest - self.source

    def __repr__(self):
        sign = "+" if self.shift > 0 else "-"
        return (
            f"MapRange({self.source}, {self.stop}, f(x) = x {sign} {abs(self.shift)})"
        )


def merge_intervals(ranges: list[range]):
    intervals = sorted(ranges, key=lambda r: r.start)
    merged = [intervals[0]]
    for r_current in intervals[1:]:
        r_previous = merged[-1]
        if r_previous.stop >= r_current.start:
            # merge
            merged[-1] = range(r_previous.start, max(r_previous.stop, r_current.stop))
        else:
            # add new range
            merged.append(r_current)
    return merged


def get_mapping(ranges: list[MapRange], item: int) -> int:
    for r in ranges:
        if r.source <= item <= r.stop:
            return item + r.shift
    return item


@utils.timeit
def part1(input_f: str):
    data = open(input_f).readlines()
    ranges = []
    seeds = utils.read_ints(data[0])
    for line in data[1:]:
        if line[0].isdigit():
            # check if line contains a range
            dest, start, length = utils.read_ints(line)
            ranges.append(MapRange(dest, start, length))
        elif line[0] == "\n":
            # check if line is empty
            pass
        else:
            if not ranges:
                continue
            # compute new seeds
            seeds = [get_mapping(ranges, seed) for seed in seeds]
            ranges = []

    # compute closest location
    return min(get_mapping(ranges, seed) for seed in seeds)


def map_ranges(ranges: list[MapRange], seeds_range: range) -> list[range]:
    ranges = deepcopy(ranges)
    original = [seeds_range]
    mapped = []
    while ranges:
        r = ranges.pop()
        intersect = False
        for s in original:
            intersection = range(max(r.source, s.start), min(r.stop, s.stop))
            if len(intersection) > 0:
                intersect = True
                break

        if intersect:
            # remove s from original intervals
            original.remove(s)

            # compute new ranges
            s1 = s.start
            s2 = s.stop
            r1 = r.source
            r2 = r.stop

            # s1->r1
            if s1 < r1:
                original.append(range(s1, r1 - 1))
                if s2 <= r2:
                    # s1->r1->s2->r2
                    mapped.append(range(r1 + r.shift, s2 + r.shift))
                else:
                    # s1->r1->r2->s2
                    mapped.append(range(r1 + r.shift, r2 + r.shift))
                    original.append(range(r2 + 1, s2))
            else:
                # check if seeds_range is inside r
                if s1 >= r1 and s2 <= r2:
                    # r1->s1->s2->r2
                    mapped.append(range(s1 + r.shift, s2 + r.shift))
                else:
                    # r1->s1->r2->s2
                    mapped.append(range(s1 + r.shift, r2 + r.shift))
                    original.append(
                        range(r2 + 1, s2)
                    )  # TODO: we might overcount here -> merge later

    return mapped + original


@utils.timeit
def part2(input_f: str):
    data = open(input_f).readlines()
    ranges = []
    seeds = utils.read_ints(data[0])
    seed_ranges = []
    for i in range(0, len(seeds), 2):
        seed_ranges.append(range(seeds[i], seeds[i] + seeds[i + 1]))

    for line in data[1:]:
        if line[0].isdigit():
            # check if line contains a range
            ranges.append(MapRange(*utils.read_ints(line)))
        elif line[0] == "\n":
            # check if line is empty
            pass
        elif ranges:
            # compute new ranges
            seed_ranges = [
                s for seed_range in seed_ranges for s in map_ranges(ranges, seed_range)
            ]
            ranges = []

    seed_ranges = [
        s for seed_range in seed_ranges for s in map_ranges(ranges, seed_range)
    ]
    return min(s.start for s in seed_ranges)


if __name__ == "__main__":
    # test_puzzle
    print("--------------PART-1--------------")
    print("test answer:", part1("test.txt"))
    print("part1 answer:", part1("input.txt"))

    print("--------------PART-2--------------")
    print("test answer: ", part2("test.txt"))
    print("part2 answer: ", part2("input2.txt"))
