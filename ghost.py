import time
from typing import Tuple, List, Optional
from collections import deque


class Ghost:
    def __init__(self, start_x: int, start_y: int, difficulty: bool):
        self.start_x = start_x
        self.start_y = start_y
        self.x = start_x
        self.y = start_y

        self.difficulty = difficulty
        self.state = "chasing"

        if self.difficulty:
            self.return_life = 8
            self.weak_ghost = 10
            self.sight_range = 10

        else:
            self.return_life = 4
            self.weak_ghost = 5
            self.sight_range = 1000

        self.death_time = 0.0
        self.edible_time = 0.0

    def update(self, player_pos: Tuple[int, int], maze: list) -> None:
        if self.state == "respawn":
            current_time = time.time()
            if current_time - self.death_time >= self.return_life:
                self.state = "chasing"

        elif self.state == "chasing":
            self.chase_player(player_pos, maze)

        elif self.state == "escape":
            if time.time() - self.edible_time >= self.weak_ghost:
                self.state = "chasing"

            if self.state == "escape":
                self.escape_player(player_pos, maze)

    def chase_player(
        self, player_pos: Tuple[int, int], maze: List[List[int]]
    ) -> None:
        target_x, target_y = player_pos

        #dist between ghost and player "Manhattan Distance"
        current_distance = abs(target_x - self.x) + abs(target_y - self.y)
        if current_distance > self.sight_range:
            return

        dir_wall_map = {
            (0, -1): 0x1,  # Up
            (1, 0): 0x2,   # Right
            (0, 1): 0x4,   # Down
            (-1, 0): 0x8   # Left
        }

        queue = [(self.x, self.y, [])]
        visited = {(self.x, self.y)}  
        best_path = []


        while queue:
            curr_x, curr_y, path = queue.pop(0)

            if (curr_x, curr_y) == (target_x, target_y):
                best_path = path
                break

            for (dx, dy) in dir_wall_map:
                wall_bit = dir_wall_map[(dx, dy)]
                next_x = curr_x + dx
                next_y = curr_y + dy

                if 0 <= next_y < len(maze) and 0 <= next_x < len(maze[0]):
                    no_wall = not (maze[curr_y][curr_x] & wall_bit)
                    not_solid = (maze[next_y][next_x] != 0xF)

                    if no_wall and not_solid and (next_x, next_y) not in visited:
                        visited.add((next_x, next_y))
                        queue.append((next_x, next_y, path + [(next_x, next_y)]))

        if best_path:
            self.x, self.y = best_path[0]
        
       

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

        for (dx, dy) in dir_wall_map:
            wall_bit = dir_wall_map[(dx, dy)]
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
        self.state = "respawn"
        self.x = self.start_x
        self.y = self.start_y
        self.death_time = time.time()

    def make_edible(self) -> None:
        if self.state != "respawn":
            self.state = "escape"
            self.edible_time = time.time()
