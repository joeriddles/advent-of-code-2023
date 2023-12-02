"""Not a super efficient solution, it requires two regular expressions per line.

A more elegant way may be using a trie-based structure...
"""
from __future__ import annotations

import pathlib
import re
import sys
import unittest

class Tests(unittest.TestCase):
    def test_example(self):
        input: list[str] = """two1nine
eightwothree
abcone2threexyz
xtwone3four
4nineeightseven2
zoneight234
7pqrstsixteen""".splitlines()
        actual = main(input)
        expected = [29, 83, 13, 24, 42, 14, 76]
        assert actual == expected
        assert sum(actual) == 281
    
    def test_file(self):
        input = path.read_text().splitlines()
        actual = sum(main(input))
        assert actual == 54_100
    
    def test_empty(self):
        assert main([]) == []


NUMBERS_DICT = {
    "one": 1,
    "two": 2,
    "three": 3,
    "four": 4,
    "five": 5,
    "six": 6,
    "seven": 7,
    "eight": 8,
    "nine": 9
}
NUMBERS = list(NUMBERS_DICT.keys())
NUMBERS_PATTERN = "|".join(NUMBERS + [r"\d"])
START_PATTERN = re.compile(rf"({NUMBERS_PATTERN})")
END_PATTERN = re.compile(rf"(?s:.*)({NUMBERS_PATTERN})")
"""See https://stackoverflow.com/a/33233868"""


def main(input: list[str]) -> list[int]:
    solution: list[int] = []
    
    for line in input:

        m = START_PATTERN.search(line)
        if m is None:
            raise ValueError(line, START_PATTERN.pattern)
        start = m.groups()[0]

        m = END_PATTERN.match(line) # note the use of `match` here instead of `search`
        if m is None:
            raise ValueError(line, END_PATTERN.pattern)
        end = m.groups()[0]

        start = NUMBERS_DICT.get(start, None) or int(start)
        end = NUMBERS_DICT.get(end, None) or int(end)
        value = int(str(start) + str(end))
        solution.append(value)

    return solution


if __name__ == "__main__":
    path = pathlib.Path(sys.argv[1])

    input: list[str]
    if path.exists():
        input = path.read_text().splitlines()
    else:
        input = sys.argv[1:]

    solution = main(input)
    print(sum(solution))
