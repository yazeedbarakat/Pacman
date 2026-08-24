# Test Plan

No automated test suite exists (see [RISK_ANALYSIS.md](RISK_ANALYSIS.md)). All verification is manual, run via `make run` / `python3 game.py`. This is the checklist actually used during the Phase 4 stabilization pass, kept here so peer reviewers (and future us) can repeat it.

## Golden path
1. Launch → main menu appears with Play / Instructions / High Scores / Exit.
2. Click Play → level 1 loads, HUD shows level/timer/lives.
3. Move Pacman with arrow keys; confirm movement is smooth (no snapping between cells).
4. Eat a regular pacgum → score increases.
5. Eat a super pacgum → all ghosts turn edible (blue) and flee.
6. Eat an edible ghost → ghost respawns at its corner after a few seconds, score increases.
7. Clear all pacgums → next level loads automatically, HUD level counter increments.
8. Repeat through to the last level → clearing it goes to the name-entry screen (not a hard quit).
9. Type a name, press Enter → returns to menu.
10. Open High Scores from the menu → new entry appears, sorted highest-first, capped at 10 entries.

## Game-over paths (all three must reach name-entry, none should hard-quit)
- **Death**: let a chasing (non-edible) ghost catch Pacman with 0 lives remaining → name-entry screen appears, not a window close.
- **Timeout**: let the level timer hit 0 → same.
- **Win**: clear the final level → same (see golden path step 8).

## Cheat mode (accessed via the panel while playing)
- Invincibility: toggle on, walk into a chasing ghost, confirm no life lost.
- Unlimited lives: toggle, confirm lives counter reflects it.
- Shadow mode (ghost freeze): toggle, confirm ghosts stop moving but still register a collision if Pacman walks into one (not full invulnerability).
- Skip level: use on every level including the last — must transition to name-entry, not crash.
- Pause timer: toggle, confirm the HUD timer stops/resumes counting down.
- Speed boost: toggle, confirm Pacman covers 2 cells per movement tick instead of 1, and that pacgums/ghosts on the skipped-over cell are still correctly eaten/collided with (not just the landing cell).

## Restart flow
- Die or win → save name → back at menu → click Play again.
- Confirm: level resets to 1, lives reset to 3, score resets to 0, maze/pacgums are freshly placed, ghosts are back at their spawn corners and moving (not frozen).

## Cross-level ghost behavior
- Play through several levels in a row (natural progression, not skip-cheat) and confirm ghost movement speed visibly increases level over level, reaching full (Pacman-matching) speed by the last level.
- Confirm ghosts keep moving after a level transition — this previously broke silently (see risk analysis).

## Name entry
- Attempt to type more than 10 characters → input stops accepting at 10.
- Attempt symbols/punctuation → rejected; letters, digits, and spaces are accepted.
- Backspace removes the last character.

## Config robustness
- Temporarily rename/corrupt `config.json` (or edit out a required key) and confirm the game logs a warning and falls back to defaults rather than crashing — required by the assignment spec.
