"""Entry point and main loop for the Pacman game.

Owns the game window, the top-level state machine (menu, playing,
pause submenu, name entry, instructions, high scores), level
progression, cheat mode, and all pygame event dispatch.
"""

import sys
import pygame
import random
import ghost_renderer as ghost_renderer_module
from ghost import Ghost
from high_scores_config import add_high_score
import pacman_setup
import maze_pacgum as m
from config_parser import read_config
from constants import resource_path, writable_path
from displays import display_menu, display_instructions, \
    display_cheat_mode, display_submenu, display_high_scores, \
    display_save_name, init_gif, init_display, display_hearts, \
    display_level, display_timer, display_score

if len(sys.argv) > 2:
    print('Usage: python3 game.py [config_file.json]')
    sys.exit(1)
config_path = sys.argv[1] if len(sys.argv) == 2 else resource_path(
    'config.json')
con = read_config(config_path)
HIGHSCORE_PATH = writable_path(con['highscore_filename'])
pygame.font.init()


def get_level_config(level_index: int) -> tuple[int, int]:
    """Look up a level's maze dimensions from the loaded config.

    Args:
        level_index: 0-based index into `con['levels']`.

    Returns:
        (width, height) of that level's maze in cells.
    """
    level = con['levels'][level_index]
    width = level['width']
    height = level['height']
    return width, height


CELL_SIZE = 40
maze_width, maze_height = get_level_config(0)
level_time = con['level_max_time']
screen_width, screen_height = 1920, 1080
x_cor = screen_width // 2 - maze_width * CELL_SIZE // 2
y_cor = screen_height // 2 - 300
FPS = 60

pygame.init()
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Pacman')
clock = pygame.time.Clock()
maze = m.maze_loader((maze_width, maze_height), con['seed'])
pacgums = m.place_pacgums((maze_width, maze_height), maze['grid'],
                          con['points_per_pacgum'],
                          con['points_per_super_pacgum'], con['pacgum'])
pacman = pacman_setup.Pacman(
    maze['grid'], maze_width, maze_height, con['lives'])
ghost_renderer = ghost_renderer_module.GhostRenderer(cell_size=CELL_SIZE)
level = 0
init_gif()


def make_ghosts(width: int, height: int, level: int) -> list[Ghost]:
    """Create the 4 ghosts, one spawned at each maze corner.

    Only some ghosts hunt the player, via their view_range: one chaser
    in the first 5 levels, two in the later levels. The rest get a
    view_range of 0 so they always wander randomly.

    Args:
        width: Maze width in cells.
        height: Maze height in cells.
        level: Current level, used to scale each ghost's difficulty
            and pick how many ghosts chase.

    Returns:
        The 4 newly created Ghost instances.
    """
    corners = [
        (0, 0), (width - 1, 0), (0, height - 1), (width - 1, height - 1)]
    num_chasers = 1 if level <= 5 else 2
    ghosts = []
    for i, (cx, cy) in enumerate(corners):
        ghost = Ghost(cx, cy, i < num_chasers, maze['grid'], level)
        if i >= num_chasers:
            ghost.view_range = 0
        ghosts.append(ghost)
    return ghosts


ghosts = make_ghosts(maze_width, maze_height, level)


def set_game() -> None:
    """Reset all game state to a fresh start at level 0.

    Rebuilds the maze, pacgums, pacman, ghosts, and level timer used
    by the main loop. Called on startup and whenever the player
    returns to the main menu.
    """
    global maze_width, maze_height, maze, pacgums, pacman, level_time, ghosts
    maze_width, maze_height = get_level_config(level_index=0)
    maze = m.maze_loader((maze_width, maze_height), con['seed'])
    pacgums = m.place_pacgums((maze_width, maze_height), maze['grid'],
                              con['points_per_pacgum'],
                              con['points_per_super_pacgum'], con['pacgum'])
    pacman = pacman_setup.Pacman(
        maze['grid'], maze_width, maze_height, con['lives'])
    ghosts = make_ghosts(maze_width, maze_height, level)
    level_time = con['level_max_time']


def switch_level(level_index: int) -> None:
    """Advance to a new level, carrying over the player's score and lives.

    Rebuilds the maze, pacgums, and ghosts for the new level, resets
    the level timer, and re-centers the maze on screen.

    Args:
        level_index: 0-based index of the level to switch to.
    """
    global maze_width, maze_height, maze, pacgums, pacman
    global level_time, x_cor, ghosts
    maze_width, maze_height = get_level_config(level_index)
    x_cor = screen_width // 2 - maze_width * CELL_SIZE // 2
    maze = m.maze_loader((maze_width, maze_height), random.randint(0, 1000))
    pacgums = m.place_pacgums((maze_width, maze_height), maze['grid'],
                              con['points_per_pacgum'],
                              con['points_per_super_pacgum'], con['pacgum'])
    score = pacman.score
    lives = pacman.lives
    pacman = pacman_setup.Pacman(
        maze['grid'], maze_width, maze_height, con['lives'])
    pacman.score = score
    pacman.lives = lives
    ghosts = make_ghosts(maze_width, maze_height, level_index + 1)
    level_time = con['level_max_time']


