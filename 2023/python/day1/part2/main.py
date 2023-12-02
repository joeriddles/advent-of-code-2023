import pathlib
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
        assert actual == ...
    
    def test_empty(self):
        assert main([]) == []


def main(input: list[str]) -> list[int]:
    solution: list[int] = []
    
    for line in input:
        ...

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
