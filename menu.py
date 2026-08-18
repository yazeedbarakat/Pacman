import pygame
from sys import exit

pygame.font.init()
menu_font = pygame.font.SysFont('comfortaa', 30)
yellow_button = pygame.transform.scale(pygame.image.load('assets/menu/yellow_button.png'), (426, 207))
purple_button = pygame.transform.scale(pygame.image.load('assets/menu/purple_button.png'), (450, 207))

def display_menu(screen, CELL_SIZE, WIDTH, HEIGHT):
    pacman = pygame.transform.scale(pygame.image.load('assets/menu/pacman.png'),
        (CELL_SIZE * 7, CELL_SIZE * 10))
    menu = pygame.transform.scale(pygame.image.load('assets/menu/game_background.png'), (WIDTH, HEIGHT))
    screen.blit(menu, (0, 0))

    play_button = pygame.Rect(WIDTH/2 - 869, HEIGHT/2 - 263, 324, 56)
    pygame.draw.rect(screen, (0, 0, 0), play_button, border_radius=50)
    screen.blit(yellow_button, (WIDTH/2 - 920, HEIGHT/2 - 339))
    start_game = menu_font.render("PLAY", True, (255, 255, 255))
    screen.blit(start_game, (WIDTH/2 - 800, HEIGHT/2 - 250))

    instructions_button = pygame.Rect(WIDTH/2 - 869, HEIGHT/2 - 181, 324, 56)
    pygame.draw.rect(screen, (0, 0, 0), instructions_button, border_radius=50)
    screen.blit(yellow_button, (WIDTH/2 - 920, HEIGHT/2 - 257))
    instructions = menu_font.render("Instructions", True, (255, 255, 255))
    screen.blit(instructions, (WIDTH/2 - 800, HEIGHT/2 - 172))

    high_score_button = pygame.Rect(WIDTH/2 - 869, HEIGHT/2 - 99, 324, 56)
    pygame.draw.rect(screen, (0, 0, 0), high_score_button, border_radius=50)
    screen.blit(yellow_button, (WIDTH/2 - 920, HEIGHT/2 - 175))
    high_score = menu_font.render("High Scores", True, (255, 255, 255))
    screen.blit(high_score, (WIDTH/2 - 800, HEIGHT/2 - 90))

    exit_button = pygame.Rect(WIDTH/2 - 869, HEIGHT/2 - 17, 324, 56)
    pygame.draw.rect(screen, (0, 0, 0), exit_button, border_radius=50)
    screen.blit(yellow_button, (WIDTH/2 - 920, HEIGHT/2 - 93))
    exit_text = menu_font.render("EXIT", True, (255, 255, 255))
    screen.blit(exit_text, (WIDTH/2 - 800, HEIGHT/2 - 4))

    pygame.display.update()
    return (play_button, instructions_button, high_score_button, exit_button)


def display_instructions(screen, CELL_SIZE, WIDTH, HEIGHT):
    arrows = pygame.transform.scale(pygame.image.load("assets/menu/arrows.png"),
        (260, 260))
    screen.blit(menu_font.render("- Eat all pacgums to clear the level", True, (255, 255, 255)),
        (WIDTH/2 - 400, HEIGHT/2 - 500))
    screen.blit(menu_font.render("- 3 lives, any mistake costs a life", True, (255, 255, 255)),
        (WIDTH/2 - 400, HEIGHT/2 - 440))
    screen.blit(menu_font.render("- Scoring values pulled from config", True, (255, 255, 255)),
        (WIDTH/2 - 400, HEIGHT/2 - 380))

    screen.blit(menu_font.render("Use the arrow keys to move", True, (255, 255, 255)),
        (WIDTH/2 - 200, HEIGHT/2 + 120))
    screen.blit(arrows, (WIDTH/2 - 130, HEIGHT/2 + 130))
    pygame.display.update()

def display_cheat_mode(screen, CELL_SIZE, WIDTH, HEIGHT):
    screen.blit(menu_font.render("CHEAT MODE", True, (255, 255, 255)),
        (WIDTH - 300, HEIGHT/2 - 380))

    unlimited_lives_button = pygame.Rect(WIDTH/2 + 490, HEIGHT/2 - 339, 324, 56)
    pygame.draw.rect(screen, (0, 255, 0), unlimited_lives_button, border_radius=50)
    screen.blit(purple_button, (WIDTH/2 + 460, HEIGHT/2 - 339))
    unlimited_lives_text = menu_font.render("UNLIMITED LIVES", True, (255, 255, 255))
    screen.blit(unlimited_lives_text, (WIDTH/2 + 550, HEIGHT/2 - 250))

    shadow_button = pygame.Rect(WIDTH/2 + 490, HEIGHT/2 - 180, 324, 56)
    pygame.draw.rect(screen, (255, 0, 0), shadow_button, border_radius=50)
    screen.blit(purple_button, (WIDTH/2 + 460, HEIGHT/2 - 257))
    shadow_text = menu_font.render("SHADOW MODE", True, (0, 0, 0))
    screen.blit(shadow_text, (WIDTH/2 + 550, HEIGHT/2 - 150))
