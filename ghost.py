import time
from typing import Tuple, List, Optional
import random


class Ghost:
    """A single maze ghost that chases, flees, or respawns based on state."""

    def __init__(self, start_x: int, start_y: int, difficulty: int,
                 maze: List[List[int]], level: int = 1):
        """Initialize a ghost at its corner spawn point.

        Args:
            start_x: Spawn/respawn column in the maze grid.
            start_y: Spawn/respawn row in the maze grid.
            difficulty: Difficulty tier; values >= 5 give shorter
                respawn/edible windows and a much larger view range.
            maze: The maze grid, used for wall/collision checks.
            level: Current level index, used to scale difficulty timers.
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

        if self.difficulty < 5:
            self.return_life = max(1, 8 - (self.level * 0.5))
            self.weak_ghost = max(1, 10 - (self.level * 0.5))
            self.view_range = 5 + (self.level * 2)
        else:
            self.return_life = max(1, 4 - (self.level * 0.5))
            self.weak_ghost = max(1, 5 - (self.level * 0.5))
            self.view_range = 30 + (self.level * 2)

        self.death_time = 0.0
        self.edible_time = 0.0

    def update(self, player_pos: Tuple[int, int]) -> None:
        """Advance the ghost's state machine by one tick.

        Handles the respawn cooldown, chasing the player, and the
        edible-then-expiring "escape" state after a super-pacgum.

        Args:
            player_pos: Current (x, y) grid position of the player.
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
        """Send the ghost back to its spawn corner and start the respawn timer."""
        self.state = "respawn"
        self.x = self.start_x
        self.y = self.start_y
        self.prev_x = self.start_x
        self.prev_y = self.start_y
        self.death_time = time.time()

    def make_edible(self) -> None:
        """Put the ghost into the fleeing "escape" state after a super-pacgum.

        No-op if the ghost is currently respawning, so eating one
        super-pacgum right after a ghost dies doesn't re-arm it early.
        """
        if self.state != "respawn":
            self.state = "escape"
            self.edible_time = time.time()

    def chase_player(self, player_pos: Tuple[int, int]) -> None:
        """Move one step toward the player via BFS, or wander if too far.

        Args:
            player_pos: Current (x, y) grid position of the player.
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
        """Move one step toward the neighbor farthest from the player.

        Args:
            player_pos: Current (x, y) grid position of the player.
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
        """Move one step to a random valid neighbor, avoiding backtracking when possible."""
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
        """Check whether stepping from (curr_x, curr_y) to (next_x, next_y) is legal.

        Args:
            curr_x: Current column.
            curr_y: Current row.
            next_x: Candidate column to move into.
            next_y: Candidate row to move into.
            wall_bit: Bitmask for the wall on the current cell's side
                facing the candidate move.

        Returns:
            True if the target cell is in bounds, not solid, and not
            blocked by a wall on the current cell.
        """
        if 0 <= next_y < len(self.maze) and 0 <= next_x < len(self.maze[0]):
            no_wall = not (self.maze[curr_y][curr_x] & wall_bit)
            not_solid = (self.maze[next_y][next_x] != 0xF)
            return no_wall and not_solid
        return False
