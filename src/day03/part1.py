# -*- coding: utf-8 -*-

import utils


def solve(matrix_data, is_part2=False):
    res = 0
    n = len(matrix_data)
    m = len(matrix_data[0])
    for i in range(n):
        for j in range(m):
            if matrix_data[i][j] == "." or matrix_data[i][j].isdigit():
                continue
            if is_part2 and matrix_data[i][j] != "*":
                continue
            # we have a symbol, look for all adjacent cells and check if they contain digits
            part_numbers = []

            # right
            num = ""
            col = j + 1
            while col < m and matrix_data[i][col].isdigit():
                num += matrix_data[i][col]
                col += 1
            if num:
                part_numbers.append(int(num))

            # left
            num = ""
            col = j - 1
            while col >= 0 and matrix_data[i][col].isdigit():
                num = matrix_data[i][col] + num
                matrix_data[i][col] = "."  # mark as visited
                col -= 1
            if num:
                part_numbers.append(int(num))

            # up and down
            for row in (-1, 1):
                if i + row < 0 or i + row >= n:
                    continue
                for k in range(-1, 2):
                    num = ""
                    col = j + k
                    if col < 0 or col >= m or not matrix_data[i + row][col].isdigit():
                        continue
                    # check where the number starts
                    start = col
                    while start - 1 >= 0 and matrix_data[i + row][start - 1].isdigit():
                        start -= 1
                    # read the number
                    while start < m and matrix_data[i + row][start].isdigit():
                        num += matrix_data[i + row][start]
                        matrix_data[i + row][start] = "."  # mark as visited
                        start += 1
                    if num:
                        part_numbers.append(int(num))

            if is_part2:
                if len(part_numbers) == 2:
                    res += part_numbers[0] * part_numbers[1]
            else:
                res += sum(part_numbers)
    return res


@utils.timeit
def part1(input_f: str):
    data = open(input_f).readlines()
    processed_data = []
    for row, line in enumerate(data):
        processed_data.append([i for i in line.strip()])
    sum = solve(processed_data)
    return sum


@utils.timeit
def part2(input_f: str):
    data = open(input_f).readlines()
    processed_data = []
    for row, line in enumerate(data):
        processed_data.append([i for i in line.strip()])
    sum = solve(processed_data, is_part2=True)
    return sum


if __name__ == "__main__":
    # test_puzzle
    print("--------------PART-1--------------")
    print("test answer:", part1("test.txt"))
    print("part1 answer:", part1("input.txt"))

    print("--------------PART-2--------------")
    print("test asnwer: ", part2("test.txt"))
    print("part2 answer: ", part2("input.txt"))
