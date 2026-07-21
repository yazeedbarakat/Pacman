from mazegenerator import MazeGenerator

def maze_loader(maze_size: tuple[int, int], maze_seed: int) -> dict:
    mg: MazeGenerator = MazeGenerator(size=maze_size, seed=maze_seed)
    maze: dict = {}
    maze['grid'] = mg.maze
    maze['maze_entry'] = mg.maze_entry
    maze['maze_exit'] = mg.maze_exit
    return maze


class Player:
    def __init__(self, grid: list[list[int]], width: int, height: int) -> None:
        self.center: tuple[int, int] = (width // 2, height // 2)
        self.position: tuple[int, int] = self.center
        self.lives: int = 3
        self.cur_dir: str = ''
        self.nxt_dir: str = ''
        self.score: int = 0
        self.grid = grid

    def move(self, direction: str) -> None:
        dir_map = {
                'N' : (0x1, 0 , -1),
                'E' : (0x2, 1, 0),
                'S' : (0x4, 0, 1),
                'W' : (0x8, -1, 0)
                }
        if self.grid[self.position[1]][self.position[0]] & dir_map[direction][0]:
            return
        self.position = (self.position[0] + dir_map[direction][1],
                         self.position[1] + dir_map[direction][2])

    def respawn(self) -> bool:
        self.lives -= 1
        self.position = self.center
        return self.lives > 0

