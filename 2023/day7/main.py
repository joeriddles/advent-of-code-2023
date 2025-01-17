"""https://en.wikipedia.org/wiki/Levenshtein_distance"""
from __future__ import annotations

import collections
import enum
import itertools
import pathlib
import sys
import unittest

BASE_DIR = pathlib.Path(__file__).parent
DEBUG = True

class Tests(unittest.TestCase):
    INPUT = [
        "32T3K 765\n",
        "T55J5 684\n",
        "KK677 28\n",
        "KTJJT 220\n",
        "QQQJA 483\n",
    ]

    def test_part1(self):
        actual = part1(self.INPUT)
        expected = 6440
        self.assertEqual(actual, expected)

    INPUT_2 = [
        "32T3K 765\n",
        "T55J5 684\n",
        "KK677 28\n",
        "KTJJT 220\n",
        "QQQJA 483\n",
    ]

    def test_part2(self):
        actual = part2(self.INPUT_2)
        expected = 5905
        self.assertEqual(actual, expected)
    
    def test_bet_comparison_high_card(self):
        hand1 = Hand("7K53J")
        hand2 = Hand("T4729")
        self.assertTrue(hand1 < hand2)

    def test_get_type_wildard_five_kind(self):
        hand = Hand("222JJ")
        self.assertEqual(hand.hand_type, HandType.FIVE_KIND)

    def test_get_type_wildard_four_kind(self):
        hand = Hand("222JK")
        self.assertEqual(hand.hand_type, HandType.FOUR_KIND)

    def test_get_type_wildard_three_kind(self):
        hand = Hand("22J45")
        self.assertEqual(hand.hand_type, HandType.THREE_KIND)


class Card:
    RANK = "AKQJT98765432J"[::-1]

    value: str
    rank: int

    def __init__(self, value: str):
        self.value = value
        self.rank = self.RANK.index(value)

    def __str__(self) -> str:
        return self.value

    def __eq__(self, other: Card) -> bool:
        return self.value == other.value

    def __lt__(self, other: Card) -> bool:
        return self.rank < other.rank


print(Card.RANK)


class HandType(enum.IntEnum):
    HIGH_CARD = 1
    ONE_PAIR = 2
    TWO_PAIR = 3
    THREE_KIND = 4
    FULL_HOUSE = 5
    FOUR_KIND = 6
    FIVE_KIND = 7


class Hand:
    cards: list[Card]
    bet: int
    hand_type: HandType

    def __init__(self, card_str: str, bet: int = 0, use_wildcards: bool = False):
        self.cards = []
        self.bet = bet
        for char in card_str:
            card = Card(char)
            self.cards.append(card)
        self.hand_type = self._get_type(use_wildcards)

    def __str__(self) -> str:
        card_str = "".join((str(card) for card in self.cards))
        return f"{card_str} {self.hand_type}"

    def __lt__(self, other: Hand) -> bool:
        if self.hand_type == other.hand_type:
            for self_card, other_card in itertools.zip_longest(self.cards, other.cards):
                if self_card == other_card:
                    continue
                return self_card < other_card
        return self.hand_type < other.hand_type

    def _get_type(self, use_wildcards: bool) -> HandType:
        counts: dict[str, int] = collections.defaultdict(lambda: 0)
        for char in self.cards:
            counts[char.value] += 1

        is_five_of_a_kind = any(_ == 5 for _ in counts.values())
        if is_five_of_a_kind:
            return HandType.FIVE_KIND
        
        is_four_of_a_kind = any(_ == 4 for _ in counts.values())
        if is_four_of_a_kind:
            return HandType.FOUR_KIND
        
        is_three_of_a_kind = any(_ == 3 for _ in counts.values())
        has_pair = any(_ == 2 for _ in counts.values())

        is_full_house = is_three_of_a_kind and has_pair
        if is_full_house:
            return HandType.FULL_HOUSE
        
        if is_three_of_a_kind:
            return HandType.THREE_KIND
        
        has_two_pair = len([_ for _ in counts.values() if _ == 2]) == 2
        if has_two_pair:
            return HandType.TWO_PAIR

        if has_pair:
            return HandType.ONE_PAIR

        return HandType.HIGH_CARD
    

def parse(input: list[str], use_wildcards: bool):
    for line in input:
        card_str, bet = line.split(maxsplit=1)
        bet = int(bet)
        yield Hand(card_str, bet)


def part1(input: list[str]) -> int:
    hands = list(parse(input, use_wildcards=False))
    hands = sorted(hands)
    winnings_count = 0
    for index in range(len(hands), 0, -1):
        hand = hands[index-1]
        if DEBUG:
            print(f"Rank {index}", hand)
        winnings = index * hand.bet
        winnings_count += winnings
    return winnings_count


def part2(input: list[str]) -> int:
    # TODO: refactor this copy-pasta of part1
    hands = list(parse(input, use_wildcards=True))
    hands = sorted(hands)
    winnings_count = 0
    for index in range(len(hands), 0, -1):
        hand = hands[index-1]
        if DEBUG:
            print(f"Rank {index}", hand)
        winnings = index * hand.bet
        winnings_count += winnings
    return winnings_count


if __name__ == "__main__":
    path = pathlib.Path(sys.argv[1])

    input: list[str]
    if path.exists():
        input = path.read_text().splitlines()
    else:
        input = sys.argv[1:]

    solution = part1(input)
    print("Part 1: ", solution)

    solution = part2(input)
    print("Part 2: ", solution)
    
