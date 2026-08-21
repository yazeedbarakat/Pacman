import time
from typing import Tuple, List, Optional
import random


class Ghost:
    def __init__(self, start_x: int, start_y: int, difficulty: bool, maze: List[List[int]], level: int = 1):
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

        if self.difficulty:
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
        self.state = "respawn"
        self.x = self.start_x
        self.y = self.start_y
        self.death_time = time.time()

    def make_edible(self) -> None:
        if self.state != "respawn":
            self.state = "escape"
            self.edible_time = time.time()

    def chase_player(self, player_pos: Tuple[int, int]) -> None:
        target_x, target_y = player_pos

        current_distance = abs(target_x - self.x) + abs(target_y - self.y)
        
        if current_distance > self.view_range:
            self.random_move()
            return

        queue = [(self.x, self.y, [])] 
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

    def is_valid_move(self, curr_x: int, curr_y: int, next_x: int, next_y: int, wall_bit: int) -> bool:
        if 0 <= next_y < len(self.maze) and 0 <= next_x < len(self.maze[0]):
            no_wall = not (self.maze[curr_y][curr_x] & wall_bit)
            not_solid = (self.maze[next_y][next_x] != 0xF)
            return no_wall and not_solid
        return False
