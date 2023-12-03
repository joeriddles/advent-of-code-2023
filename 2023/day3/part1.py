from __future__ import annotations

import dataclasses
import pathlib
import re
import unittest
import sys

BASE_DIR = pathlib.Path(__file__).parent
DEBUG = False

class Tests(unittest.TestCase):

    def test_one_part_number(self):
        input = ["1#"]
        actual = main(input)
        self.assertEqual(actual, [1])

    def test_two_part_numbers(self):
        input = ["1#.2#"]
        actual = main(input)
        self.assertEqual(actual, [1, 2])
    
    def test_one_part_diagonal(self):
        input = [
            "1.",
            ".#"
        ]
        actual = main(input)
        self.assertEqual(actual, [1])

    def test_example(self):
        input = [
            "467..114..",
            "...*......",
            "..35..633.",
            "......#...",
            "617*......",
            ".....+.58.",
            "..592.....",
            "......755.",
            "...$.*....",
            ".664.598..",
        ]
        actual = main(input)
        
        expected = [467, 35, 633, 617, 592, 755, 664, 598]
        self.assertEqual(actual, expected)
        
        expected_sum = 4_361
        self.assertEqual(sum(actual), expected_sum)
    
    def test_no_match(self):
        input = [
            ".479.",
            ".....",
        ]
        actual = main(input)
        self.assertEqual(actual, [])

    def test_empty(self):
        assert main([]) == []


@dataclasses.dataclass
class Point:
    x: int
    y: int


@dataclasses.dataclass
class Part:
    number: int
    start: Point
    end: Point

    def print(self, grid: Grid) -> None:
        """Print the part of the grid around this part."""
        points_to_check = self.generate_points_to_check()

        width = len(str(self.number)) + 2

        for i in range(0, 3):
            start = i*width
            end = (i+1)*width - 1
            cur_points = points_to_check[start:end]
            print("".join([grid.get(point) for point in cur_points]))

    def generate_points_to_check(self) -> list[Point]:
        """Generate all points in and around this part."""
        start_x = self.start.x - 1
        start_y = self.start.y - 1
        end_x = self.end.x + 1 + 1  # add extra 1 because slice end is non-inclusive
        end_y = self.end.y + 1 + 1

        if DEBUG:
            print(f"{self.start.x}:{self.end.x} -> {start_x}:{end_x}")
            print(f"{self.start.y}:{self.end.y} -> {start_y}:{end_y}")

        points_to_check: list[Point] = [
            Point(x, y)
            for y in range(start_y, end_y)
            for x in range(start_x, end_x)
        ]
        return points_to_check


class Grid:
    PART_ID_PATTERN = re.compile(r"(\d+)")

    def __init__(self, lines: list[str]):
        self.lines = lines
        self.parts = self._locate_parts()
    
    def solve(self) -> list[int]:
        valid_part_numbers: list[int] = []

        for part in self.parts:
            if part.start.y != part.end.y:
                raise ValueError("Parts should always have the same start and end Y value", part)
            
            points_to_check = part.generate_points_to_check()

            expected_number_of_points_to_check = 3 * (len(str(part.number)) + 2)
            if len(points_to_check) != expected_number_of_points_to_check:
                raise ValueError(f"{expected_number_of_points_to_check} != {len(points_to_check)}")

            for point in points_to_check:
                char = self.get(point)
                is_valid_part = char != "." and not char.isnumeric()
                if is_valid_part:
                    valid_part_numbers.append(part.number)
                    
                    if DEBUG:
                        part.print(self)
                    
                    break

        return valid_part_numbers
    
    def _locate_parts(self) -> list[Part]:
        parts = []
        
        for y, line in enumerate(self.lines):
            matches = self.PART_ID_PATTERN.finditer(line)
            for match in matches:
                id = int(match.group())
                start = Point(match.start(), y)
                end = Point(match.end() - 1, y)  # note `end` is inclusive, not exclusive like slices. argh!
                part = Part(id, start, end)
                parts.append(part)
        
        return parts
    
    def get(self, point: Point) -> str:
        """Get the char at this point or a nil value."""
        try:
            return self.lines[point.y][point.x]
        except LookupError:
            return "."


def main(input: list[str]) -> list[int]:
    grid = Grid(input)
    part_numbers = grid.solve()
    return part_numbers


if __name__ == "__main__":
    path = pathlib.Path(sys.argv[1])

    input: list[str]
    if path.exists():
        input = path.read_text().splitlines()
    else:
        input = sys.argv[1:]

    solution = main(input)
    print(sum(solution))
