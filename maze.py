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


class Pacgum:
    def __init__(self, position: tuple[int, int]) -> None:
        self.position: tuple[int, int] = position
        self.eaten: bool = False
        self.points = 10

    def eat(self) -> int:
        self.eaten = True
        return self.points

class SuperPacgum(Pacgum):
    def __init__(self, position: tuple[int, int]) -> None:
        super().__init__(self.position)
        self.points = 50



def place_pacgums(maze_size: tuple[int, int], maze_grid: list[list[int]]) -> list[Pacgum]:
    pacgums: list[Pacgum, SuperPacgum] = []
    corners: list[tuple[int, int]] = [
            (0, 0), (maze_size[0] -1, 0), (0, maze_size[1] -1),
            (maze_size[0] -1, maze_size[1] -1)
            ]
    for row in range(maze_size[1]):
        for col in range(maze_size[0]):
            if maze_grid[row][col] != 0xF and not (col, row) in corners:
                pacgums.append(Pacgum((col, row)))
    for cor in corners:
        pacgums.append(SuperPacgum(cor))
    return pacgums



