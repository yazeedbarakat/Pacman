"""Maze loading, pacgum placement, and maze/pacgum drawing.

Wraps the external mazegenerator package, defines the Pacgum and
SuperPacgum collectibles, and renders the maze grid from its wall
bitmasks.
"""

import random
from typing import Any
from mazegenerator import MazeGenerator
import pygame

from constants import CELL_SIZE

pygame.init()


def maze_loader(maze_size: tuple[int, int], maze_seed: int) -> dict[str, Any]:
    """Generate a maze using the external MazeGenerator package.

    Args:
        maze_size: (width, height) of the maze in cells.
        maze_seed: Seed for reproducible maze generation.

    Returns:
        A dict with 'grid' (the wall bitmask grid), 'maze_entry', and
        'maze_exit'.
    """
    mg = MazeGenerator(size=maze_size, seed=maze_seed)
    maze: dict[str, Any] = {}
    maze['grid'] = mg.maze
    maze['maze_entry'] = mg.maze_entry
    maze['maze_exit'] = mg.maze_exit
    return maze


class Pacgum:
    """A single collectible pellet worth points when eaten."""

    def __init__(self, position: tuple[int, int], points: int = 10) -> None:
        """Place a pacgum at the given grid position.

        Args:
            position: (x, y) grid cell the pacgum occupies.
            points: Score awarded when this pacgum is eaten.
        """
        self.position: tuple[int, int] = position
        self.eaten: bool = False
        self.points = points

    def eat(self) -> int:
        """Mark the pacgum as eaten and return the points it's worth.

        Returns:
            The number of points earned.
        """
        self.eaten = True
        return self.points


class SuperPacgum(Pacgum):
    """A pacgum worth more points that also makes ghosts edible."""

    def __init__(self, position: tuple[int, int], points: int = 50) -> None:
        """Place a super-pacgum at the given grid position.

        Args:
            position: (x, y) grid cell the super-pacgum occupies.
            points: Score awarded when this super-pacgum is eaten.
        """
        super().__init__(position, points)


def place_pacgums(maze_size: tuple[int, int], maze_grid: list[list[int]],
                  points: int = 10, super_points: int = 50,
                  max_pacgums: int = -1) -> list[Pacgum]:
    """Fill the corridors with pacgums, and each corner with a super-pacgum.

    Args:
        maze_size: (width, height) of the maze in cells.
        maze_grid: The maze's wall bitmask grid.
        points: Score each pacgum is worth (config points_per_pacgum).
        super_points: Score each super-pacgum is worth
            (config points_per_super_pacgum).
        max_pacgums: Cap on regular pacgums placed (config pacgum);
            corridors to fill are randomly sampled when there are more
            than this. Negative means no cap.

    Returns:
        The list of placed Pacgum and SuperPacgum instances.
    """
    corners: list[tuple[int, int]] = [
        (0, 0), (maze_size[0] - 1, 0), (0, maze_size[1] - 1),
        (maze_size[0] - 1, maze_size[1] - 1)
    ]
    cells: list[tuple[int, int]] = []
    for row in range(maze_size[1]):
        for col in range(maze_size[0]):
            if maze_grid[row][col] != 0xF and (col, row) not in corners:
                cells.append((col, row))
    if 0 <= max_pacgums < len(cells):
        cells = random.sample(cells, max_pacgums)
    pacgums: list[Pacgum | SuperPacgum] = [
        Pacgum(cell, points) for cell in cells]
    for cor in corners:
        pacgums.append(SuperPacgum(cor, super_points))
    return pacgums


def draw_pacgums(
    screen: pygame.Surface, pacgums: list[Pacgum], maze_x: int, maze_y: int
) -> None:
    """Draw every uneaten pacgum, drawing super-pacgums larger.

    Args:
        screen: Surface to draw onto.
        pacgums: Pacgums (and super-pacgums) to draw.
        maze_x: Pixel x-offset of the maze's top-left corner.
        maze_y: Pixel y-offset of the maze's top-left corner.
    """
    rad = 3
    for pacgum in pacgums:
        if not pacgum.eaten:
            if isinstance(pacgum, SuperPacgum):
                rad = 6
            pygame.draw.circle(
                screen, 'yellow',
                (pacgum.position[0] * CELL_SIZE + CELL_SIZE // 2 + maze_x,
                 pacgum.position[1] * CELL_SIZE + CELL_SIZE // 2 + maze_y),
                rad)


def draw_maze(
    screen: pygame.Surface, maze: dict[str, Any], maze_x: int, maze_y: int
) -> None:
    """Draw the maze grid, rendering corridors per-cell from the wall bitmask.

    Each cell's low 4 bits mark walls (up/right/down/left); a cleared
    bit is an open side, drawn as a black corridor over the dark-blue
    cell. Cells of 0xF are solid blocks drawn grey.

    Args:
        screen: Surface to draw onto.
        maze: Maze dict as returned by maze_loader, using its 'grid' key.
        maze_x: Pixel x-offset of the maze's top-left corner.
        maze_y: Pixel y-offset of the maze's top-left corner.
    """
    for y, row in enumerate(maze['grid']):
        for x, cell in enumerate(row):
            sx, sy = x * CELL_SIZE + maze_x, y * CELL_SIZE + maze_y
            if cell == 0xF:
                pygame.draw.rect(screen, 'grey', (sx, sy, CELL_SIZE, CELL_SIZE))
                continue
            else:
                pygame.draw.rect(screen, 'dark blue', (sx, sy, CELL_SIZE, CELL_SIZE))
            if not (cell & 0x1):
                pygame.draw.rect(screen, 'black', (sx + 4, sy, CELL_SIZE - 8,
                                                   CELL_SIZE // 2))
            if not (cell & 0x2):
                pygame.draw.rect(screen, 'black', (sx + CELL_SIZE // 2, sy + 4,
                                                   CELL_SIZE // 2, CELL_SIZE - 8))
            if not (cell & 0x4):
                pygame.draw.rect(screen, 'black', (sx + 4, sy + CELL_SIZE // 2,
                                                   CELL_SIZE - 8, CELL_SIZE // 2))
            if not (cell & 0x8):
                pygame.draw.rect(screen, 'black', (sx, sy + 4,
                                                   CELL_SIZE // 2, CELL_SIZE - 8))
            pygame.draw.rect(screen, 'black', (sx + 4, sy + 4,
                                               CELL_SIZE - 8, CELL_SIZE - 8))
