from typing import Tuple, List, Dict
from mazegenerator import MazeGenerator


def maze_loader(maze_size: Tuple[int, int], maze_seed: int) -> Dict:
    mg: MazeGenerator = MazeGenerator(size=maze_size, seed=maze_seed)
    maze: Dict = {
        'grid': mg.maze,
        'maze_entry': mg.maze_entry,
        'maze_exit': mg.maze_exit
    }
    return maze


class Pacgum:
    def __init__(self, position: Tuple[int, int]) -> None:
        self.position: Tuple[int, int] = position
        self.eaten: bool = False
        self.points = 10

    def eat(self) -> int:
        self.eaten = True
        return self.points


class SuperPacgum(Pacgum):
    def __init__(self, position: Tuple[int, int]) -> None:
        super().__init__(position)
        self.points = 50


def place_pacgums(
    maze_size: Tuple[int, int],
    maze_grid: List[List[int]]
) -> List[Pacgum]:
    pacgums: List[Pacgum] = []
    w, h = maze_size
    corners: List[Tuple[int, int]] = [
        (0, 0), (w - 1, 0), (0, h - 1), (w - 1, h - 1)
    ]
    for row in range(h):
        for col in range(w):
            if maze_grid[row][col] != 0xF and (col, row) not in corners:
                pacgums.append(Pacgum((col, row)))
    for cor in corners:
        pacgums.append(SuperPacgum(cor))
    return pacgums
