from __future__ import annotations

import itertools
import math
import pathlib
import sys
import typing
import unittest

BASE_DIR = pathlib.Path(__file__).parent

class Tests(unittest.TestCase):
    INPUT = [
        "Time:      7  15   30\n",
        "Distance:  9  40  200",
    ]

    def test_part1(self):
        actual = part1(self.INPUT)
        expected = 288
        assert actual == expected

    def test_part2(self):
        actual = part2(self.INPUT)
        expected = 71_503
        assert actual == expected


def parse(input: list[str]) -> typing.Generator[tuple[int, int], None, None]:
    """Parse the input into pairs of time and distance."""
    times = input[0]
    distances = input[1]
    times = [int(time.strip()) for time in times.split(":")[1].split()]
    distances = [int(dist.strip()) for dist in distances.split(":")[1].split()]
    for time, distance in itertools.zip_longest(times, distances):
        yield (time, distance)


def formula(x: int, y: int) -> int:
    return (x - y) * y


def solve(time: int, distance: int) -> int:
    """Determine the number of ways the distance could be beaten with the given time."""
    count = 0
    i = 0
    for i in range(time):
        res = formula(time, i)
        if res > distance:
            break

    is_even = time % 2 == 0

    half = math.ceil(time / 2)
    count = (half - i) * 2

    if is_even:
        count += 1
             
    return count


def part1(input: list[str]) -> int:
    total_count = 1
    races = list(parse(input))
    for time, distance in races:
        count = solve(time, distance)
        total_count *= count
    return total_count


def part2(input: list[str]) -> int:
    time = ""
    distance = ""
    for t, d in parse(input):
        time += str(t)
        distance += str(d)
    time = int(time)
    distance = int(distance)
    count = solve(time, distance)
    return count


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
    
