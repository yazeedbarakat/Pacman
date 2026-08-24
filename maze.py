from typing import Any

from mazegenerator import MazeGenerator  # type: ignore[import-not-found]


def maze_loader(maze_size: tuple[int, int], maze_seed: int) -> dict[str, Any]:
    mg = MazeGenerator(size=maze_size, seed=maze_seed)
    maze: dict[str, Any] = {}
    maze['grid'] = mg.maze
    maze['maze_entry'] = mg.maze_entry
    maze['maze_exit'] = mg.maze_exit
    return maze


class Pacgum:
    def __init__(self, position: tuple[int, int]) -> None:
        self.position: tuple[int, int] = position
        self.eaten: bool = False
        self.points = 10

    def eat(self) -> int:
        self.eaten = True
        return self.points


class SuperPacgum(Pacgum):
    def __init__(self, position: tuple[int, int]) -> None:
        super().__init__(position)
        self.points = 50


def place_pacgums(maze_size: tuple[int, int], maze_grid: list[list[int]]) -> list[Pacgum]:
    pacgums: list[Pacgum | SuperPacgum] = []
    corners: list[tuple[int, int]] = [
        (0, 0), (maze_size[0] - 1, 0), (0, maze_size[1] - 1),
        (maze_size[0] - 1, maze_size[1] - 1)
    ]
    for row in range(maze_size[1]):
        for col in range(maze_size[0]):
            if maze_grid[row][col] != 0xF and not (col, row) in corners:
                pacgums.append(Pacgum((col, row)))
    for cor in corners:
        pacgums.append(SuperPacgum(cor))
    return pacgums
