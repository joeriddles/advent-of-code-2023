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
        expected = [1]
        assert actual == expected

    def test_example(self):
        input: list[str] = """Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green""".splitlines()
        actual = main(input)
        expected = [1, 2, 5]
        assert actual == expected
    
    # def test_file(self):
    #     input = pathlib.Path(BASE_DIR / "input.txt").read_text().splitlines()
    #     actual = sum(main(input))
    #     assert actual == 54_877
    
    def test_empty(self):
        assert main([]) == []


@dataclasses.dataclass
class Game:
    id: int
    plays: list[dict[str, int]]

    def get_possible(self, max: dict[str, int]) -> bool:
        possible = True

        for play in self.plays:
            for key, play_val in play.items():
                max_val = max[key]
                if play_val > max_val:
                    possible = False
                    break

        return possible

    @classmethod
    def from_str(cls, input: str) -> Game:
        # TODO: refactor this into smaller functions

        game_str, play_str = input.split(":", maxsplit=1)
        id = int(game_str.split()[-1]) # there is a cleaner way of doing this...
        
        play_strs = [play_str.strip() for play_str in play_str.split(";")]
        play_tuples: list[list[tuple[int, str]]] = []
        for play_str in play_strs:
            move_strs = [move_str.strip() for move_str in play_str.split(",")]
            moves_for_play = [(int(splt[0]), splt[1]) for move_str in move_strs if (splt := move_str.split())]
            play_tuples.append(moves_for_play)

        plays: list[dict[str, int]] = []
        for moves in play_tuples:
            play = collections.defaultdict(lambda: 0)
            for num, color in moves:
                play[color] += num
            plays.append(play)

        return Game(id, plays)
    

def main(input: list[str]) -> list[int]:
    max: dict[str, int] = {
        "red": 12,
        "green": 13,
        "blue": 14,
    }
    possible_game_ids = []
    for line in input:
        game = Game.from_str(line)
        if game.get_possible(max):
            possible_game_ids.append(game.id)
    return possible_game_ids


if __name__ == "__main__":
    path = pathlib.Path(sys.argv[1])

    input: list[str]
    if path.exists():
        input = path.read_text().splitlines()
    else:
        input = sys.argv[1:]

    solution = main(input)
    print(sum(solution))
