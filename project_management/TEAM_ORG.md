# Team Organization

Team: **ybarakat** (Yazeed) and **aalrousa** (git author `rsn026`).

Split below is derived from `git log --format=%an -- <file>` per file, i.e. who actually authored commits touching each file — not a claimed division of labor.

| File | Primary author(s) | Notes |
|---|---|---|
| `game.py` | Yazeed (9 commits) | Main loop, event handling, state machine |
| `displays.py` (formerly `menu.py`) | Yazeed (8), aalrousa (1) | Menu/HUD screens |
| `maze_pacgum.py` (formerly `maze.py`) | Yazeed (5), aalrousa (1) | Maze loading, pacgum placement |
| `config_parser.py` | aalrousa (3), Yazeed (1) | Config loading and validation |
| `ghost.py` | Yazeed (3), aalrousa (2) | Ghost AI — see below |
| `ghost_renderer.py` | Yazeed (3), aalrousa (1) | Ghost sprite rendering |
| `pacman_setup.py` (formerly `player_setup.py`) | Yazeed (1), aalrousa (1) | Pacman entity/movement |
| `high_scores_config.py` | Yazeed (1) | High-score persistence |
| `constants.py` | Yazeed | Shared rendering constants (new since this table was last drawn up) |

**`ghost.py` ownership note:** the file was deleted and re-added multiple times across both contributors' history before the current version stabilized — flagged in [RISK_ANALYSIS.md](RISK_ANALYSIS.md) as a coordination risk rather than attributed to either person specifically, since git history alone doesn't show who was blocking whom.

## Roles as actually exercised
- **Yazeed**: primary on the game loop/state machine, UI screens, maze integration, high-score system, and the debugging/stabilization pass in Phase 4 (see [TIMELINE.md](TIMELINE.md)).
- **aalrousa**: primary on config parsing/validation and early ghost AI authorship.

This table should be corrected by both team members if it misrepresents actual contribution — it's generated from commit authorship, which doesn't capture pairing, review, or design discussions that didn't produce commits.
