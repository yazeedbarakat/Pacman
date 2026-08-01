import pygame
from sys import exit

def show_main_menu(screen, screen_width, screen_height) -> str:

    title_font = pygame.font.Font(None, 100)
    menu_font = pygame.font.Font(None, 60)
    
    options = ["Start Game", "View Highscores", "Exit"]
    selected_index = 0
    
    clock = pygame.time.Clock()
    
    while True:

        screen.fill('black')

        title_text = title_font.render("PAC-MAN", True, 'yellow')
        screen.blit(title_text, (screen_width // 2 - title_text.get_width() // 2, 150))

        for i, option in enumerate(options):
            color = 'yellow' if i == selected_index else 'white'
            text = menu_font.render(option, True, color)
            
            x = screen_width // 2 - text.get_width() // 2
            y = 350 + (i * 80)
            screen.blit(text, (x, y))
            
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected_index = (selected_index - 1) % len(options)
                elif event.key == pygame.K_DOWN:
                    selected_index = (selected_index + 1) % len(options)
                elif event.key == pygame.K_RETURN:
                    if selected_index == 0:
                        return "START"
                    elif selected_index == 1:
                        return "HIGHSCORES"
                    elif selected_index == 2:
                        pygame.quit()
                        exit()
                        
        clock.tick(60)