def handle_playing(
    frame_tick_count: int, level_time: int, level_index: int,
    shadow_mode: bool, invincible: bool, speed_boost: bool,
    time_paused: bool, buttons: tuple[pygame.Rect, ...],
    player_name: str, game_state: str, pacman: pacman_setup.Pacman,
    ghost_tick_count: int, fraction: int
) -> tuple[tuple[pygame.Rect, ...], int, str]:
    """Advance and draw one frame of active gameplay.

    Updates ghosts, moves and animates pacman, resolves pacgum and
    ghost collisions, and handles level-complete/game-over transitions,
    then draws the current frame.

    Args:
        frame_tick_count: Tick within pacman's movement cycle (1-10).
        level_time: Seconds remaining in the current level.
        level_index: 0-based index of the current level.
        shadow_mode: Cheat flag that freezes ghost movement.
        invincible: Cheat flag that disables ghost collisions.
        speed_boost: Cheat flag that doubles pacman's move speed.
        time_paused: Cheat flag that pauses the level timer.
        buttons: Current cheat-mode panel button rects.
        player_name: Name entered so far, used if this frame ends the game.
        game_state: Current game state string.
        ghost_tick_count: Tick within the ghost movement cycle.

    Returns:
        (buttons, level_index, game_state), updated for the next frame.
    """
    for ghost in ghosts:
        if shadow_mode:
            ghost.prev_x, ghost.prev_y = ghost.x, ghost.y
        elif ghost_tick_count == 1:
            ghost.update(pacman.position)
    if frame_tick_count == 1:
        pacman.move()
        pacman.update_frame()
    pac_x = pacman.prev_position[0] + (
        pacman.position[0] - pacman.prev_position[0]
    ) * frame_tick_count / fraction
    pac_y = pacman.prev_position[1] + (
        pacman.position[1] - pacman.prev_position[1]
    ) * frame_tick_count / fraction
    for pacgum in pacgums:
        if not pacgum.eaten and (pac_x - pacgum.position[0] == 0) \
                and (pac_y - pacgum.position[1] == 0):
            pacman.score += pacgum.eat()
            if isinstance(pacgum, m.SuperPacgum):
                for ghost in ghosts:
                    ghost.make_edible()
    if all(pacgum.eaten for pacgum in pacgums):
        level_index += 1
        if level_index >= len(con['levels']):
            game_state = 'name_input'
            display_save_name(player_name, True, pacman.score)
            pygame.display.update()
            return (buttons, level_index, game_state)
        else:
            switch_level(level_index)
            buttons = display_cheat_mode(invincible, shadow_mode,
                                         speed_boost, time_paused)
    cycle = 30
    for ghost in ghosts:
        gx = ghost.prev_x + (ghost.x - ghost.prev_x) * ghost_tick_count / cycle
        gy = ghost.prev_y + (ghost.y - ghost.prev_y) * ghost_tick_count / cycle
        if abs(pac_x - gx) < .3 and abs(pac_y - gy) < .3:
            if ghost.state == "escape":
                ghost.get_eaten()
                pacman.score += con['points_per_ghost']
            elif ghost.state == "chasing" and not invincible:
                if not pacman.respawn():
                    game_state = "name_input"
                    display_save_name(player_name, False, pacman.score)
                    pygame.display.update()
                    return (buttons, level_index, game_state)
    m.draw_maze(screen, maze, x_cor, y_cor)
    m.draw_pacgums(screen, pacgums, x_cor, y_cor)
    pacman.draw_pacman(
        screen, frame_tick_count, x_cor, y_cor, speed_boost, fraction)
    maze_surface = screen.subsurface(
        (x_cor, y_cor, maze_width * CELL_SIZE, maze_height * CELL_SIZE))
    ghost_renderer.draw_ghosts(maze_surface, ghosts, ghost_tick_count, 30)
    display_timer(level_time)
    display_hearts(pacman.lives)
    display_level(level_index + 1)
    display_score(pacman.score)
    pygame.display.update()
    return (buttons, level_index, game_state)


