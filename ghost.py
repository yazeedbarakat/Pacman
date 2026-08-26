"""Ghost AI module for Pacman.

Defines the Ghost class which implements three behavioral states
(chasing, escape, respawn) with BFS-based pathfinding, difficulty
scaling, and maze-aware movement.
"""

import time
from typing import Tuple, List, Optional
import random


class Ghost:
    """A ghost enemy with state-driven AI behavior.

    Each ghost operates in one of three states:
        - **chasing**: Actively pursues the player using BFS pathfinding
          when within view range, or moves randomly otherwise.
        - **escape**: Flees from the player after a super pac-gum is eaten,
          maximizing Manhattan distance each step.
        - **respawn**: Waits at the spawn point for a cooldown period
          after being eaten by the player.

    Difficulty and level affect respawn time, edible duration, and
    view range.

    Attributes:
        x: Current x-coordinate in the maze.
        y: Current y-coordinate in the maze.
        state: Current behavioral state ('chasing', 'escape', or 'respawn').
        view_range: Maximum Manhattan distance at which the ghost can
            detect the player.
    """

    def __init__(self, start_x: int, start_y: int, difficulty: bool,
                 maze: List[List[int]], level: int = 1):
        """Initialize a ghost with position, difficulty, and maze reference.

        Args:
l            start_x: Starting x-coordinate (also used as respawn position).
            start_y: Starting y-coordinate (also used as respawn position).
            difficulty: If False, the ghost uses easier settings (shorter
                view range, longer respawn/edible timers). If True, uses
                harder settings with effectively infinite view range.
            maze: 2D list representing the maze, where each cell's value
                encodes wall bits (N=0x1, E=0x2, S=0x4, W=0x8) and 0xF
                indicates a solid block.
            level: Current game level (1-indexed), used to scale ghost
                parameters.
        """
        self.start_x = start_x
        self.start_y = start_y
        self.x = start_x
        self.y = start_y
        self.prev_x = start_x
        self.prev_y = start_y
        self.level = level
        self.difficulty = difficulty
        self.maze = maze
        self.state = "chasing"

        self.dir_wall_map = {
            (0, -1): 0x1,
            (1, 0): 0x2,
            (0, 1): 0x4,
            (-1, 0): 0x8
        }

        if not self.difficulty:
            self.return_life = max(1, 8 - (self.level * 0.5))
            self.weak_ghost = max(1, 10 - (self.level * 0.5))
            self.view_range = 5 + (self.level * 2)
        else:
            self.return_life = max(1, 4 - (self.level * 0.5))
            self.weak_ghost = max(1, 5 - (self.level * 0.5))
            self.view_range = 10000

        self.death_time = 0.0
        self.edible_time = 0.0

    def update(self, player_pos: Tuple[int, int]) -> None:
        """Update the ghost's state and position for one game tick.

        Handles state transitions (respawn cooldown expiry, edible timer
        expiry) and delegates movement to the appropriate behavior method.

        Args:
            player_pos: The player's current (x, y) position.
        """
        if self.state == "respawn":
            if time.time() - self.death_time >= self.return_life:
                self.state = "chasing"
        elif self.state == "chasing":
            self.chase_player(player_pos)
        elif self.state == "escape":
            if time.time() - self.edible_time >= self.weak_ghost:
                self.state = "chasing"
            else:
                self.escape_player(player_pos)

    def get_eaten(self) -> None:
        """Handle the ghost being eaten by the player.

        Transitions the ghost to the 'respawn' state, resets its position
        to the spawn point, and records the death timestamp for cooldown
        tracking.
        """
        self.state = "respawn"
        self.x = self.start_x
        self.y = self.start_y
        self.prev_x = self.start_x
        self.prev_y = self.start_y
        self.death_time = time.time()

    def make_edible(self) -> None:
        """Make the ghost edible (vulnerable) after a super pac-gum is eaten.

        Transitions the ghost to the 'escape' state unless it is currently
        respawning. Records the timestamp to track edible duration.
        """
        if self.state != "respawn":
            self.state = "escape"
            self.edible_time = time.time()

    def chase_player(self, player_pos: Tuple[int, int]) -> None:
        """Move the ghost toward the player using BFS pathfinding.

        If the player is outside the ghost's view range (Manhattan
        distance), the ghost moves randomly instead. Otherwise, a
        breadth-first search finds the shortest path through the maze
        and the ghost advances one step along it.

        Args:
            player_pos: The player's current (x, y) position.
        """
        self.prev_x, self.prev_y = self.x, self.y
        target_x, target_y = player_pos

        current_distance = abs(target_x - self.x) + abs(target_y - self.y)

        if current_distance > self.view_range:
            self.random_move()
            return

        queue: List[Tuple[int, int, List[Tuple[int, int]]]] = [(self.x, self.y, [])]
        visited = {(self.x, self.y)}
        best_path = []

        while queue:
            current_state = queue.pop(0)
            curr_x = current_state[0]
            curr_y = current_state[1]
            path = current_state[2]

            if (curr_x, curr_y) == (target_x, target_y):
                best_path = path
                break

            for (dx, dy), wall_bit in self.dir_wall_map.items():
                next_x = curr_x + dx
                next_y = curr_y + dy

                if self.is_valid_move(curr_x, curr_y, next_x, next_y, wall_bit):
                    if (next_x, next_y) not in visited:
                        visited.add((next_x, next_y))
                        queue.append((next_x, next_y, path + [(next_x, next_y)]))

        if best_path:
            self.x, self.y = best_path[0]

    def escape_player(self, player_pos: Tuple[int, int]) -> None:
        """Move the ghost away from the player.

        Evaluates all valid adjacent moves and selects the one that
        maximizes Manhattan distance from the player.

        Args:
            player_pos: The player's current (x, y) position.
        """
        self.prev_x, self.prev_y = self.x, self.y
        target_x, target_y = player_pos

        best_move: Optional[Tuple[int, int]] = None
        longest_distance = -1

        for (dx, dy), wall_bit in self.dir_wall_map.items():
            next_x = self.x + dx
            next_y = self.y + dy

            if self.is_valid_move(self.x, self.y, next_x, next_y, wall_bit):
                dist = abs(target_x - next_x) + abs(target_y - next_y)
                if dist > longest_distance:
                    longest_distance = dist
                    best_move = (next_x, next_y)

        if best_move:
            self.x, self.y = best_move

    def random_move(self) -> None:
        """Move the ghost to a random valid adjacent cell.

        Collects all valid moves and, if more than one option exists,
        excludes the previous position to avoid immediate backtracking.
        A random choice is then made from the remaining options.
        """
        valid_moves = []

        for (dx, dy), wall_bit in self.dir_wall_map.items():
            next_x = self.x + dx
            next_y = self.y + dy

            if self.is_valid_move(self.x, self.y, next_x, next_y, wall_bit):
                valid_moves.append((next_x, next_y))

        if len(valid_moves) > 1 and (self.prev_x, self.prev_y) in valid_moves:
            valid_moves.remove((self.prev_x, self.prev_y))

        if valid_moves:
            self.prev_x, self.prev_y = self.x, self.y
            self.x, self.y = random.choice(valid_moves)

    def is_valid_move(self, curr_x: int, curr_y: int, next_x: int,
                      next_y: int, wall_bit: int) -> bool:
        """Check whether a move between two adjacent cells is valid.

        A move is valid if the destination is within maze bounds, there
        is no wall between the current and next cell (checked via the
        wall bitmask), and the destination is not a solid block (0xF).

        Args:
            curr_x: Current x-coordinate.
            curr_y: Current y-coordinate.
            next_x: Destination x-coordinate.
            next_y: Destination y-coordinate.
            wall_bit: Bitmask for the wall direction being crossed.

        Returns:
            True if the move is valid, False otherwise.
        """
        if 0 <= next_y < len(self.maze) and 0 <= next_x < len(self.maze[0]):
            no_wall = not (self.maze[curr_y][curr_x] & wall_bit)
            not_solid = (self.maze[next_y][next_x] != 0xF)
            return no_wall and not_solid
        return False
