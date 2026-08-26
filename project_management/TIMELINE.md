# Timeline

Built from the actual git history (`git log --all`), not reconstructed from memory. Dates reflect when work landed on either contributor's branch; several early commits have non-descriptive messages ("nd", "l", "ff") — see [RISK_ANALYSIS.md](RISK_ANALYSIS.md) for the note on commit hygiene.

Submission/defense date: **TBD** — not fixed at time of writing.

## Phase 1 — Scaffolding (2026-07-21 to 2026-07-26)
- Initial project skeleton, config file handling (`config_parser.py`, `config.json`)
- First pass at maze integration with the external `mazegenerator` package
- Config parser hardened to fall back to defaults on missing/invalid keys

## Phase 2 — Core gameplay loop (2026-07-28 to 2026-08-07)
- Menu screens (`menu.py`) built out
- First ghost AI implementation (`ghost.py`, `ghost_renderer.py`) — this file saw repeated delete/recreate cycles during this phase (see risk analysis)
- Pacgum placement and maze rendering

## Phase 3 — Feature completion (2026-08-17 to 2026-08-22)
- Fixed render throttling and a last-level crash; added the Instructions screen
- Ghosts finalized: chase/flee/respawn states, corner spawns
- High-score persistence and lives HUD added

## Phase 4 — Stabilization & polish (2026-08-22 to 2026-08-25)
- `main()`'s event handling split into per-state handler functions
- Name-entry/high-score flow rebuilt as its own game state, reachable from death, timeout, and level-complete (previously only reachable via pausing, and only partially wired)
- Player and ghost movement smoothed (interpolated rendering) after both were snapping instantly between grid cells
- Ghost movement speed scaled per level (slow at level 1, matching Pac-Man's speed by the last level)
- Several timing/state bugs found and fixed: level index not resetting on restart, a frame-counter reset ordering bug that froze all movement, and a tick-counter desync that silently stopped ghosts from moving after a menu restart or level transition
- Cheat mode completed (all 6 toggles functional, including speed boost)
- Codebase brought to a clean `flake8` and `mypy --strict` pass
- Project management documentation (this directory) restored — it existed as a README section as of 2026-08-01 but was removed before any actual directory was created

## Phase 5 — Gameplay fixes & doc accuracy pass (2026-08-25 to 2026-08-26, ongoing)
- Ghost chasing tuned: capped speed for playability, sped up early-level ghosts, limited chasing ghosts to one in levels 1-5 and two in 6-10, then settled on one flat medium speed for every level after those experiments
- Ghost/pacman collision and pacgum-eating now check on-screen (interpolated) position every frame instead of the logical grid position, matching what's actually drawn
- Ctrl+C, missing-asset, and maze-generator failures now exit cleanly instead of dumping a traceback
- `setup.cfg`'s line-length override removed and the codebase brought to a clean pass against flake8's real 79-character default (58 `E501` fixes across 7 files) — see [RISK_ANALYSIS.md](RISK_ANALYSIS.md)
- Dead code removed: an unused `get_ghost_move_interval()` wrapper that always returned `3`, and a redundant `display_menu()` call in the instructions-button handler whose return value was immediately discarded
- README corrected to match the current module names and behavior (`maze.py`→`maze_pacgum.py`, `player_setup.py`/`Player`→`pacman_setup.py`/`Pacman`, removed a `GhostState` enum and a maze `perfect=False` param that don't exist in the code, added the `levels` config key that was missing from the schema table)
