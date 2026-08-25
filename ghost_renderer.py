import os
import sys
import pygame
from typing import List, Dict, Optional
from ghost import Ghost


class GhostRenderer:
    """Loads ghost sprite images once and draws ghosts scaled to the maze grid."""

    def __init__(self, cell_size: int = 18) -> None:
        """Load and scale every ghost sprite for the given cell size.

        Args:
            cell_size: Maze cell size in pixels; sprites are scaled to
                fit inside a cell with a small border.
        """
        self.cell_size: int = cell_size
        self.ghost_size: int = cell_size - 16
        self.center_offset: int = (cell_size - self.ghost_size) // 2
        self.ghost_images: Dict[str, pygame.Surface] = {}
        self._load_ghost_images()

    def _load_ghost_images(self) -> None:
        """Load and scale each named ghost sprite, exiting the process on failure.

        A missing file or a pygame load error is treated as fatal
        (printed and `sys.exit(1)`) since the game can't render
        without its ghost assets.
        """
        asset_files = {
            'blinky': 'assets/ghosts/blinky.png',
            'pinky': 'assets/ghosts/pinky.png',
            'inky': 'assets/ghosts/inky.png',
            'clyde': 'assets/ghosts/clyde.png',
            'blue': 'assets/ghosts/blue_ghost.png',
        }

        for name, path in asset_files.items():
            if not os.path.exists(path):
                print(f"Error: Missing ghost image file at '{path}'")
                sys.exit(1)

            try:
                image = pygame.image.load(path).convert_alpha()
                self.ghost_images[name] = pygame.transform.scale(
                    image, (self.ghost_size, self.ghost_size)
                )
            except pygame.error as e:
                print(f"Error: Could not load ghost image '{path}': {e}")
                sys.exit(1)

    def draw_ghost(
        self,
        screen: pygame.Surface,
        ghost: Ghost,
        ghost_name: str = 'blinky',
        tick: int = 0,
        cycle_length: int = 10,
    ) -> None:
        """Draw a single ghost, interpolated between its previous and current cell.

        Blue "escape" sprite is used when the ghost is edible; nothing
        is drawn while it's respawning.

        Args:
            screen: Surface to draw onto.
            ghost: The ghost to draw.
            ghost_name: Which named sprite to use while chasing.
            tick: Current tick within the movement cycle, used for
                interpolating the on-screen position.
            cycle_length: Total ticks per movement cycle.
        """
        gx = ghost.prev_x + (ghost.x - ghost.prev_x) * tick / cycle_length
        gy = ghost.prev_y + (ghost.y - ghost.prev_y) * tick / cycle_length

        if ghost.state == "escape":
            screen.blit(self.ghost_images['blue'],
                        (gx * self.cell_size + 8, gy * self.cell_size + 8))
        elif ghost.state == "chasing":
            screen.blit(self.ghost_images[ghost_name],
                        (gx * self.cell_size + 8, gy * self.cell_size + 8))

    def draw_ghosts(
        self,
        screen: pygame.Surface,
        ghosts: List[Ghost],
        tick: int = 0,
        cycle_length: int = 10,
        ghost_names: Optional[List[str]] = None
    ) -> None:
        """Draw every ghost, cycling through ghost_names for their sprites.

        Args:
            screen: Surface to draw onto.
            ghosts: Ghosts to draw, in order.
            tick: Current tick within the movement cycle.
            cycle_length: Total ticks per movement cycle.
            ghost_names: Sprite names to cycle through; defaults to
                the four classic ghosts if not given.
        """
        if ghost_names is None:
            ghost_names = ['blinky', 'pinky', 'inky', 'clyde']

        i = 0
        for ghost in ghosts:
            name = ghost_names[i % len(ghost_names)]
            self.draw_ghost(screen, ghost, name, tick, cycle_length)
            i += 1
