import pygame
from sys import exit


def display_menu(screen, CELL_SIZE, WIDTH, HEIGHT):
    FONT = pygame.font.Font(None, 50)
    pacman = pygame.transform.scale(pygame.image.load('assets/menu/pacman.png'),
        (CELL_SIZE * 7, CELL_SIZE * 10))
    menu = pygame.transform.scale(pygame.image.load('assets/menu/game_background.png'), (WIDTH, HEIGHT))
    screen.blit(menu, (0, 0))

    start_button = pygame.Rect(WIDTH/2 - 869, HEIGHT/2 - 263, 326, 57)
    pygame.draw.rect(screen, (0, 0, 0), start_button, border_radius=5)
    start_game = FONT.render("Start Game", True, (255, 255, 255))
    screen.blit(start_game, (WIDTH/2 - 100, HEIGHT/2 - 85))

    high_score_button = pygame.Surface((269, 63), pygame.SRCALPHA)
    high_score_button.fill((0, 0, 20, 0))
    screen.blit(high_score_button, (WIDTH/2 - 869, HEIGHT/2 - 200))
    high_score = FONT.render("High Scores", True, (255, 255, 255))
    screen.blit(high_score, (WIDTH/2 - 100, HEIGHT/2 + 7))

    levels_button = pygame.Rect(WIDTH/2 - 133, HEIGHT/2 + 84, 269, 63)
    pygame.draw.rect(screen, (80, 80, 80), levels_button, border_radius=7)
    levels_text = FONT.render("Game Levels", True, (255, 255, 255))
    screen.blit(levels_text, (WIDTH/2 - 100, HEIGHT/2 + 98))

    exit_button = pygame.Rect(WIDTH/2 - 133, HEIGHT/2 + 176, 269, 63)
    pygame.draw.rect(screen, (80, 80, 80), exit_button, border_radius=7)
    exit_text = FONT.render("Exit Game", True, (255, 255, 255))
    screen.blit(exit_text, (WIDTH/2 - 100, HEIGHT/2 + 190))
    pygame.display.update()
    return (start_button, high_score, levels_button, exit_button)
