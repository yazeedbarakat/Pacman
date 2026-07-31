import os
import pygame
from typing import List, Dict, Optional
from ghost import Ghost, GhostState


class GhostRenderer:
    """Handles loading ghost sprite assets and rendering ghosts onto screen."""

    def __init__(self, cell_size: int = 18) -> None:
        """Initialize the GhostRenderer.

        Args:
            cell_size (int): Size of a maze cell in pixels. Defaults to 18.
        """
        self.cell_size: int = cell_size
        self.sprite_size: int = max(12, cell_size - 4)
        self.offset: int = (cell_size - self.sprite_size) // 2
        self.sprites: Dict[str, pygame.Surface] = {}
        self._load_sprites()

    def _load_sprites(self) -> None:
        """Load ghost PNG images from assets/ghosts/ and scale them."""
        asset_files = {
            'blinky': 'assets/ghosts/blinky.png',
            'pinky': 'assets/ghosts/pinky.png',
            'inky': 'assets/ghosts/inky.png',
            'clyde': 'assets/ghosts/clyde.png',
            'blue': 'assets/ghosts/blue_ghost.png',
        }

        for name, path in asset_files.items():
            if os.path.exists(path):
                try:
                    image = pygame.image.load(path).convert_alpha()
                    self.sprites[name] = pygame.transform.scale(
                        image, (self.sprite_size, self.sprite_size)
                    )
                except pygame.error as e:
                    print(f"Warning: Could not load ghost image '{path}': {e}")

    def draw_ghost(
        self,
        screen: pygame.Surface,
        ghost: Ghost,
        ghost_name: str = 'blinky'
    ) -> None:
        """Draw a single ghost based on its current state and identity.

        Args:
            screen (pygame.Surface): Pygame display surface.
            ghost (Ghost): The ghost instance to render.
            ghost_name (str): The name/identity of the ghost
                              ('blinky', 'pinky', 'inky', 'clyde').
        """
        gx = ghost.x * self.cell_size + self.offset
        gy = ghost.y * self.cell_size + self.offset
        sz = self.sprite_size

        if ghost.state == GhostState.ESCAPE:
            if 'blue' in self.sprites:
                screen.blit(self.sprites['blue'], (gx, gy))
            else:
                pygame.draw.rect(screen, 'blue', (gx, gy, sz, sz))
        elif ghost.state == GhostState.RESPAWN:
            pygame.draw.rect(screen, 'white', (gx, gy, sz, sz))
        else:
            # GhostState.CHASING
            if ghost_name in self.sprites:
                screen.blit(self.sprites[ghost_name], (gx, gy))
            else:
                color_map = {
                    'blinky': 'red',
                    'pinky': 'pink',
                    'inky': 'cyan',
                    'clyde': 'orange'
                }
                color = color_map.get(ghost_name, 'red')
                pygame.draw.rect(screen, color, (gx, gy, sz, sz))

    def draw_ghosts(
        self,
        screen: pygame.Surface,
        ghosts: List[Ghost],
        ghost_names: Optional[List[str]] = None
    ) -> None:
        """Draw all ghosts in the game.

        Args:
            screen (pygame.Surface): Pygame display surface.
            ghosts (List[Ghost]): List of ghost instances.
            ghost_names (Optional[List[str]]): List of ghost names in order.
        """
        if ghost_names is None:
            ghost_names = ['blinky', 'pinky', 'inky', 'clyde']

        for i, ghost in enumerate(ghosts):
            name = ghost_names[i % len(ghost_names)]
            self.draw_ghost(screen, ghost, name)
