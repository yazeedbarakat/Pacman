from typing import Any

import ghost_renderer as ghost_renderer_module
from ghost import Ghost
from high_scores_config import add_high_score
import player_setup
import pygame
import maze as m
from config_parser import read_config
from menu import display_menu, display_instructions, display_cheat_mode, \
    display_submenu, display_high_scores, display_save_name

con = read_config('config.json')
pygame.font.init()
timer_font = pygame.font.Font('assets/fonts/SourceCodePro-Bold.otf', 40)
level_font = pygame.font.Font('assets/fonts/Montserrat-Bold.otf', 45)
name_font = pygame.font.Font('assets/fonts/Comfortaa-Bold.otf', 50)


def get_level_config(level_index: int) -> tuple[int, int]:
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
heart = pygame.transform.scale(pygame.image.load('assets/menu/heart.png'), (60, 60))

pygame.init()
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Pacman')
clock = pygame.time.Clock()
maze = m.maze_loader((maze_width, maze_height), 42)
pacgums = m.place_pacgums((maze_width, maze_height), maze['grid'])
player = player_setup.Player(maze['grid'], maze_width, maze_height)
ghost_renderer = ghost_renderer_module.GhostRenderer(cell_size=CELL_SIZE)
level = 0


def make_ghosts(width: int, height: int, level: int) -> list[Ghost]:
    corners = [(0, 0), (width - 1, 0), (0, height - 1), (width - 1, height - 1)]
    return [Ghost(cx, cy, 1, maze['grid'], level) for cx, cy in corners]


def get_ghost_move_interval(level_index: int) -> int:
    num_levels = len(con['levels'])
    return max(1, num_levels - level_index)


ghosts = make_ghosts(maze_width, maze_height, level)


def set_game() -> None:
    global maze_width, maze_height, screen, maze, pacgums, \
        player, level_time, ghosts
    maze_width, maze_height = get_level_config(level_index=0)
    maze = m.maze_loader((maze_width, maze_height), 42)
    pacgums = m.place_pacgums((maze_width, maze_height), maze['grid'])
    player = player_setup.Player(maze['grid'], maze_width, maze_height)
    ghosts = make_ghosts(maze_width, maze_height, level)
    level_time = con['level_max_time']


def draw_maze(maze: dict[str, Any], cell_size: int) -> None:
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


def draw_pacman(frame_tick_count: int) -> None:
    draw_x = player.prev_position[0] + (player.position[0] -
                                        player.prev_position[0]) * frame_tick_count / 10
    draw_y = player.prev_position[1] + (player.position[1] -
                                        player.prev_position[1]) * frame_tick_count / 10
    screen.blit(player.get_frame(), (draw_x * CELL_SIZE + 4 + x_cor,
                                     draw_y * CELL_SIZE + 4 + y_cor))


def draw_pacgums() -> None:
    rad = 3
    for pacgum in pacgums:
        if not pacgum.eaten:
            if isinstance(pacgum, m.SuperPacgum):
                rad = 6
            pygame.draw.circle(
                screen, 'yellow',
                (pacgum.position[0] * CELL_SIZE + CELL_SIZE // 2 + x_cor,
                 pacgum.position[1] * CELL_SIZE + CELL_SIZE // 2 + y_cor),
                rad)


def switch_level(level_index: int) -> None:
    global maze_width, maze_height, SCREEN_WIDTH, SCREEN_HEIGHT, screen, \
        maze, pacgums, player, level_time, x_cor, ghosts
    maze_width, maze_height = get_level_config(level_index)
    x_cor = screen_width // 2 - maze_width * CELL_SIZE // 2
    maze = m.maze_loader((maze_width, maze_height), 42)
    pacgums = m.place_pacgums((maze_width, maze_height), maze['grid'])
    score = player.score
    lives = player.lives
    player = player_setup.Player(maze['grid'], maze_width, maze_height)
    player.score = score
    player.lives = lives
    ghosts = make_ghosts(maze_width, maze_height, level_index + 1)
    level_time = con['level_max_time']


def display_hearts(lives: int) -> None:
    pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(
        screen_width/2 - 350, screen_height/2 - 500, 120, 50))
    hearts = 3 if lives >= 3 else lives
    for i in range(hearts):
        screen.blit(heart, (screen_width/2 - 360 + i * 40, screen_height/2 - 505))


