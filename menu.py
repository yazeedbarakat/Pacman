import pygame
from high_scores_config import load_high_scores
import os

pygame.init()

pygame.font.init()
menu_font = pygame.font.Font('assets/fonts/Comfortaa-Regular.otf', 30)
name_font = pygame.font.Font('assets/fonts/Comfortaa-Bold.otf', 30)
yellow_button = pygame.transform.scale(
    pygame.image.load('assets/menu/yellow_button.png'), (426, 207))
purple_button = pygame.transform.scale(
    pygame.image.load('assets/menu/purple_button.png'), (490, 207))
menu = pygame.transform.scale(pygame.image.load('assets/menu/game_background.png'), (1920, 1080))
pacman = pygame.image.load('assets/menu/pac-man.png')
heart = pygame.transform.scale(pygame.image.load('assets/menu/heart.png'), (50, 50))
game_over = pygame.transform.scale(pygame.image.load('assets/menu/game_over.png'), (700, 500))
gif_frames: list[pygame.Surface] = []
gif_index = 0
gif_tick = 0

def init_gif():
    global gif_frames, gif_index
    frames = []
    for f in sorted(os.listdir('assets/menu/gif/')):
        frame = pygame.image.load(f'assets/menu/gif/{f}')
        frames.append(frame)
    gif_frames = frames
    gif_index = 0


def display_menu(
    screen: pygame.Surface, CELL_SIZE: int, WIDTH: int, HEIGHT: int
) -> tuple[pygame.Rect, pygame.Rect, pygame.Rect, pygame.Rect]:
    pacman_logo = pygame.image.load('assets/menu/Pac-Man-Logo.png')
    pacman_logo = pygame.transform.scale(pacman_logo, (500, 300))
    screen.blit(menu, (0, 0))
    screen.blit(pacman_logo, (WIDTH/2 - 250, HEIGHT/2 - 500))

    play_button = pygame.Rect(WIDTH/2 - 162, HEIGHT/2 + 10, 324, 56)
    pygame.draw.rect(screen, (0, 0, 0), play_button, border_radius=50)
    screen.blit(yellow_button, (WIDTH/2 - 213, HEIGHT/2 - 66))
    play_text = menu_font.render("PLAY", True, (255, 255, 255))
    screen.blit(play_text, (WIDTH/2 - 40, HEIGHT/2 + 20))

    instructions_button = pygame.Rect(WIDTH/2 - 162, HEIGHT/2 + 100, 324, 56)
    pygame.draw.rect(screen, (0, 0, 0), instructions_button, border_radius=50)
    screen.blit(yellow_button, (WIDTH/2 - 213, HEIGHT/2 + 24))
    instructions = menu_font.render("Instructions", True, (255, 255, 255))
    screen.blit(instructions, (WIDTH/2 - 90, HEIGHT/2 + 110))

    high_score_button = pygame.Rect(WIDTH/2 - 162, HEIGHT/2 + 190, 324, 56)
    pygame.draw.rect(screen, (0, 0, 0), high_score_button, border_radius=50)
    screen.blit(yellow_button, (WIDTH/2 - 213, HEIGHT/2 + 114))
    high_score = menu_font.render("High Scores", True, (255, 255, 255))
    screen.blit(high_score, (WIDTH/2 - 90, HEIGHT/2 + 200))

    exit_button = pygame.Rect(WIDTH/2 - 162, HEIGHT/2 + 280, 324, 56)
    pygame.draw.rect(screen, (0, 0, 0), exit_button, border_radius=50)
    screen.blit(yellow_button, (WIDTH/2 - 213, HEIGHT/2 + 204))
    exit_text = menu_font.render("EXIT", True, (255, 255, 255))
    screen.blit(exit_text, (WIDTH/2 - 40, HEIGHT/2 + 290))

    pygame.display.update()
    return (play_button, instructions_button, high_score_button, exit_button)


def display_instructions(
    screen: pygame.Surface, CELL_SIZE: int, WIDTH: int, HEIGHT: int
) -> tuple[pygame.Rect]:
    screen.blit(menu, (0, 0))
    arrows = pygame.transform.scale(pygame.image.load("assets/menu/arrows.png"),
                                    (260, 260))
    screen.blit(menu_font.render("- Eat all pacgums to clear the level", True, (255, 255, 255)),
                (WIDTH/2 - 400, HEIGHT/2 - 500))
    screen.blit(menu_font.render("- 3 lives, any mistake costs a life", True, (255, 255, 255)),
                (WIDTH/2 - 400, HEIGHT/2 - 440))
    screen.blit(menu_font.render("- Scoring values pulled from config", True, (255, 255, 255)),
                (WIDTH/2 - 400, HEIGHT/2 - 380))

    screen.blit(menu_font.render("Use the arrow keys to move", True, (255, 255, 255)),
                (WIDTH/2 - 200, HEIGHT/2 - 10))
    screen.blit(arrows, (WIDTH/2 - 130, HEIGHT/2 - 230))
    back_menu_button = pygame.Rect(WIDTH/2 - 160, HEIGHT/2 + 257, 320, 50)
    pygame.draw.rect(screen, (0, 0, 0), back_menu_button, border_radius=50)
    screen.blit(yellow_button, (WIDTH/2 - 213, HEIGHT/2 + 180))
    screen.blit(menu_font.render("Back to Menu", True, (255, 255, 255)),
                (WIDTH/2 - 105, HEIGHT/2 + 266))
    pygame.display.update()
    return (back_menu_button, )


