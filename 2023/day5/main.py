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
56 93 4
""".splitlines()
    
    def test_parse(self):
        almanac = parse("""seeds: 79 14 55 13

seed-to-soil map:
50 98 2
52 50 48
""".splitlines())
        
        self.assertEqual(almanac.seeds, [79, 14, 55, 13])

        map = almanac.find_map("seed")
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
        actual = part2(self.INPUT)
        expected = 46
        self.assertEqual(actual, expected)

MAP_PATTERN = re.compile(r"(\w+)-to-(\w+) map")


@dataclasses.dataclass
class Almanac:
    seeds: list[int]
    maps: dict[str, Map]

    def find_map(self, source: str) -> Map:
        return self.maps[source]
    
    def solve(self, seed: int) -> int:
        logs = []
        dest = "seed"
        
        try:
            while True:
                map = self.find_map(dest)
                seed = map.match(seed)
                dest = map.dest
                if DEBUG:
                    logs.append((dest, seed))
        except KeyError:    
            if DEBUG:
                print(" -> ".join([f"{source} {seed}" for source, seed in logs]))
            pass

        return seed


class FuncMap:
    _data: dict[tuple[int, int], typing.Callable[[int], int]]

    def __init__(self):
        self._data = {}
    
    def set(self, range: tuple[int, int], func: typing.Callable[[int], int]):
        self._data[range] = func

    def get(self, x: int) -> int:
        for start, end in self._data:
            if start <= x < end:
                return self._data[(start, end)](x)
        raise IndexError(x)

@dataclasses.dataclass
class Map:
    source: str
    dest: str
    func_map: FuncMap

    @classmethod
    def empty(cls, source: str, dest: str) -> Map:
        return cls(source, dest, FuncMap())
    
    def match(self, x: int) -> int:
        try:
            return self.func_map.get(x)
        except IndexError:
            return x


def parse(lines: list[str]) -> Almanac:
    almanac = Almanac([], {})

    seeds_str = lines[0]
    almanac.seeds = [int(seed) for seed in seeds_str.split(":")[-1].split()]
    lines = lines[1:]

    map: Map = Map.empty("", "")
    for line in lines:
        if line.strip() == "":
            continue
        
        if match := MAP_PATTERN.match(line):
            source, dest = match.groups()
            map = Map.empty(source, dest)
            almanac.maps[source] = map
            continue

        dest_start, source_start, range_length = tuple([int(num) for num in line.split()])
        func = functools.partial(match_func, dest_start, source_start)

        map.func_map.set(
            (source_start, source_start + range_length),
            func,
        )

    return almanac


def match_func(dest_range_start: int, source_range_start: int, x: int) -> int:
    offset = abs(source_range_start - x)
    res = dest_range_start + offset
    return res


def part1(lines: list[str]) -> list[int]:
    almanac = parse(lines)
    result = [almanac.solve(seed) for seed in almanac.seeds]
    return result


def part2(lines: list[str]) -> int:
    almanac = parse(lines)
    result = None

    for index in range(0, len(almanac.seeds), 2):
        start = almanac.seeds[index]
        length = almanac.seeds[index+1]
        end = start + length
        for seed in range(start, end):
            res = almanac.solve(seed)
            print(seed, res, end="\r")
            if result is None or res < result:
                result = res
    
    return result or -1


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
