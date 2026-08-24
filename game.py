from os import name
from sys import exit
import ghost_renderer
from ghost import Ghost  # TEMP-GHOST
from high_scores_config import add_high_score
import player_setup
import  pygame
import maze as m
from config_parser import read_config
from menu import display_menu, display_instructions, display_cheat_mode, \
display_submenu, display_high_scores

con = read_config('config.json')
print(con)
pygame.font.init()
timer_font = pygame.font.SysFont('sourcecodepro', 40, bold=True)
level_font = pygame.font.SysFont('montserrat', 45, bold=True)
name_font = pygame.font.SysFont('comfortaa', 50, bold=True)

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
heart = pygame.transform.scale(pygame.image.load('assets/menu/heart.png'), (60, 60))

pygame.init()
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Pacman')
clock = pygame.time.Clock()
maze = m.maze_loader((maze_width, maze_height), 42)
pacgums = m.place_pacgums((maze_width, maze_height), maze['grid'])
player = player_setup.Player(maze['grid'], maze_width, maze_height)
ghost_renderer = ghost_renderer.GhostRenderer(cell_size=CELL_SIZE)  # TEMP-GHOST: was called with wrong args
level = 0
def make_ghosts(width, height, level):  # TEMP-GHOST
    corners = [(0, 0), (width - 1, 0), (0, height - 1), (width - 1, height - 1)]
    return [Ghost(cx, cy, 1, maze['grid'], level) for cx, cy in corners]

ghosts = make_ghosts(maze_width, maze_height, level)  # TEMP-GHOST

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
    ghosts = make_ghosts(maze_width, maze_height, level_index + 1)  # TEMP-GHOST
    level_time = con['level_max_time']

def display_hearts(lives: int):
    pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(screen_width/2 - 350, screen_height/2 - 500, 120, 50))
    hearts = 3 if lives >= 3 else lives
    for i in range(hearts):
        screen.blit(heart, (screen_width/2 - 360 + i * 40, screen_height/2 - 505))

def display_level(level: int):
    pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(screen_width/2 + 200, screen_height/2 - 500, 190, 50))
    level_text = level_font.render(f'level: {level}', True, (255, 255, 255))
    screen.blit(level_text, (screen_width/2 + 200, screen_height/2 - 500))

def display_timer(time):
    minutes = time//60
    if minutes // 10 == 0:
        minutes = '0' + str(minutes)
    seconds = time % 60
    if seconds // 10 == 0:
        seconds = '0' + str(seconds)
    pygame.draw.rect(screen, (0, 0, 0),pygame.Rect(screen_width/2- 80, screen_height/2 - 500, 130, 50))
    time_text = timer_font.render(f"{minutes}:{seconds}", True, (255, 255, 255))
    screen.blit(time_text, (screen_width/2 - 75, screen_height/2 - 500))

