from typing import List, Tuple, Dict
import pygame

CELL_SIZE = 18


class Player:
    def __init__(
        self,
        grid: List[List[int]],
        width: int,
        height: int,
        cell_size: int = 18
    ) -> None:
        self.grid = grid
        self.cell_size = cell_size
        self.offset = 2
        self.center: Tuple[int, int] = (width // 2, height // 2)
        if self.grid[self.center[1]][self.center[0]] == 0xF:
            while self.grid[self.center[1]][self.center[0]] == 0xF:
                self.center = (self.center[0] - 1, self.center[1])
        self.position: Tuple[int, int] = self.center
        self.lives: int = 3
        self.cur_dir: str = ''
        self.nxt_dir: str = ''
        self.score: int = 0
        self.frame_index: int = 0

        sdim = (max(12, self.cell_size - 4), max(12, self.cell_size - 4))
        self.frames: Dict[str, List[pygame.Surface]] = {
            'U': [
                pygame.transform.scale(
                    pygame.image.load('assets/pacman-up/1.png'), sdim
                ),
                pygame.transform.scale(
                    pygame.image.load('assets/pacman-up/2.png'), sdim
                ),
                pygame.transform.scale(
                    pygame.image.load('assets/pacman-up/3.png'), sdim
                ),
            ],
            'R': [
                pygame.transform.scale(
                    pygame.image.load('assets/pacman-right/1.png'), sdim
                ),
                pygame.transform.scale(
                    pygame.image.load('assets/pacman-right/2.png'), sdim
                ),
                pygame.transform.scale(
                    pygame.image.load('assets/pacman-right/3.png'), sdim
                ),
            ],
            'D': [
                pygame.transform.scale(
                    pygame.image.load('assets/pacman-down/1.png'), sdim
                ),
                pygame.transform.scale(
                    pygame.image.load('assets/pacman-down/2.png'), sdim
                ),
                pygame.transform.scale(
                    pygame.image.load('assets/pacman-down/3.png'), sdim
                ),
            ],
            'L': [
                pygame.transform.scale(
                    pygame.image.load('assets/pacman-left/1.png'), sdim
                ),
                pygame.transform.scale(
                    pygame.image.load('assets/pacman-left/2.png'), sdim
                ),
                pygame.transform.scale(
                    pygame.image.load('assets/pacman-left/3.png'), sdim
                ),
            ]
        }

    def move(self) -> None:
        dir_map = {
            '': (0x0, 0, 0),
            'U': (0x1, 0, -1),
            'R': (0x2, 1, 0),
            'D': (0x4, 0, 1),
            'L': (0x8, -1, 0)
        }
        if self.cur_dir not in dir_map:
            return
        wall_flag, dx, dy = dir_map[self.cur_dir]
        if self.grid[self.position[1]][self.position[0]] & wall_flag:
            return
        self.position = (self.position[0] + dx, self.position[1] + dy)

    def respawn(self) -> bool:
        self.lives -= 1
        self.position = self.center
        return self.lives > 0

    def get_frame(self) -> pygame.Surface:
        if self.cur_dir == '':
            return self.frames['L'][0]
        return self.frames[self.cur_dir][self.frame_index]

    def update_frame(self) -> None:
        self.frame_index = (self.frame_index + 1) % 3
