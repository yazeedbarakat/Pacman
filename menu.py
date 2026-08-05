import pygame
from sys import exit


CELL_SIZE = 30
WIDTH = 1000
HEIGHT = 800
pygame.init()
FONT = pygame.font.Font(None, 50)
s = pygame.display.set_mode((WIDTH, HEIGHT))
pacman = pygame.transform.scale(pygame.image.load('assets/menu/pacman.png'),
    (CELL_SIZE * 7, CELL_SIZE * 10))
menu = pygame.transform.scale(pygame.image.load('assets/menu/game_menu.png'), (WIDTH, HEIGHT))
s.blit(menu, (0, 0))
start_button = pygame.Rect(WIDTH/2 - 133, HEIGHT/2 - 101, 269, 63)
pygame.draw.rect(s, (80, 80, 80), start_button, border_radius=7)
start_game = FONT.render("Start Game", True, (255, 255, 255))
s.blit(start_game, (WIDTH/2 - 90, HEIGHT/2 - 85))
pygame.draw.rect(s, (80, 80, 80), (WIDTH/2 - 133, HEIGHT/2 - 9, 269, 63), border_radius=7)
pygame.draw.rect(s, (80, 80, 80), (WIDTH/2 - 133, HEIGHT/2 + 84, 269, 63), border_radius=7)
pygame.draw.rect(s, (80, 80, 80), (WIDTH/2 - 133, HEIGHT/2 + 176, 269, 63), border_radius=7)
pygame.display.update()

while(True):
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            if start_button.collidepoint(event.pos):
                continue