def main() -> None:
    global level_time
    frame_tick_count = 0
    timer_tick_count = 0
    time_paused = False
    level_index = 0
    game_state = 'menu'
    cheat_mode_buttons = display_cheat_mode(screen, CELL_SIZE, screen_width, screen_height)
    invincible = False
    shadow_mode = False
    speed_boost = False
    player_name = ''
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
                        if isinstance(pacgum, m.SuperPacgum):  # TEMP-GHOST
                            for ghost in ghosts:  # TEMP-GHOST
                                ghost.make_edible()  # TEMP-GHOST
                for ghost in ghosts:  # TEMP-GHOST
                    if not(shadow_mode):
                        ghost.update(player.position)  # TEMP-GHOST
                    if (ghost.x, ghost.y) == player.position:  # TEMP-GHOST
                        if ghost.state == "escape":  # TEMP-GHOST
                            ghost.get_eaten()  # TEMP-GHOST
                            player.score += con['points_per_ghost']  # TEMP-GHOST
                        elif ghost.state == "chasing" and not invincible:  # TEMP-GHOST
                            if not player.respawn():  # TEMP-GHOST
                                pygame.quit()  # TEMP-GHOST
                                exit()  # TEMP-GHOST
            frame_tick_count = 0
        if game_state == 'playing':
            draw_maze(maze, CELL_SIZE)
            draw_pacgums()
            draw_pacman()
            # TEMP-GHOST: subsurface lines up ghost grid coords with the maze's x_cor/y_cor offset
            maze_surface = screen.subsurface((x_cor, y_cor, maze_width * CELL_SIZE, maze_height * CELL_SIZE))  # TEMP-GHOST
            ghost_renderer.draw_ghosts(maze_surface, ghosts)  # TEMP-GHOST
            display_timer(level_time)
            display_hearts(player.lives)
            display_level(level_index + 1)
            pygame.display.update()
        elif game_state == 'submenu':
            buttons = display_submenu(screen, CELL_SIZE, screen_width, screen_height)
            if player_name == '':
                name_rect = pygame.Rect(screen_width/2 - 155, screen_height/2 + 14, 340, 50)
                pygame.draw.rect(screen, 'yellow', name_rect, 2)
                text_surface = name_font.render('enter your name', True, 'grey')
                screen.blit(text_surface, (screen_width/2 - 150, screen_height/2 + 20))
            else:
                name_rect = pygame.Rect(screen_width/2 - 35 - len(player_name) * 10, screen_height/2 + 14, len(player_name) * 28, 50)
                pygame.draw.rect(screen, 'yellow', name_rect, 2)
                text_surface = name_font.render(player_name, True, (255, 255, 255))
                screen.blit(text_surface, (screen_width/2 - 30 - \
                    len(player_name) * 10, screen_height/2 + 20))
            pygame.display.update()

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
                    if buttons[0].collidepoint(event.pos):
                        game_state = 'playing'
                        #buttons = display_menu(screen, CELL_SIZE, screen_width, screen_height)
                        cheat_mode_buttons = display_cheat_mode(screen, CELL_SIZE, screen_width, screen_height)
                    elif buttons[1].collidepoint(event.pos):
                        game_state = 'instructions'
                        buttons = display_menu(screen, CELL_SIZE, screen_width, screen_height)
                        buttons = display_instructions(screen, CELL_SIZE, screen_width, screen_height)
                    elif buttons[2].collidepoint(event.pos):
                        game_state = 'high_score'
                        buttons = display_high_scores(screen, CELL_SIZE, screen_width, screen_height, con['highscore_filename'])
                    elif buttons[3].collidepoint(event.pos):
                        pygame.quit()
                        exit()
                elif game_state == 'playing':
                    if cheat_mode_buttons[0].collidepoint(event.pos):
                        invincible = not(invincible)
                    elif cheat_mode_buttons[1].collidepoint(event.pos):
                        player.lives = 100000
                    elif cheat_mode_buttons[2].collidepoint(event.pos):
                        shadow_mode = not(shadow_mode)
                    elif cheat_mode_buttons[3].collidepoint(event.pos):
                        level_index += 1
                        if level_index >= len(con['levels']):
                            pygame.quit()
                            exit()
                        switch_level(level_index)
                        cheat_mode_buttons = display_cheat_mode(screen, CELL_SIZE, screen_width, screen_height)
                    elif cheat_mode_buttons[4].collidepoint(event.pos):
                        time_paused = not(time_paused)
                        if time_paused:
                            pygame.draw.rect(screen, (0, 255, 0), pygame.Rect(screen_width/2 + 800, screen_height/2, 20, 20), border_radius=50)
                        else:
                            pygame.draw.rect(screen, (255, 0, 0), pygame.Rect(screen_width/2 + 800, screen_height/2, 20, 20), border_radius=50)
                    elif cheat_mode_buttons[5].collidepoint(event.pos):
                        speed_boost = not(speed_boost)
                elif game_state == 'submenu':
                    if buttons[0].collidepoint(event.pos):
                        game_state = 'playing'
                        cheat_mode_buttons = display_cheat_mode(screen, CELL_SIZE, screen_width, screen_height)
                    elif buttons[1].collidepoint(event.pos):
                        game_state = 'menu'
                        buttons = display_menu(screen, CELL_SIZE, screen_width, screen_height)
                        #game_state = 'name_entry'
                        #input_rect = pygame.Rect(screen_width/2, screen_height/2, 600, 900)
                        #pygame.draw.rect(screen, (255, 0, 0), input_rect)
                elif game_state == 'instructions':
                    if buttons[0].collidepoint(event.pos):
                        game_state = 'menu'
                        buttons = display_menu(screen, CELL_SIZE, screen_width, screen_height)
                elif game_state == 'high_score':
                    if buttons[0].collidepoint(event.pos):
                        game_state = 'menu'
                        buttons = display_menu(screen, CELL_SIZE, screen_width, screen_height)

                elif game_state == 'name_entry':
                    pass
            elif game_state == 'instructions':
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
            elif event.type == pygame.KEYDOWN and game_state == 'submenu':
                if event.key == pygame.K_BACKSPACE:
                    player_name = player_name[:-1]
                elif event.key in (pygame.K_KP_ENTER, pygame.K_RETURN):
                    add_high_score(con['highscore_filename'] ,player_name, player.score)
                    game_state = 'menu'
                    buttons = display_menu(screen, CELL_SIZE, screen_width, screen_height)
                    #add_high_score(con['highscore_filename'] ,player_name, player.score)
                else:
                    if len(player_name) <= 10:
                        player_name += event.unicode
                    #text_surface = level_font.render(player_name, True, (255, 255, 255))
                    #screen.blit(text_surface, (screen_width/2 - 150, screen_height/2))
        if all(pacgum.eaten for pacgum in pacgums):
            print(f"Level complete! {player.score}")
            level_index += 1
            if level_index >= len(con['levels']):
                pygame.quit()
                exit()
            #level += 1
            switch_level(level_index)
            cheat_mode_buttons = display_cheat_mode(screen, CELL_SIZE, screen_width, screen_height)
if __name__ == '__main__':
    main()
