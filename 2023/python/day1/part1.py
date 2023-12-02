import pathlib
import sys
import unittest

class Tests(unittest.TestCase):
    def test_example(self):
        input: list[str] = """1abc2
pqr3stu8vwx
a1b2c3d4e5f
treb7uchet""".splitlines()
        actual = main(input)
        expected = [12, 38, 15, 77]
        assert actual == expected
    
    def test_file(self):
        input = pathlib.Path("input.txt").read_text().splitlines()
        actual = sum(main(input))
        assert actual == 54_877
    
    def test_empty(self):
        assert main([]) == []


def main(input: list[str]) -> list[int]:
    solution: list[int] = []
    
    for line in input:
        first, second = -1, -1
        for char in line:
            try:
                second = int(char)
                if first == -1:
                    first = second
            except ValueError:
                pass
        value = int(str(first) + str(second))
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
