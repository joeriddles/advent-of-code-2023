from __future__ import annotations

import collections
import dataclasses
import pathlib
import unittest
import sys

BASE_DIR = pathlib.Path(__file__).parent

class Tests(unittest.TestCase):
    def test_example_short(self):
        input = "Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green"
        actual = main([input])
        expected = [48]
        assert actual == expected

    def test_example(self):
        input: list[str] = """Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green""".splitlines()
        actual = main(input)
        expected = [48, 12, 1560, 630, 36]
        assert actual == expected
    
    def test_empty(self):
        assert main([]) == []


@dataclasses.dataclass
class Game:
    id: int
    plays: list[list[tuple[int, str]]]

    @classmethod
    def from_str(cls, input: str) -> Game:
        # TODO: refactor this into smaller functions

        game_str, play_str = input.split(":", maxsplit=1)
        id = int(game_str.split()[-1]) # there is a cleaner way of doing this...
        
        play_strs = [play_str.strip() for play_str in play_str.split(";")]
        plays: list[list[tuple[int, str]]] = []
        for play_str in play_strs:
            move_strs = [move_str.strip() for move_str in play_str.split(",")]
            moves_for_play = [(int(splt[0]), splt[1]) for move_str in move_strs if (splt := move_str.split())]
            plays.append(moves_for_play)

        return Game(id, plays)
    

def main(input: list[str]) -> list[int]:
    games = [Game.from_str(line) for line in input]

    games_maxs: list[dict[str, int]] = []
    for game in games:
        max_num_by_color: dict[str, int] = collections.defaultdict(lambda: 0)
        for play in game.plays:
            for num, color in play:
                if num > max_num_by_color[color]:
                    max_num_by_color[color] = num
        games_maxs.append(max_num_by_color)
    
    powers: list[int] = []
    for game_max in games_maxs:
        power = 1
        for num in game_max.values():
            power *= num
        powers.append(power)

    return powers


if __name__ == "__main__":
    path = pathlib.Path(sys.argv[1])

    input: list[str]
    if path.exists():
        input = path.read_text().splitlines()
    else:
        input = sys.argv[1:]

    solution = main(input)
    print(sum(solution))
