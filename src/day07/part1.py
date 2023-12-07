# -*- coding: utf-8 -*-
from collections import Counter

import utils
from dataclasses import dataclass


VALS = ["A", "K", "Q", "J", "T", "9", "8", "7", "6", "5", "4", "3", "2"]
VALS = {v: i for i, v in enumerate(VALS[::-1])}


@dataclass()
class Cards:
    hand: str
    use_joker: bool = False

    def __post_init__(self):
        count = Counter(self.hand)
        if self.use_joker and "J" in count:
            # create a new Cards object where J is replaced with highest count card
            most_common = [i for i in count.most_common() if i[0] != "J"]
            if len(most_common) == 0:
                # all cards are J
                self.score = 7
                return
            # if there are multiple most common cards, choose the one with the highest value
            most_count = most_common[0][1]
            highest_val = sorted([i for i in most_common if i[1] == most_count], key=lambda x: VALS[x[0]])[-1][0]
            self.score = Cards(self.hand.replace("J", highest_val), True).score
            return

        if len(count) == 1:
            # five of a kind
            self.score = 7
        elif len(count) == 2:
            if 4 in count.values():
                # four of a kind
                self.score = 6
            else:
                # full house
                self.score = 5
        elif len(count) == 3:
            if 3 in count.values():
                # three of a kind
                self.score = 4
            else:
                # two pairs
                self.score = 3
        elif len(count) == 4:
            # one pair
            self.score = 2
        else:
            self.score = 1

    def __lt__(self, other):
        if self.score == other.score:
            for i, j in zip(self.hand, other.hand):
                if i != j:
                    if self.use_joker:
                        v1 = -1 if i == "J" else VALS[i]
                        v2 = -1 if j == "J" else VALS[j]
                    else:
                        v1 = VALS[i]
                        v2 = VALS[j]
                    return v1 < v2
        return self.score < other.score


@utils.timeit
def solve(input_f: str, is_part2: bool = False):
    data = open(input_f).readlines()
    hands = []
    for line in data:
        hand, bid = line.split()
        hands.append(tuple((Cards(hand, is_part2), int(bid))))

    hands = sorted(hands, key=lambda x: x[0])
    s = 0
    for pos, hand in enumerate(hands):
        print(hand)
        s += (pos + 1) * hand[1]

    return s


if __name__ == "__main__":
    # test_puzzle
    print("--------------PART-1--------------")
    print("test answer:", solve("test.txt"))
    print("part1 answer:", solve("input.txt"))

    print("--------------PART-2--------------")
    print("test answer: ", solve("test.txt", True))
    print("part2 answer: ", solve("input.txt", True))
