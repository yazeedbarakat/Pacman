*This activity has been created as part of the 42 curriculum by aalrousa, ybarakat.*

# Pac-Man

## Description

This project is an object-oriented recreation of the classic 1980 arcade game **Pac-Man**, implemented in Python using Pygame and an external maze generator package. The goal of the game is to navigate Pac-Man through randomly generated maze corridors, eat all the Pacgums while dodging chasing ghosts, and score maximum points before running out of lives or time.

The project demonstrates modular software architecture, robust error handling, JSON configuration parsing, dynamic sprite rendering, state-driven ghost AI, and automated build/linting via a `Makefile`.

---

## Instructions

### Prerequisites
- **Python**: Version 3.10 or later
- **Dependencies**: `pygame`, `flake8`, `mypy`

### Installation & Setup
To install project dependencies, run:
```bash
make install
```

### Running the Game
To launch the Pac-Man game with a configuration file:
```bash
make run
# Or directly via Python:
python3 game.py config.json
```

### Debugging
To launch the game in debug mode using Python's built-in debugger (`pdb`):
```bash
make debug
```

### Code Formatting & Static Analysis
To run static type checking (`mypy`) and code style enforcement (`flake8`):
```bash
make lint
```

### Cleaning Up
To remove temporary Python cache directories (`__pycache__`, `.mypy_cache`, `.pyc` files):
```bash
make clean
```

---

## Configuration

Game parameters are configured via a standard JSON file (e.g., `config.json`) which supports line comments starting with `#`.

### Config Schema & Defaults
| Parameter | Type | Default | Description |
|---|---|---|---|
| `highscore_filename` | `str` | `"pc.json"` | Path to persistent highscore JSON file |
| `lives` | `int` | `3` | Initial number of Pac-Man lives |
| `pacgum` | `int` | `42` | Number of pacgums placed in maze |
| `points_per_pacgum` | `int` | `10` | Score awarded for eating a small Pacgum |
| `points_per_super_pacgum` | `int` | `50` | Score awarded for eating a Super-pacgum |
| `points_per_ghost` | `int` | `200` | Score awarded for eating a vulnerable ghost |
| `seed` | `int` | `42` | Seed for fixed level 1 maze generation |
| `level_max_time` | `int` | `90` | Time limit per level in seconds |

Invalid or missing configuration keys fall back cleanly to safe defaults without throwing Python tracebacks.

---

## Highscore

The highscore module provides a persistent highscore system saved in JSON format on disk:
- **Persistence**: Highscores are loaded from `highscore.json` when the application starts and updated upon game completion.
- **Validation**: Player names are capped at 10 characters (alphanumeric characters and spaces only). Negative or non-integer scores are rejected.
- **Top 10 Rankings**: The system retains only the top 10 scores sorted descending.
- **Implementation Rationale**: Storing highscores as structured JSON allows simple file parsing, easy inspection during peer evaluations, and robust error handling against corrupt or missing files.

---

## Maze Generation

Maze levels are generated using the external `A-Maze-ing` package (`mazegenerator`):
- **Package Integration**: Integrated directly via `maze.py` through the `MazeGenerator` class without modifying the external package interface.
- **Corridor Generation**: The generator parameter `perfect=False` is passed to create loops and open corridors suitable for Pac-Man navigation.
- **Seed Progression**: Level 1 uses a fixed seed specified in `config.json` (`seed = 42`), ensuring a reproducible initial level, while subsequent levels generate randomized mazes.
- **Wall Encoding**: Maze cells return bitmask integers (`0x1` Top, `0x2` Right, `0x4` Bottom, `0x8` Left, `0xF` Solid Wall), which `maze.py` and `ghost.py` inspect for movement validation.

---

## Implementation

The project is structured into modular Python source files:
- **`game.py`**: Entry point and Pygame main loop. Handles display updates, tick timing, HUD rendering, keyboard input, and collision checking.
- **`config_parser.py`**: Strips `#` comment lines from JSON files and validates configuration types against default schemas.
- **`maze.py`**: Interoperates with `MazeGenerator`, loads maze grid arrays, and handles `Pacgum` and `SuperPacgum` placement.
- **`player_setup.py`**: Defines the `Player` class managing grid coordinates, lives, movement direction, score, and directional animation frames.
- **`ghost.py`**: Defines `Ghost` AI entities and `GhostState` (`CHASING`, `ESCAPE`, `RESPAWN`). Computes Manhattan distance pathfinding along valid corridors.
- **`ghost_renderer.py`**: Manages loading and dynamic scaling of ghost PNG sprite assets (`blinky`, `pinky`, `inky`, `clyde`, `blue_ghost`).

---

## General Software Architecture

```mermaid
graph TD
    A[game.py - Game Loop & Window] --> B[config_parser.py]
    A --> C[maze.py - Maze Loader & Pacgums]
    A --> D[player_setup.py - Player Entity]
    A --> E[ghost.py - Ghost AI]
    A --> F[ghost_renderer.py - Ghost Sprites]
    C --> G[mazegenerator Package]
    E --> H[GhostState Enum]
```

### Module Responsibilities & Coupling
- **Decoupled Graphics**: `ghost_renderer.py` abstracts sprite rendering away from `ghost.py` logic, allowing state updates and rendering to remain independent.
- **Event-Driven Movement**: Keypresses update `Player.cur_dir`, which is evaluated on every movement tick against `maze['grid']` wall bitmasks.
- **Robust Exception Handling**: File reads, image loading, and external package calls are wrapped in `try-except` blocks to prevent unhandled tracebacks.

---

## Project Management

Project management documentation, progress tracking, risk assessment, and peer evaluation acceptance test plans are documented in the dedicated `project_management/` directory.

- Link to directory: [project_management/](project_management/)

---

## Resources

### References & Documentation
- [Pygame Documentation](https://www.pygame.org/docs/) — Pygame graphical library references and event handling.
- [PEP 8 Style Guide for Python Code](https://peps.python.org/pep-0008/) — Code formatting standards enforced via `flake8`.
- [PEP 257 Docstring Conventions](https://peps.python.org/pep-0257/) — Documentation standard for Python modules and methods.
- [Pac-Man Game Mechanics](https://pacman.fandom.com/wiki/Pac-Man_Wiki) — Insights on arcade ghost AI behaviors and scoring mechanics.

### AI Usage Statement
Artificial Intelligence tools were utilized during the development of this project to:
- Assist in optimizing grid rendering offsets and sprite scaling math across varying display resolutions.
- Refactor conditional statements to meet strict PEP 8 and `flake8` line length requirements.
- Generate structured documentation templates and architectural summaries.
- Debug bitwise wall collision calculations (`0x1`, `0x2`, `0x4`, `0x8`) for ghost pathfinding.
