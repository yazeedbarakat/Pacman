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

## Phase 4 — Stabilization & polish (2026-08-22 to 2026-08-25, ongoing)
- `main()`'s event handling split into per-state handler functions
- Name-entry/high-score flow rebuilt as its own game state, reachable from death, timeout, and level-complete (previously only reachable via pausing, and only partially wired)
- Player and ghost movement smoothed (interpolated rendering) after both were snapping instantly between grid cells
- Ghost movement speed scaled per level (slow at level 1, matching Pac-Man's speed by the last level)
- Several timing/state bugs found and fixed: level index not resetting on restart, a frame-counter reset ordering bug that froze all movement, and a tick-counter desync that silently stopped ghosts from moving after a menu restart or level transition
- Cheat mode completed (all 6 toggles functional, including speed boost)
- Codebase brought to a clean `flake8` and `mypy --strict` pass
- Project management documentation (this directory) restored — it existed as a README section as of 2026-08-01 but was removed before any actual directory was created