def handle_submenu(
    player_name: str, buttuns: tuple[pygame.Rect, ...]
) -> tuple[pygame.Rect, ...]:
    """Redraw the pause submenu for the current frame.

    Args:
        player_name: Unused; kept for call-site symmetry with the
            other handle_* functions.
        buttuns: Unused; kept for call-site symmetry with the other
            handle_* functions.

    Returns:
        The submenu's button rects, for click handling.
    """
    buttons = display_submenu()
    pygame.display.update()
    return buttons


def button_collision(click_pos: tuple[int, int], butten: pygame.Rect) -> bool:
    start_x = butten.left
    end_x = butten.right
    start_y = butten.top
    end_y = butten.bottom
    x_in_bound = False
    y_in_bound = False
    if click_pos[0] in range(start_x, end_x + 1):
        x_in_bound = True
    if click_pos[1] in range(start_y, end_y + 1):
        y_in_bound = True
    return x_in_bound and y_in_bound


def handle_menu_buttons(
    buttons: tuple[pygame.Rect, ...], event: pygame.event.Event,
    game_state: str, invincible:  bool, shadow_mode: bool, speed_boost: bool,
    time_paused: bool
) -> tuple[tuple[pygame.Rect, ...], str]:
    """Handle a mouse click on the main menu, dispatching to the button.

    Args:
        buttons: Main menu button rects (play, instructions, high
            scores, exit) to test the click against.
        event: The MOUSEBUTTONDOWN event to handle.
        game_state: Current game state string.
        invincible: Current invincibility cheat toggle state.
        shadow_mode: Current shadow-mode cheat toggle state.
        speed_boost: Current speed-boost cheat toggle state.
        time_paused: Current pause-timer cheat toggle state.

    Returns:
        (buttons, game_state), updated for whichever screen was
        entered by the click.
    """
    if button_collision(event.pos, buttons[0]):
        game_state = 'playing'
        buttons = display_cheat_mode(
            invincible, shadow_mode, speed_boost, time_paused)
    elif button_collision(event.pos, buttons[1]):
        game_state = 'instructions'
        buttons = display_instructions()
    elif button_collision(event.pos, buttons[2]):
        game_state = 'high_score'
        buttons = display_high_scores(HIGHSCORE_PATH)
    elif button_collision(event.pos, buttons[3]):
        pygame.quit()
        sys.exit()
    return (buttons, game_state)


def handle_playing_buttons(
    buttons: tuple[pygame.Rect, ...], event: pygame.event.Event,
    level_index: int, invincible: bool, shadow_mode: bool,
    speed_boost: bool, time_paused: bool, game_state: str, player_name: str
) -> tuple[tuple[pygame.Rect, ...], int, bool, bool, bool, bool, str, str]:
    """Handle a mouse click on the in-game cheat-mode panel.

    Dispatches to skip level, add a life, or toggle one of the
    shadow/invincibility/pause/speed-boost cheats, based on which
    button rect the click landed in.

    Args:
        buttons: Cheat-mode panel button rects to test the click against.
        event: The MOUSEBUTTONDOWN event to handle.
        level_index: 0-based index of the current level.
        invincible: Current invincibility cheat toggle state.
        shadow_mode: Current shadow-mode cheat toggle state.
        speed_boost: Current speed-boost cheat toggle state.
        time_paused: Current pause-timer cheat toggle state.
        game_state: Current game state string.
        player_name: Name entered so far, used if skipping the last level.

    Returns:
        (buttons, level_index, invincible, shadow_mode, speed_boost,
        time_paused, game_state, player_name), updated per the cheat toggled.
    """
    if button_collision(event.pos, buttons[0]):
        level_index += 1
        if level_index >= len(con['levels']):
            game_state = 'name_input'
            display_save_name(player_name, True, pacman.score)
            return (buttons, level_index, invincible, shadow_mode,
                    speed_boost, time_paused, game_state, player_name)
        else:
            switch_level(level_index)
            buttons = display_cheat_mode(
                invincible, shadow_mode, speed_boost, time_paused)
    elif button_collision(event.pos, buttons[1]):
        pacman.lives += 1
        buttons = display_cheat_mode(
            invincible, shadow_mode, speed_boost, time_paused)
    elif button_collision(event.pos, buttons[2]):
        shadow_mode = not (shadow_mode)
        buttons = display_cheat_mode(
            invincible, shadow_mode, speed_boost, time_paused)
    elif button_collision(event.pos, buttons[3]):
        invincible = not (invincible)
        buttons = display_cheat_mode(
            invincible, shadow_mode, speed_boost, time_paused)
    elif button_collision(event.pos, buttons[4]):
        time_paused = not (time_paused)
        buttons = display_cheat_mode(
            invincible, shadow_mode, speed_boost, time_paused)
    elif button_collision(event.pos, buttons[5]):
        speed_boost = not (speed_boost)
        buttons = display_cheat_mode(
            invincible, shadow_mode, speed_boost, time_paused)
    return (buttons, level_index, invincible, shadow_mode,
            speed_boost, time_paused, game_state, player_name)


