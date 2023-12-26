# -*- coding: utf-8 -*-

from __future__ import annotations
from collections import OrderedDict
import utils
from dataclasses import dataclass


LEFT = (0, -1)
RIGHT = (0, 1)
UP = (-1, 0)
DOWN = (1, 0)


def add(p1: tuple[int, int], p2: tuple[int, int]) -> tuple[int, int]:
    return p1[0] + p2[0], p1[1] + p2[1]


@dataclass(frozen=True)
class Beam:
    pos: tuple[int, int]
    dir: tuple[int, int]

    def __post_init__(self):
        if abs(self.dir[0]) + abs(self.dir[1]) != 1:
            raise ValueError("Wrong direction!")

    def update(self, tile) -> list[Beam]:
        pos = self.pos
        dir = self.dir
        if tile == "-":
            if dir in (LEFT, RIGHT):
                return [Beam(add(pos, dir), dir)]
            else:
                return [Beam(add(pos, LEFT), LEFT), Beam(add(pos, RIGHT), RIGHT)]
        elif tile == '|':
            if dir in (UP, DOWN):
                return [Beam(add(pos, dir), dir)]
            else:
                return [Beam(add(pos, DOWN), DOWN), Beam(add(pos, UP), UP)]
        elif tile == '/':
            if dir == DOWN:
                d = LEFT
            elif dir == RIGHT:
                d = UP
            elif dir == UP:
                d = RIGHT
            elif dir == LEFT:
                d = DOWN
            else:
                raise ValueError("AAA")
            return [Beam(add(pos, d), d)]
        elif tile == '\\':
            if dir == DOWN:
                d = RIGHT
            elif dir == RIGHT:
                d = DOWN
            elif dir == UP:
                d = LEFT
            elif dir == LEFT:
                d = UP
            else:
                raise ValueError("BBB")
            return [Beam(add(pos, d), d)]
        elif tile == ".":
            return [Beam(add(pos, dir), dir)]
        else:
            raise ValueError("Wrong tile!")


def get_visited(visited, n, m) -> str:
    visited_pos = {i.pos for i in visited}
    world_str = ""
    for i in range(n):
        for j in range(m):
            if (i, j) not in visited_pos:
                world_str += "."
            else:
                world_str += "#"
        world_str += "\n"
    return world_str


def get_score(pos_dir_scores: dict[Beam, int]) -> int:
    score = 0
    visited = {b.pos for b in pos_dir_scores}
    for key in pos_dir_scores:
        if key.pos in visited:
            score += 1
            visited.remove(key.pos)
        pos_dir_scores[key] = score
    return score


def good_cache(start, world, pos_dir_scores):
    beams = [start]
    pos_dir_scores[start] = 0
    while beams:
        beam = beams.pop()
        tile = world[beam.pos[0]][beam.pos[1]]
        new_beams = beam.update(tile)
        for b in new_beams:
            if b.pos[0] >= len(world) or b.pos[1] >= len(world[0]) or b.pos[0] < 0 or b.pos[1] < 0:
                continue
            if b not in pos_dir_scores:
                pos_dir_scores[b] = 0
                beams.append(b)
            elif pos_dir_scores[b] > 0:
                score_until_now = get_score(pos_dir_scores)
                # TODO: exclude b?
                # TODO: update dict
                print("CACHE")
                return score_until_now + pos_dir_scores[b]

    return pos_dir_scores


def solve(beams: list[Beam], world: list[list[str]]) -> int:
    pos_dir_visited = {beams[0]}
    while beams:
        beam = beams.pop()
        tile = world[beam.pos[0]][beam.pos[1]]
        new_beams = beam.update(tile)
        for b in new_beams:
            if b.pos[0] >= len(world) or b.pos[1] >= len(world[0]) or b.pos[0] < 0 or b.pos[1] < 0:
                continue
            if b not in pos_dir_visited:
                pos_dir_visited.add(b)
                beams.append(b)
    res = get_visited(pos_dir_visited, len(world), len(world[0]))
    return res.count("#")


@utils.timeit
def part1(input_f: str):
    data = open(input_f).readlines()
    world = []
    for line in data:
        world.append([i for i in line.strip()])

    # beams = [Beam((0, 0), RIGHT)]
    # return solve(beams, world)
    scores = good_cache(Beam((0, 0), RIGHT), world, OrderedDict())
    return get_score(scores)


@utils.timeit
def part2(input_f: str):
    data = open(input_f).readlines()
    world = []
    for line in data:
        world.append([i for i in line.strip()])

    max_config = 0
    rows, cols = len(world), len(world[0])
    start_up = [Beam((0, i), DOWN) for i in range(cols)]
    start_down = [Beam((rows - 1, i), UP) for i in range(cols)]
    start_left = [Beam((i, 0), RIGHT) for i in range(rows)]
    start_right = [Beam((i, cols - 1), LEFT) for i in range(rows)]
    starting_pos = start_right + start_up + start_left + start_down
    for start in starting_pos:
        beams = [start]
        score = solve(beams, world)
        max_config = max(max_config, score)
    return max_config


@utils.timeit
def part3(input_f: str):
    data = open(input_f).readlines()
    world = []
    for line in data:
        world.append([i for i in line.strip()])

    max_config = 0
    rows, cols = len(world), len(world[0])
    start_up = [Beam((0, i), DOWN) for i in range(cols)]
    start_down = [Beam((rows - 1, i), UP) for i in range(cols)]
    start_left = [Beam((i, 0), RIGHT) for i in range(rows)]
    start_right = [Beam((i, cols - 1), LEFT) for i in range(rows)]
    starting_pos = start_right + start_up + start_left + start_down
    scores = OrderedDict()
    for start in starting_pos:
        new_scores = good_cache(start, world, scores)
        scores |= new_scores
    return max_config


if __name__ == "__main__":
    print("--------------PART-1--------------")
    print("test answer:", part1("test.txt"))
    print("part1 answer:", part1("input.txt"))

    # print("--------------PART-2--------------")
    print("test answer: ", part3("test.txt"))
    print("part2 answer: ", part2("input.txt"))
