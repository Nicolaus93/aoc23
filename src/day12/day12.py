# -*- coding: utf-8 -*-

import utils
from itertools import product
from functools import lru_cache


def is_valid(arr, nums):
    groups = arr.split(".")
    seq_lens = [len(g) for g in groups if g]
    if len(seq_lens) != len(nums):
        return False
    if not all(i == j for i, j in zip(seq_lens, nums)):
        return False

    return True


@utils.timeit
def part1(input_f: str):
    data = open(input_f).readlines()
    s = 0
    for line in data:
        pattern, nums = line.split(" ")
        nums = [int(i) for i in nums.split(",")]
        q_marks = pattern.count("?")
        for p in product(".#", repeat=q_marks):
            arr = ""
            pos = 0
            for i in pattern:
                if i == "?":
                    arr += p[pos]
                    pos += 1
                else:
                    arr += i
            if is_valid("".join(arr), nums):
                s += 1

    return s


@lru_cache(maxsize=None)
def get_valid(pattern, pattern_pos, nums, nums_pos, count):
    if pattern_pos == len(pattern):
        if nums_pos == len(nums):
            # come from '.'
            if count == 0:
                return 1
        elif nums_pos == len(nums) - 1 and count == nums[nums_pos]:
            return 1
        return 0

    if pattern[pattern_pos] == ".":
        # we can either come from '.' or '#'
        if count == 0:
            # if we come from '.', then count is 0
            return get_valid(pattern, pattern_pos + 1, nums, nums_pos, 0)
        else:
            # come from '#'
            if nums_pos >= len(nums) or count != nums[nums_pos]:
                return 0
            else:
                return get_valid(pattern, pattern_pos + 1, nums, nums_pos + 1, 0)
    elif pattern[pattern_pos] == "#":
        return get_valid(pattern, pattern_pos + 1, nums, nums_pos, count + 1)
    elif pattern[pattern_pos] == "?":
        hash_count = get_valid(pattern, pattern_pos + 1, nums, nums_pos, count + 1)
        if count == 0:
            # if we come from '.', then count is 0
            dot_count = get_valid(pattern, pattern_pos + 1, nums, nums_pos, 0)
        else:
            # come from '#'
            if nums_pos >= len(nums) or count != nums[nums_pos]:
                dot_count = 0
            else:
                dot_count = get_valid(pattern, pattern_pos + 1, nums, nums_pos + 1, 0)
        return hash_count + dot_count

    else:
        raise ValueError("invalid pattern")


@utils.timeit
def part2(input_f: str):
    data = open(input_f).readlines()
    s = 0
    for line in data:
        pattern, nums = line.split(" ")
        nums = [int(i) for i in nums.split(",")]
        new_nums = tuple([n for n in nums] * 5)
        new_pattern = "?".join([pattern] * 5)
        ways = get_valid(new_pattern, 0, new_nums, 0, 0)
        # print(ways)
        s += ways

    return s


if __name__ == "__main__":
    # test_puzzle
    print("--------------PART-1--------------")
    print("test answer:", part1("test.txt"))
    print("part1 answer:", part1("input.txt"))

    print("--------------PART-2--------------")
    print("test answer: ", part2("test.txt"))
    print("part2 answer: ", part2("input.txt"))