def display_level(level: int) -> None:
    pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(
        screen_width/2 + 200, screen_height/2 - 500, 190, 50))
    level_text = level_font.render(f'level: {level}', True, (255, 255, 255))
    screen.blit(level_text, (screen_width/2 + 200, screen_height/2 - 500))


def display_timer(time: int) -> None:
    minutes = time//60
    minutes_str = '0' + str(minutes) if minutes // 10 == 0 else str(minutes)
    seconds = time % 60
    seconds_str = '0' + str(seconds) if seconds // 10 == 0 else str(seconds)
    pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(
        screen_width/2 - 80, screen_height/2 - 500, 130, 50))
    time_text = timer_font.render(f"{minutes_str}:{seconds_str}", True, (255, 255, 255))
    screen.blit(time_text, (screen_width/2 - 75, screen_height/2 - 500))


def handle_playing(frame_tick_count: int, level_time: int, level_index: int,
                   shadow_mode: bool, invincible: bool, speed_boost: bool,
                   buttons: tuple[pygame.Rect, ...], player_name: str,
                   game_state: str,
                   ghost_tick_count: int) -> tuple[tuple[pygame.Rect, ...], int, str]:
    for ghost in ghosts:
        if not (shadow_mode) and ghost_tick_count == 1:
            ghost.update(player.position)
    if frame_tick_count == 1:
        if speed_boost:
            player.move(2)
        else:
            player.move(1)
        player.update_frame()
        dx = player.position[0] - player.prev_position[0]
        dy = player.position[1] - player.prev_position[1]
        distance = max(abs(dx), abs(dy))
        traversed = [player.position]
        if distance > 0:
            step_x = dx // distance
            step_y = dy // distance
            traversed = [(player.prev_position[0] + step_x * i,
                          player.prev_position[1] + step_y * i)
                         for i in range(1, distance + 1)]
        for pacgum in pacgums:
            if not pacgum.eaten and pacgum.position in traversed:
                pacgum.eaten = True
                player.score += pacgum.eat()
                if isinstance(pacgum, m.SuperPacgum):
                    for ghost in ghosts:
                        ghost.make_edible()
        ghost_cycle_length = 10 * get_ghost_move_interval(level_index)
        for ghost in ghosts:
            fraction = ghost_tick_count / ghost_cycle_length
            ghost_pos = (round(ghost.prev_x + (ghost.x - ghost.prev_x) * fraction),
                         round(ghost.prev_y + (ghost.y - ghost.prev_y) * fraction))
            if ghost_pos in traversed:
                if ghost.state == "escape":
                    ghost.get_eaten()
                    player.score += con['points_per_ghost']
                elif ghost.state == "chasing" and not invincible:
                    if not player.respawn():
                        game_state = "name_input"
                        display_save_name(player_name, screen, screen_width, screen_height)
                        pygame.display.update()
                        return (buttons, level_index, game_state)
        if all(pacgum.eaten for pacgum in pacgums):
            level_index += 1
            if level_index >= len(con['levels']):
                game_state = 'name_input'
                display_save_name(player_name, screen, screen_width, screen_height)
                pygame.display.update()
                return (buttons, level_index, game_state)
            else:
                switch_level(level_index)
                buttons = display_cheat_mode(screen, CELL_SIZE, screen_width, screen_height)
    draw_maze(maze, CELL_SIZE)
    draw_pacgums()
    draw_pacman(frame_tick_count)
    # subsurface lines up ghost grid coords with the maze's x_cor/y_cor offset
    maze_surface = screen.subsurface(
        (x_cor, y_cor, maze_width * CELL_SIZE, maze_height * CELL_SIZE))
    ghost_renderer.draw_ghosts(maze_surface, ghosts, ghost_tick_count,
                               10 * get_ghost_move_interval(level_index))
    display_timer(level_time)
    display_hearts(player.lives)
    display_level(level_index + 1)
    pygame.display.update()
    return (buttons, level_index, game_state)