def handle_submenu_buttons(
    buttons: tuple[pygame.Rect, ...], event: pygame.event.Event,
    game_state: str, player_name: str, invincible: bool,
    shadow_mode: bool, speed_boost: bool, time_paused: bool
) -> tuple[tuple[pygame.Rect, ...], str]:
    """Handle a mouse click on the pause submenu, dispatching to the
    clicked button.

    Args:
        buttons: Submenu button rects (continue, save & quit) to test
            the click against.
        event: The MOUSEBUTTONDOWN event to handle.
        game_state: Current game state string.
        player_name: Name entered so far, used if saving and quitting.
        invincible: Current invincibility cheat toggle state.
        shadow_mode: Current shadow-mode cheat toggle state.
        speed_boost: Current speed-boost cheat toggle state.
        time_paused: Current pause-timer cheat toggle state.

    Returns:
        (buttons, game_state), updated for whichever option was clicked.
    """
    if button_collision(event.pos, buttons[0]):
        game_state = 'playing'
        buttons = display_cheat_mode(
            invincible, shadow_mode, speed_boost, time_paused)
    elif button_collision(event.pos, buttons[1]):
        game_state = 'name_input'
        display_save_name(player_name, False, pacman.score)
    return (buttons, game_state)


def main() -> None:
    """Run the game: set up the window and menu, then loop until quit.

    Owns the top-level state machine (menu/playing/submenu/name_input/
    instructions/high_score), the frame clock, and all pygame event
    dispatch (mouse clicks and keyboard input).
    """
    global level_time
    frame_tick_count = 0
    timer_tick_count = 0
    ghost_tick_count = 0
    fraction = 12
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
                invincible, speed_boost, time_paused, buttons, player_name,
                game_state, pacman, ghost_tick_count, fraction)
        elif game_state == 'submenu':
            buttons = handle_submenu(player_name, buttons)
        elif game_state == 'name_input':
            display_save_name(player_name,
                              level_index >= len(con['levels']),
                              pacman.score)
            pygame.display.update()
        if speed_boost:
            fraction = 9
        else:
            fraction = 12
        if frame_tick_count >= fraction:
            frame_tick_count = 0
        ghost_cycle_length = 30
        if ghost_tick_count >= ghost_cycle_length:
            ghost_tick_count = 0
        if timer_tick_count >= FPS:
            timer_tick_count = 0
            if not time_paused and game_state == 'playing':
                level_time -= 1
                if level_time <= 0:
                    game_state = "name_input"
                    display_save_name(player_name, False, pacman.score)
                    pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
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
                    if button_collision(event.pos, buttons[0]):
                        game_state = 'menu'
                        buttons = display_menu()
                elif game_state == 'high_score':
                    if button_collision(event.pos, buttons[0]):
                        game_state = 'menu'
                        buttons = display_menu()

            elif event.type == pygame.KEYDOWN and game_state == 'playing':
                if event.key in (pygame.K_UP, pygame.K_w):
                    pacman.nxt_dir = 'U'
                elif event.key in (pygame.K_DOWN, pygame.K_s):
                    pacman.nxt_dir = 'D'
                elif event.key in (pygame.K_LEFT, pygame.K_a):
                    pacman.nxt_dir = 'L'
                elif event.key in (pygame.K_RIGHT, pygame.K_d):
                    pacman.nxt_dir = 'R'
                elif event.key == pygame.K_ESCAPE:
                    game_state = 'submenu'
                    buttons = display_submenu()
                    pygame.display.update()
            elif event.type == pygame.KEYDOWN and game_state == 'name_input':
                if event.key == pygame.K_BACKSPACE:
                    player_name = player_name[:-1]
                elif (event.key in (pygame.K_KP_ENTER, pygame.K_RETURN)
                        and player_name != ''):
                    add_high_score(
                        HIGHSCORE_PATH, player_name,
                        pacman.score)
                    game_state = 'menu'
                    buttons = display_menu()
                else:
                    if (len(player_name) < 10
                            and (event.unicode.isalnum()
                                 or event.unicode == ' ')):
                        player_name += event.unicode


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('\nInterrupted. Goodbye!')
        pygame.quit()
        sys.exit(0)
    except Exception as e:
        print(f'Unexpected error: {e}')
        pygame.quit()
        sys.exit(1)
