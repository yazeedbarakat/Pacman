import pygame
from high_scores_config import load_high_scores
import os

pygame.init()

pygame.font.init()
menu_font = pygame.font.Font('assets/fonts/Comfortaa-Regular.otf', 30)
name_font = pygame.font.Font('assets/fonts/Comfortaa-Bold.otf', 30)
level_font = pygame.font.Font('assets/fonts/Montserrat-Bold.otf', 45)
timer_font = pygame.font.Font('assets/fonts/Montserrat-Bold.otf', 40)

yellow_button = pygame.transform.scale(
    pygame.image.load('assets/menu/yellow_button.png'), (426, 207))
purple_button = pygame.transform.scale(
    pygame.image.load('assets/menu/purple_button.png'), (490, 207))
background = pygame.transform.scale(
    pygame.image.load('assets/menu/game_background.png'), (1920, 1080))
pacman = pygame.image.load('assets/menu/pac-man.png')
heart = pygame.transform.scale(pygame.image.load('assets/menu/heart.png'), (60, 60))
game_over = pygame.transform.scale(pygame.image.load('assets/menu/game_over.png'), (700, 500))
you_win = pygame.transform.scale(pygame.image.load('assets/menu/you_win.png'), (700, 500))
gif_frames: list[pygame.Surface] = []
gif_index = 0
gif_tick = 0
screen: pygame.Surface = pygame.Surface((0, 0))
width: int = 0
height: int = 0


def init_gif() -> None:
    """Load every frame of the game-over gif from disk, sorted by filename."""
    global gif_frames, gif_index
    frames = []
    for f in sorted(os.listdir('assets/menu/gif/')):
        frame = pygame.image.load(f'assets/menu/gif/{f}')
        frames.append(frame)
    gif_frames = frames
    gif_index = 0


def init_display(game_screen: pygame.Surface, screen_width: int, screen_height: int) -> None:
    """Bind this module's drawing target and dimensions to the game's screen.

    Must be called before any display_* function, since they all draw
    onto the module-level `screen` set here.

    Args:
        game_screen: The pygame display surface to draw onto.
        screen_width: Width of the screen in pixels.
        screen_height: Height of the screen in pixels.
    """
    global screen, width, height
    screen = game_screen
    width = screen_width
    height = screen_height


def create_menu_button(
    rect_y_offset: int, icon_y_offset: int,
    text: str, text_x_offset: int, text_y_offset: int
) -> pygame.Rect:
    """Draw one yellow main-menu button with a label and return its clickable rect.

    Args:
        rect_y_offset: Vertical offset of the button rect from screen center.
        icon_y_offset: Vertical offset of the button icon from screen center.
        text: Label text to render on the button.
        text_x_offset: Horizontal offset of the label from screen center.
        text_y_offset: Vertical offset of the label from screen center.

    Returns:
        The button's clickable rect, for collision testing on click.
    """
    button = pygame.Rect(width/2 - 162, height/2 + rect_y_offset, 324, 56)
    pygame.draw.rect(screen, 'black', button, border_radius=50)
    screen.blit(yellow_button, (width/2 - 213, height/2 + icon_y_offset))
    display_text = menu_font.render(text, True, 'white')
    screen.blit(display_text, (width/2 + text_x_offset, height/2 + text_y_offset))
    return button


def display_menu() -> tuple[pygame.Rect, pygame.Rect, pygame.Rect, pygame.Rect]:
    """Draw the main menu and return its buttons' clickable rects.

    Returns:
        (play_button, instructions_button, high_score_button, exit_button).
    """
    pacman_logo = pygame.image.load('assets/menu/Pac-Man-Logo.png')
    pacman_logo = pygame.transform.scale(pacman_logo, (500, 300))
    screen.blit(background, (0, 0))
    screen.blit(pacman_logo, (width/2 - 250, height/2 - 500))

    play_button = create_menu_button(10, -66, "PLAY", -40, 20)

    instructions_button = create_menu_button(100, 24, "INSTRUCTIONS", -115, 110)

    high_score_button = create_menu_button(190, 114, "HIGH SCORES", -115, 200)

    exit_button = create_menu_button(280, 204, "EXIT", -40, 290)

    pygame.display.update()
    return (play_button, instructions_button, high_score_button, exit_button)


def display_instructions() -> tuple[pygame.Rect]:
    """Draw the instructions screen and return its back-to-menu button rect.

    Returns:
        A 1-tuple containing the back-to-menu button's clickable rect.
    """
    screen.blit(background, (0, 0))
    arrows = pygame.transform.scale(pygame.image.load("assets/menu/arrows.png"),
                                    (260, 260))
    screen.blit(menu_font.render("- Eat all pacgums to clear the level", True, 'white'),
                (width/2 - 400, height/2 - 500))
    screen.blit(menu_font.render("- 3 lives, any mistake costs a life", True, 'white'),
                (width/2 - 400, height/2 - 440))
    screen.blit(menu_font.render("- Scoring values pulled from config", True, 'white'),
                (width/2 - 400, height/2 - 380))

    screen.blit(menu_font.render("Use the arrow keys to move", True, 'white'),
                (width/2 - 200, height/2 - 10))
    screen.blit(arrows, (width/2 - 130, height/2 - 230))
    back_menu_button = pygame.Rect(width/2 - 160, height/2 + 257, 320, 50)
    pygame.draw.rect(screen, 'black', back_menu_button, border_radius=50)
    screen.blit(yellow_button, (width/2 - 213, height/2 + 180))
    screen.blit(menu_font.render("Back to Menu", True, 'white'),
                (width/2 - 105, height/2 + 266))
    pygame.display.update()
    return (back_menu_button, )