def handle_submenu(player_name: str,
                   buttuns: tuple[pygame.Rect, ...]) -> tuple[pygame.Rect, ...]:
    buttons = display_submenu(screen, CELL_SIZE, screen_width, screen_height)
    pygame.display.update()
    return buttons


def handle_menu_buttons(
    buttons: tuple[pygame.Rect, ...], event: pygame.event.Event, game_state: str
) -> tuple[tuple[pygame.Rect, ...], str]:
    if buttons[0].collidepoint(event.pos):
        game_state = 'playing'
        buttons = display_cheat_mode(screen, CELL_SIZE, screen_width, screen_height)
    elif buttons[1].collidepoint(event.pos):
        game_state = 'instructions'
        buttons = display_menu(screen, CELL_SIZE, screen_width, screen_height)
        buttons = display_instructions(screen, CELL_SIZE, screen_width, screen_height)
    elif buttons[2].collidepoint(event.pos):
        game_state = 'high_score'
        buttons = display_high_scores(screen, CELL_SIZE, screen_width,
                                      screen_height, con['highscore_filename'])
    elif buttons[3].collidepoint(event.pos):
        pygame.quit()
        exit()
    return (buttons, game_state)


def handle_playing_buttons(
    buttons: tuple[pygame.Rect, ...], event: pygame.event.Event,
    level_index: int, invincible: bool, shadow_mode: bool,
    speed_boost: bool, time_paused: bool, game_state: str, player_name: str
) -> tuple[tuple[pygame.Rect, ...], int, bool, bool, bool, bool, str, str]:
    if buttons[0].collidepoint(event.pos):
        invincible = not (invincible)
    elif buttons[1].collidepoint(event.pos):
        player.lives = 100000
    elif buttons[2].collidepoint(event.pos):
        shadow_mode = not (shadow_mode)
    elif buttons[3].collidepoint(event.pos):
        level_index += 1
        if level_index >= len(con['levels']):
            game_state = 'name_input'
            display_save_name(player_name, screen, screen_width, screen_height)
            return (buttons, level_index, invincible, shadow_mode,
                    speed_boost, time_paused, game_state, player_name)
        else:
            switch_level(level_index)
            buttons = display_cheat_mode(screen, CELL_SIZE, screen_width, screen_height)
    elif buttons[4].collidepoint(event.pos):
        time_paused = not (time_paused)
        if time_paused:
            pygame.draw.rect(screen, (0, 255, 0), pygame.Rect(
                screen_width/2 + 800, screen_height/2, 20, 20), border_radius=50)
        else:
            pygame.draw.rect(screen, (255, 0, 0), pygame.Rect(
                screen_width/2 + 800, screen_height/2, 20, 20), border_radius=50)
    elif buttons[5].collidepoint(event.pos):
        speed_boost = not (speed_boost)
    return (buttons, level_index, invincible, shadow_mode,
            speed_boost, time_paused, game_state, player_name)


def handle_submenu_buttons(
    buttons: tuple[pygame.Rect, ...], event: pygame.event.Event, game_state: str,
    player_name: str
) -> tuple[tuple[pygame.Rect, ...], str]:
    if buttons[0].collidepoint(event.pos):
        game_state = 'playing'
        buttons = display_cheat_mode(screen, CELL_SIZE, screen_width, screen_height)
    elif buttons[1].collidepoint(event.pos):
        game_state = 'name_input'
        display_save_name(player_name, screen, screen_width, screen_height)
    return (buttons, game_state)


