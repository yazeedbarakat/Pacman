import time
from enum import Enum
from typing import Tuple

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

    def chase_player(self, player_pos: Tuple[int, int], maze: list) -> None:
        target_x, target_y = player_pos
        directions = [(0, -1), (0, 1), (-1, 0), (1, 0)]

        best_move = None
        shortest_distance = float('inf')

        for dx, dy in directions:
            next_x = self.x + dx
            next_y = self.y + dy

            # next position is within the maze boundaries
            if 0 <= next_y < len(maze) and 0 <= next_x < len(maze[0]):
                # Check if the tile is a corridor
                if maze[next_y][next_x] != '██':
                    # Calculate distance to the player from this new tile
                    distance = abs(target_x - next_x) + abs(target_y - next_y)
                    # If best path, save it
                    if distance < shortest_distance:
                        shortest_distance = distance
                        best_move = (next_x, next_y)

        # Execute the move
        if best_move:
            self.x, self.y = best_move

    def escape_player(self, player_pos: Tuple[int, int], maze: list) -> None:
        target_x, target_y = player_pos
        directions = [(0, -1), (0, 1), (-1, 0), (1, 0)]

        best_move = None
        longest_distance = -1  # Start extremely low so any valid move is considered

        for dx, dy in directions:
            next_x = self.x + dx
            next_y = self.y + dy

            # Check if the next position is within the maze boundaries
            if 0 <= next_y < len(maze) and 0 <= next_x < len(maze[0]):

                # Check if the tile is a corridor (not a wall)
                if maze[next_y][next_x] != '██':

                    #Calculate distance to the player from this new tile
                    distance = abs(target_x - next_x) + abs(target_y - next_y)

                    #If this path pushes the ghost further away, save it
                    if distance > longest_distance:
                        longest_distance = distance
                        best_move = (next_x, next_y)

        # Execute the move
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
