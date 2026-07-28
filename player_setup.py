import pygame

CELL_SIZE = 30

PACMAN_UP_1 = pygame.transform.scale(pygame.image.load('assets/pacman-up/1.png'), (CELL_SIZE - 8, CELL_SIZE - 8))
PACMAN_UP_2 = pygame.transform.scale(pygame.image.load('assets/pacman-up/2.png'), (CELL_SIZE - 8, CELL_SIZE - 8))
PACMAN_UP_3 = pygame.transform.scale(pygame.image.load('assets/pacman-up/3.png'), (CELL_SIZE - 8, CELL_SIZE - 8))
PACMAN_DOWN_1 = pygame.transform.scale(pygame.image.load('assets/pacman-down/1.png'), (CELL_SIZE - 8, CELL_SIZE - 8))
PACMAN_DOWN_2 = pygame.transform.scale(pygame.image.load('assets/pacman-down/2.png'), (CELL_SIZE - 8, CELL_SIZE - 8))
PACMAN_DOWN_3 = pygame.transform.scale(pygame.image.load('assets/pacman-down/3.png'), (CELL_SIZE - 8, CELL_SIZE - 8))
PACMAN_LEFT_1 = pygame.transform.scale(pygame.image.load('assets/pacman-left/1.png'), (CELL_SIZE - 8, CELL_SIZE - 8))
PACMAN_LEFT_2 = pygame.transform.scale(pygame.image.load('assets/pacman-left/2.png'), (CELL_SIZE - 8, CELL_SIZE - 8))
PACMAN_LEFT_3 = pygame.transform.scale(pygame.image.load('assets/pacman-left/3.png'), (CELL_SIZE - 8, CELL_SIZE - 8))
PACMAN_RIGHT_1 = pygame.transform.scale(pygame.image.load('assets/pacman-right/1.png'), (CELL_SIZE - 8, CELL_SIZE - 8))
PACMAN_RIGHT_2 = pygame.transform.scale(pygame.image.load('assets/pacman-right/2.png'), (CELL_SIZE - 8, CELL_SIZE - 8))
PACMAN_RIGHT_3 = pygame.transform.scale(pygame.image.load('assets/pacman-right/3.png'), (CELL_SIZE - 8, CELL_SIZE - 8))


class Player:
    def __init__(self, grid: list[list[int]], width: int, height: int) -> None:
        self.grid = grid
        self.center: tuple[int, int] = (width // 2, height // 2)
        if self.grid[self.center[1]][self.center[0]] == 0xF:
            while self.grid[self.center[1]][self.center[0]] == 0xF:
                self.center = (self.center[0] - 1, self.center[1])
        self.position: tuple[int, int] = self.center
        self.lives: int = 3
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

    def move(self) -> None:
        dir_map = {
                '': (0x0, 0, 0),
                'U' : (0x1, 0 , -1),
                'R' : (0x2, 1, 0),
                'D' : (0x4, 0, 1),
                'L' : (0x8, -1, 0)
                }
        if self.grid[self.position[1]][self.position[0]] & dir_map[self.cur_dir][0]:
            return
        self.position = (self.position[0] + dir_map[self.cur_dir][1],
                         self.position[1] + dir_map[self.cur_dir][2])

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