def main() -> None:
    global level_time
    frame_tick_count = 0
    timer_tick_count = 0
    time_paused = False
    level_index = 0
    game_state = 'menu'
    # buttons = display_cheat_mode(screen, CELL_SIZE, screen_width, screen_height)
    invincible = False
    shadow_mode = False
    speed_boost = False
    player_name = ''
    ghost_tick_count = 0
    set_game()
    buttons: tuple[pygame.Rect, ...] = display_menu(
        screen, CELL_SIZE, screen_width, screen_height)
    while True:
        clock.tick(FPS)
        frame_tick_count += 1
        timer_tick_count += 1
        ghost_tick_count += 1
        if game_state == 'playing':
            buttons, level_index, game_state = handle_playing(
                frame_tick_count, level_time, level_index, shadow_mode,
                invincible, speed_boost, buttons, player_name, game_state,
                ghost_tick_count)
        elif game_state == 'submenu':
            buttons = handle_submenu(player_name, buttons)
        elif game_state == 'name_input':
            display_save_name(player_name, screen, screen_width, screen_height)
            pygame.display.update()
        if frame_tick_count >= 10:
            frame_tick_count = 0
        ghost_cycle_length = 10 * get_ghost_move_interval(level_index)
        if ghost_tick_count >= ghost_cycle_length:
            ghost_tick_count = 0
        if timer_tick_count >= FPS:
            timer_tick_count = 0
            if not time_paused:
                level_time -= 1
            if level_time <= 0:
                pygame.quit()
                exit()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if game_state == 'menu':
                    level_index = 0
                    frame_tick_count = 0
                    ghost_tick_count = 0
                    set_game()
                    buttons, game_state = handle_menu_buttons(buttons, event, game_state)
                elif game_state == 'playing':
                    (buttons, level_index, invincible, shadow_mode,
                     speed_boost, time_paused, game_state,
                     player_name) = handle_playing_buttons(
                        buttons, event, level_index, invincible,
                        shadow_mode, speed_boost, time_paused, game_state,
                        player_name)
                elif game_state == 'submenu':
                    buttons, game_state = handle_submenu_buttons(
                        buttons, event, game_state, player_name)
                elif game_state == 'instructions':
                    if buttons[0].collidepoint(event.pos):
                        game_state = 'menu'
                        buttons = display_menu(screen, CELL_SIZE, screen_width, screen_height)
                elif game_state == 'high_score':
                    if buttons[0].collidepoint(event.pos):
                        game_state = 'menu'
                        buttons = display_menu(screen, CELL_SIZE, screen_width, screen_height)

            elif event.type == pygame.KEYDOWN and game_state == 'playing':
                if event.key == pygame.K_UP:
                    player.cur_dir = 'U'
                elif event.key == pygame.K_DOWN:
                    player.cur_dir = 'D'
                elif event.key == pygame.K_LEFT:
                    player.cur_dir = 'L'
                elif event.key == pygame.K_RIGHT:
                    player.cur_dir = 'R'
                elif event.key == pygame.K_ESCAPE:
                    game_state = 'submenu'
                    buttons = display_submenu(screen, CELL_SIZE, screen_width, screen_height)
                    pygame.display.update()
            elif event.type == pygame.KEYDOWN and game_state == 'name_input':
                if event.key == pygame.K_BACKSPACE:
                    player_name = player_name[:-1]
                elif event.key in (pygame.K_KP_ENTER, pygame.K_RETURN):
                    add_high_score(con['highscore_filename'], player_name, player.score)
                    game_state = 'menu'
                    buttons = display_menu(screen, CELL_SIZE, screen_width, screen_height)
                else:
                    if len(player_name) < 10 and (event.unicode.isalnum() or event.unicode == ' '):
                        player_name += event.unicode


if __name__ == '__main__':
    main()