def display_high_scores(
    screen: pygame.Surface, CELL_SIZE: int, WIDTH: int, HEIGHT: int,
    file_name: str
) -> tuple[pygame.Rect]:
    screen.blit(menu, (0, 0))
    title = name_font.render('TOP 10 PLAYERS', True,'green')
    screen.blit(title, (WIDTH/2 - 130, HEIGHT/2 - 500))
    sub_titles = name_font.render('SCORE                    NAME',
        True,'green')
    screen.blit(sub_titles, (WIDTH/2 - 180, HEIGHT/2 - 400))
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
        screen.blit(rank_text, (WIDTH/2 - 350, HEIGHT/2 - 300 + i * 50))
        score_text = menu_font.render(f"{score['score']}", True, color)
        screen.blit(score_text, (WIDTH/2 - 155, HEIGHT/2 - 300 + i * 50))
        name_text = name_font.render(f"{score['name']}", True, color)
        screen.blit(name_text, (WIDTH/2 + 140, HEIGHT/2 - 300 + i * 50))
    back_menu_button = pygame.Rect(WIDTH/2 - 160, HEIGHT/2 + 300, 320, 50)
    pygame.draw.rect(screen, 'black', back_menu_button, border_radius=50)
    screen.blit(yellow_button, (WIDTH/2 - 213, HEIGHT/2 + 223))
    screen.blit(menu_font.render("Back to Menu", True, 'white'),
                (WIDTH/2 - 105, HEIGHT/2 + 310))
    pygame.display.update()
    return (back_menu_button, )


def display_cheat_mode(
    screen: pygame.Surface, CELL_SIZE: int, WIDTH: int, HEIGHT: int,
    invincible:  bool, shadow_mode: bool, speed_boost: bool,
    time_paused: bool, unlimited_lives
) -> tuple[pygame.Rect, pygame.Rect, pygame.Rect, pygame.Rect, pygame.Rect, pygame.Rect]:
    screen.blit(menu, (0, 0))

    invincibility_button = pygame.Rect(WIDTH/2 + 520, HEIGHT/2 - 348, 364, 56)
    pygame.draw.rect(screen, 'black', invincibility_button, border_radius=50)
    screen.blit(purple_button, (WIDTH/2 + 460, HEIGHT/2 - 424))
    invincibility_text = menu_font.render("INVINCIBILITY", True, 'white')
    screen.blit(invincibility_text, (WIDTH/2 + 550, HEIGHT/2 - 335))
    if invincible:
        pygame.draw.rect(screen, 'green', pygame.Rect(
            WIDTH/2 + 840, HEIGHT/2 - 330, 20, 20), border_radius=50)
    else:
        pygame.draw.rect(screen, 'red', pygame.Rect(
            WIDTH/2 + 840, HEIGHT/2 - 330, 20, 20), border_radius=50)

    unlimited_lives_button = pygame.Rect(WIDTH/2 + 520, HEIGHT/2 - 264, 364, 56)
    pygame.draw.rect(screen, 'black', unlimited_lives_button, border_radius=50)
    screen.blit(purple_button, (WIDTH/2 + 460, HEIGHT/2 - 339))
    unlimited_lives_text = menu_font.render("UNLIMITED LIVES", True, 'white')
    screen.blit(unlimited_lives_text, (WIDTH/2 + 550, HEIGHT/2 - 250))
    if unlimited_lives:
        pygame.draw.rect(screen, 'green', pygame.Rect(
            WIDTH/2 + 840, HEIGHT/2 - 245, 20, 20), border_radius=50)
    else:
        pygame.draw.rect(screen, 'red', pygame.Rect(
            WIDTH/2 + 840, HEIGHT/2 - 245, 20, 20), border_radius=50)

    shadow_button = pygame.Rect(WIDTH/2 + 520, HEIGHT/2 - 180, 364, 56)
    pygame.draw.rect(screen, 'black', shadow_button, border_radius=50)
    screen.blit(purple_button, (WIDTH/2 + 460, HEIGHT/2 - 257))
    shadow_text = menu_font.render("SHADOW MODE", True, 'white')
    screen.blit(shadow_text, (WIDTH/2 + 550, HEIGHT/2 - 168))
    if shadow_mode:
        pygame.draw.rect(screen, 'green', pygame.Rect(
            WIDTH/2 + 840, HEIGHT/2 - 162, 20, 20), border_radius=50)
    else:
        pygame.draw.rect(screen, 'red', pygame.Rect(
            WIDTH/2 + 840, HEIGHT/2 - 162, 20, 20), border_radius=50)

    skip_level_button = pygame.Rect(WIDTH/2 + 520, HEIGHT/2 - 100, 364, 56)
    pygame.draw.rect(screen, 'black', skip_level_button, border_radius=50)
    screen.blit(purple_button, (WIDTH/2 + 460, HEIGHT/2 - 175))
    skip_level_text = menu_font.render("SKIP LEVEL", True, 'white')
    screen.blit(skip_level_text, (WIDTH/2 + 550, HEIGHT/2 - 85))

    pause_timer_button = pygame.Rect(WIDTH/2 + 520, HEIGHT/2 - 20, 364, 56)
    pygame.draw.rect(screen, 'black', pause_timer_button, border_radius=50)
    screen.blit(purple_button, (WIDTH/2 + 460, HEIGHT/2 - 95))
    pause_timer_text = menu_font.render("PAUSE TIMER", True, 'white')
    screen.blit(pause_timer_text, (WIDTH/2 + 550, HEIGHT/2 - 5))
    if time_paused:
        pygame.draw.rect(screen, 'green', pygame.Rect(
            WIDTH/2 + 840, HEIGHT/2, 20, 20), border_radius=50)
    else:
        pygame.draw.rect(screen, 'red', pygame.Rect(
            WIDTH/2 + 840, HEIGHT/2, 20, 20), border_radius=50)

    speed_boost_button = pygame.Rect(WIDTH/2 + 520, HEIGHT/2 + 64, 364, 56)
    pygame.draw.rect(screen, 'black', speed_boost_button, border_radius=50)
    screen.blit(purple_button, (WIDTH/2 + 460, HEIGHT/2 - 12))
    speed_boost_text = menu_font.render("SPEED BOOST", True, 'white')
    screen.blit(speed_boost_text, (WIDTH/2 + 550, HEIGHT/2 + 77))
    if speed_boost:
        pygame.draw.rect(screen, 'green', pygame.Rect(
            WIDTH/2 + 840, HEIGHT/2 + 82, 20, 20), border_radius=50)
    else:
        pygame.draw.rect(screen, 'red', pygame.Rect(
            WIDTH/2 + 840, HEIGHT/2 + 82, 20, 20), border_radius=50)

    return (invincibility_button, unlimited_lives_button, shadow_button,
            skip_level_button, pause_timer_button, speed_boost_button)


