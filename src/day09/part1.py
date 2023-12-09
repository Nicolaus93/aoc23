# -*- coding: utf-8 -*-

import utils


@utils.timeit
def solve(input_f: str, is_part2: bool = False):
    data = open(input_f).readlines()
    s = 0
    for line in data:
        nums = utils.read_ints(line)
        diffs = [nums]
        max_it = 200
        for it in range(max_it):
            diff = [j - i for j, i in zip(diffs[-1][1:], diffs[-1])]
            if all(v == 0 for v in diff):
                break
            diffs.append(diff)
        if it == max_it - 1:
            raise ValueError("max iteration reached")

        added = [0]
        for diff in reversed(diffs):
            if is_part2:
                added.append(diff[0] - added[-1])
            else:
                added.append(added[-1] + diff[-1])
        # print(added)
        s += added[-1]

    return s


if __name__ == "__main__":
    # test_puzzle
    print("--------------PART-1--------------")
    print("test answer:", solve("test.txt"))
    print("part1 answer:", solve("input.txt"))

    print("--------------PART-2--------------")
    print("test answer: ", solve("test.txt", is_part2=True))
    print("part2 answer: ", solve("input.txt", is_part2=True))
