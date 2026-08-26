"""Ghost rendering module for Pacman.

Provides the GhostRenderer class which handles loading ghost sprite
assets and drawing interpolated ghost positions onto a Pygame surface.
"""

import os
import sys
import pygame
from typing import List, Dict, Optional
from ghost import Ghost


class GhostRenderer:
    """Renders ghost sprites onto a Pygame surface.

    Loads and scales ghost sprite images from the assets directory and
    draws them with linear interpolation between grid positions for
    smooth animation. Ghosts in the 'escape' state are rendered with
    the blue (vulnerable) sprite; ghosts in 'respawn' are not drawn.

    Attributes:
        cell_size: Size of each maze cell in pixels.
        ghost_size: Rendered size of ghost sprites in pixels.
        ghost_images: Mapping of ghost names to their loaded Pygame surfaces.
    """

    def __init__(self, cell_size: int = 18) -> None:
        """Initialize the renderer and load ghost sprite assets.

        Args:
            cell_size: Size of each maze cell in pixels. Ghost sprites are
                scaled to ``cell_size - 8`` pixels. Defaults to 18.
        """
        self.cell_size: int = cell_size
        self.ghost_size: int = cell_size - 16
        self.center_offset: int = (cell_size - self.ghost_size) // 2
        self.ghost_images: Dict[str, pygame.Surface] = {}
        self._load_ghost_images()

    def _load_ghost_images(self) -> None:
        """Load and scale ghost sprite images from the assets directory.

        Loads PNG images for Blinky, Pinky, Inky, Clyde, and the blue
        (vulnerable) ghost. Each image is converted with alpha
        transparency and scaled to ``ghost_size``. Exits the program
        if any image file is missing or cannot be loaded.
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
        """Draw a single ghost with interpolated position.

        Linearly interpolates between the ghost's previous and current
        grid position based on the current tick within the movement
        cycle. Ghosts in 'escape' state are drawn with the blue sprite;
        ghosts in 'chasing' state use their named sprite. Ghosts in
        'respawn' state are not rendered.

        Args:
            screen: The Pygame surface to draw on.
            ghost: The Ghost instance to render.
            ghost_name: Name key for the ghost's sprite (e.g. 'blinky',
                'pinky', 'inky', 'clyde'). Defaults to 'blinky'.
            tick: Current tick within the movement cycle, used for
                interpolation. Defaults to 0.
            cycle_length: Total ticks per movement cycle. Defaults to 10.
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
        """Draw all ghosts in the list with their assigned sprites.

        Each ghost is assigned a name from ``ghost_names`` in a cyclic
        fashion (wrapping around if there are more ghosts than names).

        Args:
            screen: The Pygame surface to draw on.
            ghosts: List of Ghost instances to render.
            tick: Current tick within the movement cycle. Defaults to 0.
            cycle_length: Total ticks per movement cycle. Defaults to 10.
            ghost_names: Ordered list of ghost name keys to assign. If
                None, defaults to ['blinky', 'pinky', 'inky', 'clyde'].
        """
        if ghost_names is None:
            ghost_names = ['blinky', 'pinky', 'inky', 'clyde']

        i = 0
        for ghost in ghosts:
            name = ghost_names[i % len(ghost_names)]
            self.draw_ghost(screen, ghost, name, tick, cycle_length)
            i += 1
