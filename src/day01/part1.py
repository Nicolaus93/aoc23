# -*- coding: utf-8 -*-

import utils


def part1(line):
    str_num = ""
    for char in line:
        # check if char is number:
        if char.isdigit():
            str_num += char
    return str_num[0], str_num[-1]


def part2(line):

    convert = {
        "one": "1",
        "two": "2",
        "three": "3",
        "four": "4",
        "five": "5",
        "six": "6",
        "seven": "7",
        "eight": "8",
        "nine": "9"
    }

    str_num = []
    # check if line contains "one" or "two"
    for pos, char in enumerate(line):
        # check if char is number:
        if char.isdigit():
            str_num.append(char)
        else:
            # check if next chars are letters and form a word which is in
            # ("one", "two", "three", "four", "five", "six", "seven", "eight", "nine")
            for num in convert.keys():
                if line[pos:].startswith(num):
                    str_num.append(convert[num])
                    break

    # get first and last number
    first = convert[str_num[0]] if str_num[0].isalpha() else str_num[0]
    last = convert[str_num[-1]] if str_num[-1].isalpha() else str_num[-1]
    return first, last


@utils.timeit
def solve(input_f: str, is_part2: bool):
    data = open(input_f).readlines()
    all_sum = 0
    f = part2 if is_part2 else part1
    for pos, line in enumerate(data):
        first, last = f(line)
        all_sum += int(first + last)

    return all_sum


if __name__ == "__main__":

    print("--------------PART-1--------------")
    print(f"part 1: ", solve("test.txt", False))

    print("--------------PART-2--------------")
    print(f"part 2: ", solve("test.txt", True))
