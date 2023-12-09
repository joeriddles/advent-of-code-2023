from __future__ import annotations

import dataclasses
import functools
import pathlib
import re
import sys
import unittest
import typing

BASE_DIR = pathlib.Path(__file__).parent
DEBUG = False

class Tests(unittest.TestCase):
    INPUT: list[str] = """seeds: 79 14 55 13

seed-to-soil map:
50 98 2
52 50 48

soil-to-fertilizer map:
0 15 37
37 52 2
39 0 15

fertilizer-to-water map:
49 53 8
0 11 42
42 0 7
57 7 4

water-to-light map:
88 18 7
18 25 70

light-to-temperature map:
45 77 23
81 45 19
68 64 13

temperature-to-humidity map:
0 69 1
1 0 69

humidity-to-location map:
60 56 37
56 93 4""".splitlines()
    
    def test_parse(self):
        almanac = parse("""seeds: 79 14 55 13

seed-to-soil map:
50 98 2
52 50 48""".splitlines())
        
        self.assertEqual(almanac.seeds, [79, 14, 55, 13])

        map = almanac.maps[0]
        self.assertEqual(map.source, "seed")
        self.assertEqual(map.dest, "soil")

        self.assertEqual(map.match(0), 0)

        self.assertEqual(map.match(98), 50)
        self.assertEqual(map.match(99), 51)
        self.assertEqual(map.match(100), 100)

        self.assertEqual(map.match(50), 52)
        self.assertEqual(map.match(51), 53)

    def test_part1(self):
        actual = part1(self.INPUT)
        expected = [82, 43, 86, 35]
        self.assertEqual(actual, expected)

    def test_part2(self):
        ...

MAP_PATTERN = re.compile(r"(\w+)-to-(\w+) map")


@dataclasses.dataclass
class Almanac:
    seeds: list[int]
    maps: list[Map]

    def find_map(self, source: str) -> Map:
        return [_ for _ in self.maps if _.source == source][0]


@dataclasses.dataclass
class Map:
    source: str
    dest: str
    funcs: list[typing.Callable[[int], tuple[bool, int]]]

    @classmethod
    def empty(cls, source: str, dest: str) -> Map:
        return cls(source, dest, [])
    
    def match(self, x: int) -> int:
        for func in self.funcs:
            match, res = func(x)
            if match:
                return res
        return x


def parse(lines: list[str]) -> Almanac:
    almanac = Almanac([], [])

    seeds_str = lines.pop(0)
    almanac.seeds = [int(seed) for seed in seeds_str.split(":")[-1].split()]

    cur_map: Map = Map.empty("", "")
    for line in lines:
        if line.strip() == "":
            continue
        
        if match := MAP_PATTERN.match(line):
            source, dest = match.groups()
            cur_map = Map.empty(source, dest)
            almanac.maps.append(cur_map)
            continue

        dest_range_start, source_range_start, range_length = tuple([int(num) for num in line.split()])
        func = functools.partial(match_func, dest_range_start, source_range_start, range_length)
        cur_map.funcs.append(func)

    return almanac


def match_func(dest_range_start: int, source_range_start: int, range_length: int, x: int) -> tuple[bool, int]:
    """If x is in the source range, calculating the dest mapping value."""
    source_range_end = source_range_start + range_length
    res = -1
    match = source_range_start <= x < source_range_end
    if match:
        offset = abs(source_range_start - x)
        res = dest_range_start + offset
    return match, res


def part1(lines: list[str]) -> list[int]:
    almanac = parse(lines)

    final_dests: list[int] = []

    for seed in almanac.seeds:
        logs = []
        cur = seed
        dest = "seed"
        
        while dest != "location":
            map = almanac.find_map(dest)
            cur = map.match(cur)
            logs.append((dest, cur))
            dest = map.dest
        
        final_dests.append(cur)
        
        if DEBUG:
            print(" -> ".join([f"{source} {seed}" for source, seed in logs]))

    return final_dests


def part2(lines: list[str]) -> int:
    return -1


if __name__ == "__main__":
    path = pathlib.Path(sys.argv[1])

    input: list[str]
    if path.exists():
        input = path.read_text().splitlines()
    else:
        input = sys.argv[1:]

    solution = part1(input)
    print("Part 1: ", min(solution))

    solution = part2(input)
    print("Part 2: ", solution)