def display_high_scores(file_name: str) -> tuple[pygame.Rect]:
    """Draw the top-10 high score table and return its back-to-menu button rect.

    Args:
        file_name: Path to the JSON high score file to load and display.

    Returns:
        A 1-tuple containing the back-to-menu button's clickable rect.
    """
    screen.blit(background, (0, 0))
    title = name_font.render('TOP 10 PLAYERS', True, 'green')
    screen.blit(title, (width/2 - 130, height/2 - 500))
    sub_titles = name_font.render('SCORE                    NAME',
                                  True, 'green')
    screen.blit(sub_titles, (width/2 - 180, height/2 - 400))
    high_scores = load_high_scores(file_name)
    high_scores = sorted(high_scores, key=lambda x: x['score'], reverse=True)
    for i, score in enumerate(high_scores):
        if i == 0:
            color = 'red'
        elif i in (1, 2):
            color = 'orange'
        elif i in (3, 4):
            color = 'yellow'
        else:
            color = 'white'
        rank_text = name_font.render(f"{i + 1}", True, color)
        screen.blit(rank_text, (width/2 - 350, height/2 - 300 + i * 50))
        score_text = menu_font.render(f"{score['score']}", True, color)
        screen.blit(score_text, (width/2 - 155, height/2 - 300 + i * 50))
        name_text = name_font.render(f"{score['name']}", True, color)
        screen.blit(name_text, (width/2 + 140, height/2 - 300 + i * 50))
    back_menu_button = pygame.Rect(width/2 - 160, height/2 + 300, 320, 50)
    pygame.draw.rect(screen, 'black', back_menu_button, border_radius=50)
    screen.blit(yellow_button, (width/2 - 213, height/2 + 223))
    screen.blit(menu_font.render("Back to Menu", True, 'white'),
                (width/2 - 105, height/2 + 310))
    pygame.display.update()
    return (back_menu_button, )


def create_cheat_mode_button(
    mode: bool | None, rect_y_offset: int, icon_y_offset: int,
    text: str, text_y_offset: int, switch_y_offset: int = 0
) -> pygame.Rect:
    """Draw one purple cheat-mode button, with an on/off dot if `mode` is given.

    Args:
        mode: Current toggle state to show as a green/red dot, or
            None for a button with no on/off indicator (e.g. skip level).
        rect_y_offset: Vertical offset of the button rect from screen center.
        icon_y_offset: Vertical offset of the button icon from screen center.
        text: Label text to render on the button.
        text_y_offset: Vertical offset of the label from screen center.
        switch_y_offset: Vertical offset of the on/off dot from screen center.

    Returns:
        The button's clickable rect, for collision testing on click.
    """
    button = pygame.Rect(width/2 + 520, height/2 + rect_y_offset, 364, 56)
    pygame.draw.rect(screen, 'black', button, border_radius=50)
    screen.blit(purple_button, (width/2 + 460, height/2 + icon_y_offset))
    display_text = menu_font.render(text, True, 'white')
    screen.blit(display_text, (width/2 + 550, height/2 + text_y_offset))
    if mode is not None:
        if mode:
            pygame.draw.rect(screen, 'green', pygame.Rect(
                width/2 + 840, height/2 + switch_y_offset, 20, 20), border_radius=50)
        else:
            pygame.draw.rect(screen, 'red', pygame.Rect(
                width/2 + 840, height/2 + switch_y_offset, 20, 20), border_radius=50)
    return button


def display_cheat_mode(
    invincible: bool, shadow_mode: bool, speed_boost: bool, time_paused: bool
) -> tuple[
    pygame.Rect, pygame.Rect, pygame.Rect, pygame.Rect, pygame.Rect, pygame.Rect
]:
    """Draw the cheat-mode panel and return its buttons' clickable rects.

    Args:
        invincible: Current invincibility toggle state.
        shadow_mode: Current shadow-mode (ghosts frozen) toggle state.
        speed_boost: Current speed-boost toggle state.
        time_paused: Current pause-timer toggle state.

    Returns:
        (skip_level_button, extra_lives_button, shadow_button,
        invincibility_button, pause_timer_button, speed_boost_button).
    """
    screen.blit(background, (0, 0))

    skip_level_button = create_cheat_mode_button(None, -348, -424, "SKIP LEVEL", -335)

    extra_lives_button = create_cheat_mode_button(None, -264, -339, "ADD EXTRA LIVE", -250)

    shadow_button = create_cheat_mode_button(shadow_mode, -180, -257, "SHADOW MODE", -168, -162)

    invincibility_button = create_cheat_mode_button(
        invincible, -100, -175, "INVINCIBILITY", -85, -80)

    pause_timer_button = create_cheat_mode_button(time_paused, -20, -95, "PAUSE TIMER", -5, -1)

    speed_boost_button = create_cheat_mode_button(speed_boost, 64, -12, "SPEED BOOST", 77, 82)

    return (skip_level_button, extra_lives_button, shadow_button,
            invincibility_button, pause_timer_button, speed_boost_button)


