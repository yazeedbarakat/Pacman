import ghost_renderer as ghost_renderer_module
from ghost import Ghost
from high_scores_config import add_high_score
import pacman_setup
import pygame
import maze_pacgum as m
from config_parser import read_config
from constants import CELL_SIZE
from displays import display_menu, display_instructions, display_cheat_mode, \
    display_submenu, display_high_scores, display_save_name, init_gif, \
    init_display, display_hearts, display_level, display_timer

con = read_config('config.json')
pygame.font.init()


def get_level_config(level_index: int) -> tuple[int, int]:
    level = con['levels'][level_index]
    width = level['width']
    height = level['height']
    return width, height


maze_width, maze_height = get_level_config(0)
level_time = con['level_max_time']
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
pacman = pacman_setup.Pacman(maze['grid'], maze_width, maze_height)
ghost_renderer = ghost_renderer_module.GhostRenderer(cell_size=CELL_SIZE)
level = 0
init_gif()


def make_ghosts(width: int, height: int, level: int) -> list[Ghost]:
    corners = [(0, 0), (width - 1, 0), (0, height - 1), (width - 1, height - 1)]
    return [Ghost(cx, cy, 1, maze['grid'], level) for cx, cy in corners]


def get_ghost_move_interval(level_index: int) -> int:
    num_levels = len(con['levels'])
    return max(1, num_levels - level_index)


ghosts = make_ghosts(maze_width, maze_height, level)


def set_game() -> None:
    global maze_width, maze_height, maze, pacgums, pacman, level_time, ghosts
    maze_width, maze_height = get_level_config(level_index=0)
    maze = m.maze_loader((maze_width, maze_height), 42)
    pacgums = m.place_pacgums((maze_width, maze_height), maze['grid'])
    pacman = pacman_setup.Pacman(maze['grid'], maze_width, maze_height)
    ghosts = make_ghosts(maze_width, maze_height, level)
    level_time = con['level_max_time']


def switch_level(level_index: int) -> None:
    global maze_width, maze_height, maze, pacgums, pacman, level_time, x_cor, ghosts
    maze_width, maze_height = get_level_config(level_index)
    x_cor = screen_width // 2 - maze_width * CELL_SIZE // 2
    maze = m.maze_loader((maze_width, maze_height), 42)
    pacgums = m.place_pacgums((maze_width, maze_height), maze['grid'])
    score = pacman.score
    lives = pacman.lives
    pacman = pacman_setup.Pacman(maze['grid'], maze_width, maze_height)
    pacman.score = score
    pacman.lives = lives
    ghosts = make_ghosts(maze_width, maze_height, level_index + 1)
    level_time = con['level_max_time']


def handle_playing(frame_tick_count: int, level_time: int, level_index: int,
                   shadow_mode: bool, invincible: bool, speed_boost: bool,
                   time_paused: bool, buttons: tuple[pygame.Rect, ...],
                   player_name: str, game_state: str,
                   ghost_tick_count: int) -> tuple[tuple[pygame.Rect, ...], int, str]:
    for ghost in ghosts:
        if not (shadow_mode) and ghost_tick_count == 1:
            ghost.update(pacman.position)
    if frame_tick_count == 1:
        if speed_boost:
            pacman.move(2)
        else:
            pacman.move(1)
        pacman.update_frame()
        dx = pacman.position[0] - pacman.prev_position[0]
        dy = pacman.position[1] - pacman.prev_position[1]
        distance = max(abs(dx), abs(dy))
        traversed = [pacman.position]
        if distance > 0:
            step_x = dx // distance
            step_y = dy // distance
            traversed = [(pacman.prev_position[0] + step_x * i,
                          pacman.prev_position[1] + step_y * i)
                         for i in range(1, distance + 1)]
        for pacgum in pacgums:
            if not pacgum.eaten and pacgum.position in traversed:
                pacgum.eaten = True
                pacman.score += pacgum.eat()
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
                    pacman.score += con['points_per_ghost']
                elif ghost.state == "chasing" and not invincible:
                    if not pacman.respawn():
                        game_state = "name_input"
                        display_save_name(player_name)
                        pygame.display.update()
                        return (buttons, level_index, game_state)
        if all(pacgum.eaten for pacgum in pacgums):
            level_index += 1
            if level_index >= len(con['levels']):
                game_state = 'name_input'
                display_save_name(player_name)
                pygame.display.update()
                return (buttons, level_index, game_state)
            else:
                switch_level(level_index)
                buttons = display_cheat_mode(invincible, shadow_mode, speed_boost, time_paused)
    m.draw_maze(screen, maze, x_cor, y_cor)
    m.draw_pacgums(screen, pacgums, x_cor, y_cor)
    pacman.draw_pacman(screen, frame_tick_count, x_cor, y_cor)
    # subsurface lines up ghost grid coords with the maze's x_cor/y_cor offset
    maze_surface = screen.subsurface(
        (x_cor, y_cor, maze_width * CELL_SIZE, maze_height * CELL_SIZE))
    ghost_renderer.draw_ghosts(maze_surface, ghosts, ghost_tick_count,
                               10 * get_ghost_move_interval(level_index))
    display_timer(level_time)
    display_hearts(pacman.lives)
    display_level(level_index + 1)
    pygame.display.update()
    return (buttons, level_index, game_state)


