from __future__ import annotations

import dataclasses
import pathlib
import re
import unittest
import sys

BASE_DIR = pathlib.Path(__file__).parent
CARD_PATTERN = re.compile(r"Card\s+(\d+)")


class Tests(unittest.TestCase):
    def test_example(self):
        input: list[str] = """Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53
Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19
Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1
Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83
Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36
Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11
""".splitlines()
        actual = part1(input)
        expected = [8, 2, 2, 1, 0, 0]
        assert actual == expected


@dataclasses.dataclass
class Card:
    id: int
    winning_numbers: list[int]
    card_numbers: list[int]

    @classmethod
    def from_str(cls, string: str) -> Card:
        left, card_str = tuple(string.split("|", maxsplit=1))
        card_id_str, winning_str = left.split(":", maxsplit=1)
        
        winning_numbers = [int(num) for num in winning_str.split()]
        card_numbers = [int(num) for num in card_str.split()]

        card_id = -1
        card_match = CARD_PATTERN.match(card_id_str)
        if card_match:
            card_id = int(card_match.groups()[0])
        
        return Card(card_id, winning_numbers, card_numbers)

    def get_matching_numbers(self) -> set[int]:
        return set(self.winning_numbers) & set(self.card_numbers)

    def calculate_points(self) -> int:
        matching_numbers = self.get_matching_numbers()
        if not matching_numbers:
            return 0
    
        power = len(matching_numbers) - 1
        points = 2 ** power
        return points


def part1(input: list[str]) -> list[int]:
    cards = [Card.from_str(line) for line in input]
    points = [card.calculate_points() for card in cards]
    return points


if __name__ == "__main__":
    path = pathlib.Path(sys.argv[1])

    input: list[str]
    if path.exists():
        input = path.read_text().splitlines()
    else:
        input = sys.argv[1:]

    solution = part1(input)
    print(sum(solution))
