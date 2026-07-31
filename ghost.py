import time
from enum import Enum
from typing import Tuple, List, Optional


class GhostState(Enum):
    CHASING = 1
    ESCAPE = 2
    RESPAWN = 3


class Ghost:
    def __init__(self, start_x: int, start_y: int):
        self.start_x = start_x
        self.start_y = start_y
        self.x = start_x
        self.y = start_y

        # Current state
        self.state = GhostState.CHASING

        # Respawn mechanics
        self.respawn_duration = 5.0  # wait 5 seconds before coming back
        self.death_time = 0.0

        self.edible_duration = 7.0
        self.edible_time = 0.0

    def update(self, player_pos: Tuple[int, int], maze: list) -> None:
        if self.state == GhostState.RESPAWN:
            self.handle_respawn()
        elif self.state == GhostState.CHASING:
            self.chase_player(player_pos, maze)
        elif self.state == GhostState.ESCAPE:
            self.handle_escape_timer()
            if self.state == GhostState.ESCAPE:
                self.escape_player(player_pos, maze)

    def handle_respawn(self) -> None:
        current_time = time.time()
        if current_time - self.death_time >= self.respawn_duration:
            self.state = GhostState.CHASING

    def handle_escape_timer(self) -> None:
        if time.time() - self.edible_time >= self.edible_duration:
            self.state = GhostState.CHASING

    def chase_player(
        self, player_pos: Tuple[int, int], maze: List[List[int]]
    ) -> None:
        target_x, target_y = player_pos
        dir_wall_map = {
            (0, -1): 0x1,  # Up
            (1, 0): 0x2,   # Right
            (0, 1): 0x4,   # Down
            (-1, 0): 0x8   # Left
        }

        best_move: Optional[Tuple[int, int]] = None
        shortest_distance = float('inf')

        for (dx, dy), wall_bit in dir_wall_map.items():
            next_x = self.x + dx
            next_y = self.y + dy

            # Check maze boundary
            if 0 <= next_y < len(maze) and 0 <= next_x < len(maze[0]):
                # Check if current cell has a wall in this direction
                no_wall = not (maze[self.y][self.x] & wall_bit)
                not_solid = (maze[next_y][next_x] != 0xF)
                if no_wall and not_solid:
                    dist = abs(target_x - next_x) + abs(target_y - next_y)
                    if dist < shortest_distance:
                        shortest_distance = dist
                        best_move = (next_x, next_y)

        if best_move:
            self.x, self.y = best_move

    def escape_player(
        self, player_pos: Tuple[int, int], maze: List[List[int]]
    ) -> None:
        target_x, target_y = player_pos
        dir_wall_map = {
            (0, -1): 0x1,  # Up
            (1, 0): 0x2,   # Right
            (0, 1): 0x4,   # Down
            (-1, 0): 0x8   # Left
        }

        best_move: Optional[Tuple[int, int]] = None
        longest_distance = -1.0

        for (dx, dy), wall_bit in dir_wall_map.items():
            next_x = self.x + dx
            next_y = self.y + dy

            if 0 <= next_y < len(maze) and 0 <= next_x < len(maze[0]):
                no_wall = not (maze[self.y][self.x] & wall_bit)
                not_solid = (maze[next_y][next_x] != 0xF)
                if no_wall and not_solid:
                    dist = float(
                        abs(target_x - next_x) + abs(target_y - next_y)
                    )
                    if dist > longest_distance:
                        longest_distance = dist
                        best_move = (next_x, next_y)

        if best_move:
            self.x, self.y = best_move

    def get_eaten(self) -> None:
        self.state = GhostState.RESPAWN
        self.x = self.start_x
        self.y = self.start_y
        self.death_time = time.time()

    def make_edible(self) -> None:
        if self.state != GhostState.RESPAWN:
            self.state = GhostState.ESCAPE
            self.edible_time = time.time()