def handle_submenu(player_name: str,
                   buttuns: tuple[pygame.Rect, ...]) -> tuple[pygame.Rect, ...]:
    buttons = display_submenu()
    pygame.display.update()
    return buttons


def handle_menu_buttons(
    buttons: tuple[pygame.Rect, ...], event: pygame.event.Event,
    game_state: str, invincible:  bool, shadow_mode: bool, speed_boost: bool,
    time_paused: bool
) -> tuple[tuple[pygame.Rect, ...], str]:
    if buttons[0].collidepoint(event.pos):
        game_state = 'playing'
        buttons = display_cheat_mode(invincible, shadow_mode, speed_boost, time_paused)
    elif buttons[1].collidepoint(event.pos):
        game_state = 'instructions'
        buttons = display_menu()
        buttons = display_instructions()
    elif buttons[2].collidepoint(event.pos):
        game_state = 'high_score'
        buttons = display_high_scores(con['highscore_filename'])
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
        level_index += 1
        if level_index >= len(con['levels']):
            game_state = 'name_input'
            display_save_name(player_name)
            return (buttons, level_index, invincible, shadow_mode,
                    speed_boost, time_paused, game_state, player_name)
        else:
            switch_level(level_index)
            buttons = display_cheat_mode(invincible, shadow_mode, speed_boost, time_paused)
    elif buttons[1].collidepoint(event.pos):
        if pacman.lives < 3:
            pacman.lives += 1
        buttons = display_cheat_mode(invincible, shadow_mode, speed_boost, time_paused)
    elif buttons[2].collidepoint(event.pos):
        shadow_mode = not (shadow_mode)
        buttons = display_cheat_mode(invincible, shadow_mode, speed_boost, time_paused)
    elif buttons[3].collidepoint(event.pos):
        invincible = not (invincible)
        buttons = display_cheat_mode(invincible, shadow_mode, speed_boost, time_paused)
    elif buttons[4].collidepoint(event.pos):
        time_paused = not (time_paused)
        buttons = display_cheat_mode(invincible, shadow_mode, speed_boost, time_paused)
    elif buttons[5].collidepoint(event.pos):
        speed_boost = not (speed_boost)
        buttons = display_cheat_mode(invincible, shadow_mode, speed_boost, time_paused)
    return (buttons, level_index, invincible, shadow_mode,
            speed_boost, time_paused, game_state, player_name)


def handle_submenu_buttons(
    buttons: tuple[pygame.Rect, ...], event: pygame.event.Event, game_state: str,
    player_name: str, invincible:  bool, shadow_mode: bool, speed_boost: bool,
    time_paused: bool
) -> tuple[tuple[pygame.Rect, ...], str]:
    if buttons[0].collidepoint(event.pos):
        game_state = 'playing'
        buttons = display_cheat_mode(invincible, shadow_mode, speed_boost, time_paused)
    elif buttons[1].collidepoint(event.pos):
        game_state = 'name_input'
        display_save_name(player_name)
    return (buttons, game_state)


