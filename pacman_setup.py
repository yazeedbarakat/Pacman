"""The Pacman player entity.

Defines the Pacman class: grid-based movement against the maze's wall
bitmasks, lives and score, respawning, and directional sprite
animation with interpolated drawing.
"""

import pygame

from constants import CELL_SIZE

PACMAN_UP_1 = pygame.transform.scale(pygame.image.load(
    'assets/pacman-up/1.png'), (CELL_SIZE - 15, CELL_SIZE - 15))
PACMAN_UP_2 = pygame.transform.scale(pygame.image.load(
    'assets/pacman-up/2.png'), (CELL_SIZE - 15, CELL_SIZE - 15))
PACMAN_UP_3 = pygame.transform.scale(pygame.image.load(
    'assets/pacman-up/3.png'), (CELL_SIZE - 15, CELL_SIZE - 15))
PACMAN_DOWN_1 = pygame.transform.scale(pygame.image.load(
    'assets/pacman-down/1.png'), (CELL_SIZE - 15, CELL_SIZE - 15))
PACMAN_DOWN_2 = pygame.transform.scale(pygame.image.load(
    'assets/pacman-down/2.png'), (CELL_SIZE - 15, CELL_SIZE - 15))
PACMAN_DOWN_3 = pygame.transform.scale(pygame.image.load(
    'assets/pacman-down/3.png'), (CELL_SIZE - 15, CELL_SIZE - 15))
PACMAN_LEFT_1 = pygame.transform.scale(pygame.image.load(
    'assets/pacman-left/1.png'), (CELL_SIZE - 15, CELL_SIZE - 15))
PACMAN_LEFT_2 = pygame.transform.scale(pygame.image.load(
    'assets/pacman-left/2.png'), (CELL_SIZE - 15, CELL_SIZE - 15))
PACMAN_LEFT_3 = pygame.transform.scale(pygame.image.load(
    'assets/pacman-left/3.png'), (CELL_SIZE - 15, CELL_SIZE - 15))
PACMAN_RIGHT_1 = pygame.transform.scale(pygame.image.load(
    'assets/pacman-right/1.png'), (CELL_SIZE - 15, CELL_SIZE - 15))
PACMAN_RIGHT_2 = pygame.transform.scale(pygame.image.load(
    'assets/pacman-right/2.png'), (CELL_SIZE - 15, CELL_SIZE - 15))
PACMAN_RIGHT_3 = pygame.transform.scale(pygame.image.load(
    'assets/pacman-right/3.png'), (CELL_SIZE - 15, CELL_SIZE - 15))


class Pacman:
    """The player character: grid movement, lives/score, sprite anim."""

    def __init__(
        self, grid: list[list[int]], width: int, height: int,
        con_lives: int
    ) -> None:
        """Spawn Pacman at the maze center, nudging off any wall cell.

        Args:
            grid: The maze's wall bitmask grid.
            width: Maze width in cells.
            height: Maze height in cells.
            con_lives: Starting number of lives, from the config.
        """
        self.grid = grid
        self.center: tuple[int, int] = (width // 2, height // 2)
        if self.grid[self.center[1]][self.center[0]] == 0xF:
            while self.grid[self.center[1]][self.center[0]] == 0xF:
                self.center = (self.center[0] - 1, self.center[1])
        self.position: tuple[int, int] = self.center
        self.prev_position: tuple[int, int] = self.center
        self.lives: int = con_lives
        self.cur_dir: str = ''
        self.nxt_dir: str = ''
        self.score: int = 0
        self.frame_index: int = 0
        self.frames = {
            'U': [PACMAN_UP_1, PACMAN_UP_2, PACMAN_UP_3],
            'R': [PACMAN_RIGHT_1, PACMAN_RIGHT_2, PACMAN_RIGHT_3],
            'D': [PACMAN_DOWN_1, PACMAN_DOWN_2, PACMAN_DOWN_3],
            'L': [PACMAN_LEFT_1, PACMAN_LEFT_2, PACMAN_LEFT_3]
        }

    def move(self, steps: int) -> None:
        """Advance up to `steps` cells in the current direction,
        stopping at walls.

        Args:
            steps: Number of grid cells to attempt to move (1 normally,
                2 with the speed-boost cheat).
        """
        dir_map = {
            '': (0x0, 0, 0),
            'U': (0x1, 0, -1),
            'R': (0x2, 1, 0),
            'D': (0x4, 0, 1),
            'L': (0x8, -1, 0)
        }
        self.prev_position = self.position
        for i in range(steps):
            if (self.grid[self.position[1]][self.position[0]]
                    & dir_map[self.cur_dir][0]):
                break
            self.position = (self.position[0] + dir_map[self.cur_dir][1],
                             self.position[1] + dir_map[self.cur_dir][2])

    def respawn(self) -> bool:
        """Lose a life and reset to the maze center.

        Returns:
            True if Pacman still has lives remaining, False if this
            was the last life.
        """
        self.lives -= 1
        self.position = self.center
        self.prev_position = self.center
        return self.lives > 0

    def get_frame(self) -> pygame.Surface:
        """Get the current animation frame for the current facing direction.

        Returns:
            The sprite surface to draw; defaults to the idle-left
            frame if no direction has been set yet.
        """
        if self.cur_dir == '':
            return self.frames['L'][0]
        return self.frames[self.cur_dir][self.frame_index]

    def update_frame(self) -> None:
        """Advance the walking animation to the next of its 3 frames."""
        self.frame_index = (self.frame_index + 1) % 3

    def draw_pacman(
        self, screen: pygame.Surface, frame_tick_count: int,
        maze_x: int, maze_y: int, speed_boost: bool, fraction: int
    ) -> None:
        """Draw Pacman, interpolated between its previous and current cell.

        Args:
            screen: Surface to draw onto.
            frame_tick_count: Tick within the movement cycle (1-10),
                used to interpolate the on-screen position.
            maze_x: Pixel x-offset of the maze's top-left corner.
            maze_y: Pixel y-offset of the maze's top-left corner.
        """
        draw_x = self.prev_position[0] + (
            self.position[0] - self.prev_position[0]) * frame_tick_count / fraction
        draw_y = self.prev_position[1] + (
            self.position[1] - self.prev_position[1]) * frame_tick_count / fraction
        screen.blit(self.get_frame(), (
            draw_x * CELL_SIZE + 8 + maze_x, draw_y * CELL_SIZE + 8 + maze_y))
