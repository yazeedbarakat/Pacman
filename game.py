import sys
import pygame
import maze as m
import player_setup
from ghost import Ghost, GhostState
from ghost_renderer import GhostRenderer
from config_parser import read_config

config_file = sys.argv[1] if len(sys.argv) > 1 else 'config.json'
config = read_config(config_file) if config_file else {}

maze_width, maze_height = 30, 30
CELL_SIZE = 18
HUD_HEIGHT = 36
SCREEN_WIDTH = maze_width * CELL_SIZE
SCREEN_HEIGHT = maze_height * CELL_SIZE + HUD_HEIGHT
FPS = 60

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Pacman')
clock = pygame.time.Clock()
font = pygame.font.SysFont('arial', 14, bold=True)

seed = config.get("seed", 42)
max_time_sec = config.get("level_max_time", 90)
maze = m.maze_loader((maze_width, maze_height), seed)
pacgums = m.place_pacgums((maze_width, maze_height), maze['grid'])
player = player_setup.Player(
    maze['grid'], maze_width, maze_height, CELL_SIZE
)
player.lives = config.get("lives", 3)
ghost_renderer = GhostRenderer(CELL_SIZE)

ghosts = [
    Ghost(1, 1),
    Ghost(maze_width - 2, 1),
    Ghost(1, maze_height - 2),
    Ghost(maze_width - 2, maze_height - 2)
]


def draw_maze(maze: dict, cell_size: int) -> None:
    for y, row in enumerate(maze['grid']):
        for x, cell in enumerate(row):
            sx, sy = x * cell_size, y * cell_size
            if cell == 0xF:
                pygame.draw.rect(
                    screen, 'black', (sx, sy, cell_size, cell_size)
                )
                continue
            else:
                pygame.draw.rect(
                    screen, 'teal', (sx, sy, cell_size, cell_size)
                )
            if not (cell & 0x1):
                pygame.draw.rect(
                    screen, 'light gray',
                    (sx + 2, sy, cell_size - 4, cell_size // 2)
                )
            if not (cell & 0x2):
                hsize = cell_size // 2
                pygame.draw.rect(
                    screen, 'dark gray',
                    (sx + hsize, sy + 2, hsize, cell_size - 4)
                )
            if not (cell & 0x4):
                vsize = cell_size // 2
                pygame.draw.rect(
                    screen, 'dark gray',
                    (sx + 2, sy + vsize, cell_size - 4, vsize)
                )
            if not (cell & 0x8):
                pygame.draw.rect(
                    screen, 'light gray',
                    (sx, sy + 2, cell_size // 2, cell_size - 4)
                )
            pygame.draw.rect(
                screen, 'gray',
                (sx + 2, sy + 2, cell_size - 4, cell_size - 4)
            )


def draw_pacman() -> None:
    px = player.position[0] * CELL_SIZE + getattr(player, 'offset', 2)
    py = player.position[1] * CELL_SIZE + getattr(player, 'offset', 2)
    screen.blit(player.get_frame(), (px, py))


def draw_pacgums() -> None:
    rad = 2
    for pacgum in pacgums:
        if not pacgum.eaten:
            if isinstance(pacgum, m.SuperPacgum):
                rad = 4
            gx = pacgum.position[0] * CELL_SIZE + CELL_SIZE // 2
            gy = pacgum.position[1] * CELL_SIZE + CELL_SIZE // 2
            pygame.draw.circle(screen, 'yellow', (gx, gy), rad)


def draw_ghosts() -> None:
    ghost_renderer.draw_ghosts(screen, ghosts)


def draw_hud(
    score: int, lives: int, level: int = 1, time_left: int = 90
) -> None:
    hud_y = maze_height * CELL_SIZE
    pygame.draw.rect(
        screen, (20, 20, 20), (0, hud_y, SCREEN_WIDTH, HUD_HEIGHT)
    )
    pygame.draw.line(
        screen, 'teal', (0, hud_y), (SCREEN_WIDTH, hud_y), 2
    )
    hud_text = (
        f"Score: {score}  |  Lives: {lives}  |  "
        f"Level: {level}  |  Time: {time_left}s"
    )
    text_surf = font.render(hud_text, True, (255, 255, 255))
    screen.blit(text_surf, (15, hud_y + 10))


def main() -> None:
    tick_count = 0
    start_time = pygame.time.get_ticks()

    while True:
        clock.tick(FPS)
        tick_count += 1

        elapsed_sec = (pygame.time.get_ticks() - start_time) // 1000
        time_left = max(0, max_time_sec - elapsed_sec)

        if tick_count == 10:
            player.update_frame()
            player.move()

            for ghost in ghosts:
                ghost.update(player.position, maze['grid'])

            for pacgum in pacgums:
                if not pacgum.eaten and pacgum.position == player.position:
                    pacgum.eaten = True
                    player.score += pacgum.eat()

                    is_super = (
                        getattr(pacgum, 'is_super', False)
                        or isinstance(pacgum, m.SuperPacgum)
                    )
                    if is_super:
                        for ghost in ghosts:
                            ghost.make_edible()

            for ghost in ghosts:
                if (ghost.x, ghost.y) == player.position:
                    if ghost.state == GhostState.CHASING:
                        print("Pacman Lost a Life!")
                        still_alive = player.respawn()
                        for g in ghosts:
                            g.x, g.y = g.start_x, g.start_y
                            g.state = GhostState.CHASING
                        if not still_alive:
                            print(f"Game Over! Final Score: {player.score}")
                            pygame.time.delay(1500)
                            pygame.quit()
                            sys.exit(0)
                        break
                    elif ghost.state == GhostState.ESCAPE:
                        ghost.get_eaten()
                        player.score += 200

            tick_count = 0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    player.cur_dir = 'U'
                elif event.key == pygame.K_DOWN:
                    player.cur_dir = 'D'
                elif event.key == pygame.K_LEFT:
                    player.cur_dir = 'L'
                elif event.key == pygame.K_RIGHT:
                    player.cur_dir = 'R'

        draw_maze(maze, CELL_SIZE)
        draw_pacgums()
        draw_pacman()
        draw_ghosts()
        draw_hud(player.score, player.lives, 1, time_left)
        pygame.display.update()

        if all(pacgum.eaten for pacgum in pacgums):
            print(f"Level complete! {player.score}")
            pygame.quit()
            sys.exit(0)


if __name__ == '__main__':
    main()
