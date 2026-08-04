from sys import exit
import player_setup
import  pygame
import maze as m
from config_parser import read_config

con = read_config('config.json')

def get_level_config(level_index):
    level = con['levels'][level_index]
    width = level['width']
    height = level['height']
    return width, height

maze_width, maze_height = get_level_config(0)
level_time = con['level_max_time']
CELL_SIZE = 30
SCREEN_WIDTH, SCREEN_HEIGHT = maze_width * CELL_SIZE, maze_height * CELL_SIZE
FPS = 60


pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Pacman')
clock = pygame.time.Clock()
maze = m.maze_loader((maze_width, maze_height), 42)
pacgums = m.place_pacgums((maze_width, maze_height), maze['grid'])
player = player_setup.Player(maze['grid'], maze_width, maze_height)


def draw_maze(maze: dict, cell_size: int) -> None:
    for y, row in enumerate(maze['grid']):
        for x, cell in enumerate(row):
            sx, sy = x * cell_size, y * cell_size
            if cell == 0xF:
                pygame.draw.rect(screen, 'grey', (sx, sy, cell_size, cell_size))
                continue
            else:
                pygame.draw.rect(screen, 'black', (sx, sy, cell_size, cell_size))
            if not (cell & 0x1):
                pygame.draw.rect(screen, 'dark red', (sx + 4, sy, cell_size - 8,
                    cell_size // 2))
            if not (cell & 0x2):
                pygame.draw.rect(screen, 'dark red', (sx + cell_size // 2, sy + 4,
                    cell_size // 2, cell_size - 8))
            if not (cell & 0x4):
                pygame.draw.rect(screen, 'dark red', (sx + 4, sy + cell_size // 2,
                    cell_size - 8, cell_size // 2))
            if not (cell & 0x8):
                pygame.draw.rect(screen, 'dark red', (sx, sy + 4,
                    cell_size // 2, cell_size - 8))
            pygame.draw.rect(screen, 'dark red', (sx + 4, sy + 4,
                cell_size - 8, cell_size - 8))

def draw_pacman() -> None:
    screen.blit(player.get_frame(), (player.position[0] * CELL_SIZE + 4,
        player.position[1] * CELL_SIZE + 4))

def draw_pacgums() -> None:
    rad = 3
    for pacgum in pacgums:
        if not pacgum.eaten:
            if isinstance(pacgum, m.SuperPacgum):
                rad = 6
            pygame.draw.circle(screen, 'yellow', (pacgum.position[0] * CELL_SIZE + CELL_SIZE // 2,
                pacgum.position[1] * CELL_SIZE + CELL_SIZE // 2), rad)


def switch_level(level_index) -> None:
    global maze_width, maze_height, SCREEN_WIDTH, SCREEN_HEIGHT, screen,\
    maze, pacgums, player, level_time
    maze_width, maze_height = get_level_config(level_index)
    SCREEN_WIDTH, SCREEN_HEIGHT = maze_width * CELL_SIZE, maze_height * CELL_SIZE
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('Pacman')
    maze = m.maze_loader((maze_width, maze_height), 42)
    pacgums = m.place_pacgums((maze_width, maze_height), maze['grid'])
    score = player.score
    lives = player.lives
    player = player_setup.Player(maze['grid'], maze_width, maze_height)
    player.score = score
    player.lives = lives
    level_time = con['level_max_time']

def main() -> None:
    global level_time
    frame_tick_count = 0
    timer_tick_count = 0
    level_index = 0
    while True:
        if level_index > len(con['levels']):
            pygame.quit()
            exit()
        clock.tick(FPS)
        frame_tick_count += 1
        timer_tick_count += 1
        if frame_tick_count == 10:
            player.update_frame()
            player.move()
            for pacgum in pacgums:
                if not pacgum.eaten and pacgum.position == player.position:
                    pacgum.eaten = True
                    player.score += pacgum.eat()
            frame_tick_count = 0
        if timer_tick_count >= FPS:
            timer_tick_count = 0
            level_time -= 1
            if level_time <= 0:
                pygame.quit()
                exit()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    player.cur_dir = 'U'
                elif event.key == pygame.K_DOWN:
                    player.cur_dir = 'D'
                elif event.key == pygame.K_LEFT:
                    player.cur_dir = 'L'
                elif event.key == pygame.K_RIGHT:
                    player.cur_dir = 'R'
        draw_maze(maze, CELL_SIZE)
        draw_pacgums()
        draw_pacman()
        pygame.display.update()
        if all(pacgum.eaten for pacgum in pacgums):
            print(f"Level complete! {player.score}")
            level_index += 1
            switch_level(level_index)

if __name__ == '__main__':
    main()