def main() -> None:
    global level_time
    frame_tick_count = 0
    timer_tick_count = 0
    ghost_tick_count = 0
    level_index = 0
    game_state = 'menu'
    invincible = False
    shadow_mode = False
    speed_boost = False
    time_paused = False
    player_name = ''
    set_game()
    init_display(screen, screen_width, screen_height)
    buttons: tuple[pygame.Rect, ...] = display_menu()
    while True:
        clock.tick(FPS)
        frame_tick_count += 1
        timer_tick_count += 1
        ghost_tick_count += 1
        if game_state == 'playing':
            buttons, level_index, game_state = handle_playing(
                frame_tick_count, level_time, level_index, shadow_mode,
                invincible, speed_boost, time_paused, buttons, player_name, game_state,
                ghost_tick_count)
        elif game_state == 'submenu':
            buttons = handle_submenu(player_name, buttons)
        elif game_state == 'name_input':
            display_save_name(player_name)
            pygame.display.update()
        if frame_tick_count >= 10:
            frame_tick_count = 0
        ghost_cycle_length = 10 * get_ghost_move_interval(level_index)
        if ghost_tick_count >= ghost_cycle_length:
            ghost_tick_count = 0
        if timer_tick_count >= FPS:
            timer_tick_count = 0
            if not time_paused and game_state == 'playing':
                level_time -= 1
                if level_time <= 0:
                    game_state = "name_input"
                    display_save_name(player_name)
                    pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if game_state == 'menu':
                    level_index = 0
                    frame_tick_count = 0
                    ghost_tick_count = 0
                    player_name = ''
                    set_game()
                    buttons, game_state = handle_menu_buttons(
                        buttons, event, game_state, invincible, shadow_mode,
                        speed_boost, time_paused)
                elif game_state == 'playing':
                    (buttons, level_index, invincible, shadow_mode,
                     speed_boost, time_paused, game_state,
                     player_name) = handle_playing_buttons(
                        buttons, event, level_index, invincible,
                        shadow_mode, speed_boost, time_paused, game_state,
                        player_name)
                elif game_state == 'submenu':
                    buttons, game_state = handle_submenu_buttons(
                        buttons, event, game_state, player_name,
                        invincible, shadow_mode, speed_boost,
                        time_paused)
                elif game_state == 'instructions':
                    if buttons[0].collidepoint(event.pos):
                        game_state = 'menu'
                        buttons = display_menu()
                elif game_state == 'high_score':
                    if buttons[0].collidepoint(event.pos):
                        game_state = 'menu'
                        buttons = display_menu()

            elif event.type == pygame.KEYDOWN and game_state == 'playing':
                if event.key == pygame.K_UP:
                    pacman.cur_dir = 'U'
                elif event.key == pygame.K_DOWN:
                    pacman.cur_dir = 'D'
                elif event.key == pygame.K_LEFT:
                    pacman.cur_dir = 'L'
                elif event.key == pygame.K_RIGHT:
                    pacman.cur_dir = 'R'
                elif event.key == pygame.K_ESCAPE:
                    game_state = 'submenu'
                    buttons = display_submenu()
                    pygame.display.update()
            elif event.type == pygame.KEYDOWN and game_state == 'name_input':
                if event.key == pygame.K_BACKSPACE:
                    player_name = player_name[:-1]
                elif event.key in (pygame.K_KP_ENTER, pygame.K_RETURN) and player_name != '':
                    add_high_score(con['highscore_filename'], player_name, pacman.score)
                    game_state = 'menu'
                    buttons = display_menu()
                else:
                    if len(player_name) < 10 and (event.unicode.isalnum() or event.unicode == ' '):
                        player_name += event.unicode


if __name__ == '__main__':
    main()