def display_submenu(
    screen: pygame.Surface, CELL_SIZE: int, WIDTH: int, HEIGHT: int
) -> tuple[pygame.Rect, pygame.Rect]:
    screen.blit(menu, (0, 0))
    screen.blit(pacman, (WIDTH/2 - 270, HEIGHT/2 - 500))

    # text_surface = menu_font.render()

    continue_button = pygame.Rect(WIDTH/2 - 162, HEIGHT/2 + 110, 324, 56)
    pygame.draw.rect(screen, 'black', continue_button, border_radius=50)
    screen.blit(yellow_button, (WIDTH/2 - 213, HEIGHT/2 + 34))
    continue_text = menu_font.render("continue", True, 'white')
    screen.blit(continue_text, (WIDTH/2 - 70, HEIGHT/2 + 120))

    save_quit_button = pygame.Rect(WIDTH/2 - 162, HEIGHT/2 + 200, 324, 56)
    pygame.draw.rect(screen, 'black', save_quit_button, border_radius=50)
    screen.blit(yellow_button, (WIDTH/2 - 213, HEIGHT/2 + 124))
    save_quit_text = menu_font.render("Save and Quit", True, 'white')
    screen.blit(save_quit_text, (WIDTH/2 - 110, HEIGHT/2 + 213))
    return (continue_button, save_quit_button)


def display_save_name(player_name: str, screen: pygame.Surface,
                      screen_width: int, screen_height: int) -> None:
    global gif_index, gif_tick
    screen.blit(menu, (0, 0))
    screen.blit(game_over, (screen_width/2 - 350, screen_height/2 - 650))
    frame = pygame.transform.scale(gif_frames[gif_index], (500, 300))
    screen.blit(frame, (screen_width//2 - 250, screen_height//2 + 200))
    gif_tick += 1
    if gif_tick % 3 == 0:
        gif_index = (gif_index + 1) % len(gif_frames)
    if player_name == '':
        name_rect = pygame.Rect(screen_width/2 - 155, screen_height/2 + 14, 340, 50)
        pygame.draw.rect(screen, 'yellow', name_rect, 2)
        text_surface = name_font.render('enter your name', True, 'grey')
        screen.blit(text_surface, (screen_width/2 - 125, screen_height/2 + 20))
    else:
        enter = name_font.render('press enter',  True, 'white')
        screen.blit(enter, (screen_width/2 - 100, screen_height/2 + 80))
        name_rect = pygame.Rect(screen_width/2 - 35 - len(player_name) * 14,
                                screen_height/2 + 14, len(player_name) * 28, 50)
        pygame.draw.rect(screen, 'yellow', name_rect, 2)
        text_surface = name_font.render(player_name, True, 'white')
        screen.blit(text_surface, (screen_width/2 - 30 -
                                   len(player_name) * 10, screen_height/2 + 20))
    pygame.display.update()
