# -*- coding: utf-8 -*-

import utils


@utils.timeit
def part1(input_f: str):
    data = open(input_f).readlines()

    points = 0
    for line in data:
        nums = line.split(":")[1].split("|")
        win_nums = set(utils.read_ints(nums[0]))
        my_nums = set(utils.read_ints(nums[1]))
        common = win_nums.intersection(my_nums)
        if len(common) > 0:
            points += 2 ** (len(common) - 1)

    return points


@utils.timeit
def part2(input_f: str):
    data = open(input_f).readlines()
    count = [0] * len(data)
    for pos, line in enumerate(data):
        count[pos] += 1
        nums = line.split(":")[1].split("|")
        win_nums = set(utils.read_ints(nums[0]))
        my_nums = set(utils.read_ints(nums[1]))
        common = win_nums.intersection(my_nums)
        for i in range(len(common)):
            # TODO: except index error?
            count[pos + i + 1] += 1 * count[pos]

    return sum(count)


if __name__ == "__main__":
    # test_puzzle
    print("--------------PART-1--------------")
    print("test answer:", part1("test.txt"))
    print("part1 answer:", part1("input.txt"))

    # print("--------------PART-2--------------")
    print("test answer: ", part2("test.txt"))
    print("part2 answer: ", part2("input.txt"))