def display_submenu() -> tuple[pygame.Rect, pygame.Rect]:
    """Draw the pause submenu and return its buttons' clickable rects.

    Returns:
        (continue_button, save_quit_button).
    """
    screen.blit(background, (0, 0))
    screen.blit(pacman, (width/2 - 270, height/2 - 500))

    continue_button = pygame.Rect(width/2 - 162, height/2 + 110, 324, 56)
    pygame.draw.rect(screen, 'black', continue_button, border_radius=50)
    screen.blit(yellow_button, (width/2 - 213, height/2 + 34))
    continue_text = menu_font.render("continue", True, 'white')
    screen.blit(continue_text, (width/2 - 70, height/2 + 120))

    save_quit_button = pygame.Rect(width/2 - 162, height/2 + 200, 324, 56)
    pygame.draw.rect(screen, 'black', save_quit_button, border_radius=50)
    screen.blit(yellow_button, (width/2 - 213, height/2 + 124))
    save_quit_text = menu_font.render("Save and Quit", True, 'white')
    screen.blit(save_quit_text, (width/2 - 110, height/2 + 213))
    return (continue_button, save_quit_button)


def display_save_name(player_name: str, game_won: bool) -> None:
    """Draw the game-over screen with its animated gif and name-entry field.

    Args:
        player_name: Name typed so far; an empty string shows a
            placeholder prompt instead of the entry box.
    """
    global gif_index, gif_tick
    screen.blit(background, (0, 0))
    if game_won:
         screen.blit(you_win, (width/2 - 380, height/2 - 650))
    else:
        screen.blit(game_over, (width/2 - 350, height/2 - 650))
    frame = pygame.transform.scale(gif_frames[gif_index], (500, 300))
    screen.blit(frame, (width//2 - 250, height//2 + 200))
    gif_tick += 1
    if gif_tick % 3 == 0:
        gif_index = (gif_index + 1) % len(gif_frames)
    if player_name == '':
        name_rect = pygame.Rect(width/2 - 155, height/2 + 14, 340, 50)
        pygame.draw.rect(screen, 'yellow', name_rect, 2)
        text_surface = name_font.render('enter your name', True, 'grey')
        screen.blit(text_surface, (width/2 - 125, height/2 + 20))
    else:
        enter = name_font.render('press enter',  True, 'white')
        screen.blit(enter, (width/2 - 100, height/2 + 80))
        name_rect = pygame.Rect(width/2 - 35 - len(player_name) * 14,
                                height/2 + 14, len(player_name) * 28, 50)
        pygame.draw.rect(screen, 'yellow', name_rect, 2)
        text_surface = name_font.render(player_name, True, 'white')
        screen.blit(text_surface, (width/2 - 30 -
                                   len(player_name) * 10, height/2 + 20))
    pygame.display.update()


def display_level(level: int) -> None:
    """Redraw the level number in the HUD.

    Args:
        level: 1-based level number to display.
    """
    pygame.draw.rect(screen, 'black', pygame.Rect(
        width/2 + 200, height/2 - 500, 190, 50))
    level_text = level_font.render(f'level: {level}', True, 'white')
    screen.blit(level_text, (width/2 + 200, height/2 - 500))


def display_timer(time: int) -> None:
    """Redraw the remaining time in the HUD as mm:ss.

    Args:
        time: Seconds remaining in the level.
    """
    minutes = time//60
    minutes_str = '0' + str(minutes) if minutes // 10 == 0 else str(minutes)
    seconds = time % 60
    seconds_str = '0' + str(seconds) if seconds // 10 == 0 else str(seconds)
    pygame.draw.rect(screen, 'black', pygame.Rect(
        width/2 - 80, height/2 - 500, 130, 50))
    time_text = timer_font.render(f"{minutes_str}:{seconds_str}", True, 'white')
    screen.blit(time_text, (width/2 - 75, height/2 - 500))


def display_hearts(lives: int) -> None:
    """Redraw the lives HUD as up to 3 heart icons.

    Args:
        lives: Current number of lives remaining (capped at 3 icons).
    """
    pygame.draw.rect(screen, 'black', pygame.Rect(
        width/2 - 350, height/2 - 500, 120, 50))
    hearts = 3 if lives >= 3 else lives
    for i in range(hearts):
        screen.blit(heart, (width/2 - 360 + i * 40, height/2 - 505))
