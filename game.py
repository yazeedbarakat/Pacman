from sys import exit
import player_setup
import  pygame
import maze as m
from config_parser import read_config
from menu import display_menu, display_instructions, display_cheat_mode

con = read_config('config.json')

def get_level_config(level_index):
    level = con['levels'][level_index]
    width = level['width']
    height = level['height']
    return width, height

maze_width, maze_height = get_level_config(0)
level_time = con['level_max_time']
CELL_SIZE = 30
screen_width, screen_height = 1920, 1080
x_cor = screen_width // 2 - maze_width * CELL_SIZE // 2
y_cor = screen_height // 2 - 200
FPS = 60


pygame.init()
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Pacman')
clock = pygame.time.Clock()
maze = m.maze_loader((maze_width, maze_height), 42)
pacgums = m.place_pacgums((maze_width, maze_height), maze['grid'])
player = player_setup.Player(maze['grid'], maze_width, maze_height)


def draw_maze(maze: dict, cell_size: int) -> None:
    for y, row in enumerate(maze['grid']):
        for x, cell in enumerate(row):
            sx, sy = x * cell_size + x_cor, y * cell_size + y_cor
            if cell == 0xF:
                pygame.draw.rect(screen, 'grey', (sx, sy, cell_size, cell_size))
                continue
            else:
                pygame.draw.rect(screen, 'dark blue', (sx, sy, cell_size, cell_size))
            if not (cell & 0x1):
                pygame.draw.rect(screen, 'black', (sx + 4, sy, cell_size - 8,
                    cell_size // 2))
            if not (cell & 0x2):
                pygame.draw.rect(screen, 'black', (sx + cell_size // 2, sy + 4,
                    cell_size // 2, cell_size - 8))
            if not (cell & 0x4):
                pygame.draw.rect(screen, 'black', (sx + 4, sy + cell_size // 2,
                    cell_size - 8, cell_size // 2))
            if not (cell & 0x8):
                pygame.draw.rect(screen, 'black', (sx, sy + 4,
                    cell_size // 2, cell_size - 8))
            pygame.draw.rect(screen, 'black', (sx + 4, sy + 4,
                cell_size - 8, cell_size - 8))

def draw_pacman() -> None:
    screen.blit(player.get_frame(), (player.position[0] * CELL_SIZE + 4 + x_cor,
        player.position[1] * CELL_SIZE + 4 + y_cor))

def draw_pacgums() -> None:
    rad = 3
    for pacgum in pacgums:
        if not pacgum.eaten:
            if isinstance(pacgum, m.SuperPacgum):
                rad = 6
            pygame.draw.circle(screen, 'yellow', (pacgum.position[0] * \
                CELL_SIZE + CELL_SIZE // 2 + x_cor,
                pacgum.position[1] * CELL_SIZE + CELL_SIZE // 2 + y_cor), rad)

def switch_level(level_index) -> None:
    global maze_width, maze_height, SCREEN_WIDTH, SCREEN_HEIGHT, screen,\
    maze, pacgums, player, level_time, x_cor
    maze_width, maze_height = get_level_config(level_index)
    x_cor = screen_width // 2 - maze_width * CELL_SIZE // 2
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
    game_state = 'menu'
    buttons = display_menu(screen, CELL_SIZE, screen_width, screen_height)

    while True:
        clock.tick(FPS)
        frame_tick_count += 1
        timer_tick_count += 1
        if frame_tick_count == 10:
            if game_state == 'playing':
                player.move()
                player.update_frame()
                for pacgum in pacgums:
                    if not pacgum.eaten and pacgum.position == player.position:
                        pacgum.eaten = True
                        player.score += pacgum.eat()
            frame_tick_count = 0
        if game_state == 'playing':
            draw_maze(maze, CELL_SIZE)
            draw_pacgums()
            draw_pacman()
        pygame.display.update()
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
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if buttons[0].collidepoint(event.pos):
                    game_state = 'playing'
                    buttons = display_menu(screen, CELL_SIZE, screen_width, screen_height)
                    display_cheat_mode(screen, CELL_SIZE, screen_width, screen_height)
                elif buttons[1].collidepoint(event.pos):
                    buttons = display_menu(screen, CELL_SIZE, screen_width, screen_height)
                    display_instructions(screen, CELL_SIZE, screen_width, screen_height)
                    game_state = 'instructions'
                elif buttons[2].collidepoint(event.pos):
                    game_state = 'high_score'
                elif buttons[3].collidepoint(event.pos):
                    pygame.quit()
                    exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    player.cur_dir = 'U'
                elif event.key == pygame.K_DOWN:
                    player.cur_dir = 'D'
                elif event.key == pygame.K_LEFT:
                    player.cur_dir = 'L'
                elif event.key == pygame.K_RIGHT:
                    player.cur_dir = 'R'
        if all(pacgum.eaten for pacgum in pacgums):
            print(f"Level complete! {player.score}")
            level_index += 1
            if level_index >= len(con['levels']):
                pygame.quit()
                exit()
            buttons = display_menu(screen, CELL_SIZE, screen_width, screen_height)
            switch_level(level_index)

if __name__ == '__main__':
    main()
