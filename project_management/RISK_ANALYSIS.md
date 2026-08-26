# Risk Analysis

Risks below are grounded in things that actually happened during development — either issues found and fixed, or structural properties of the codebase as it stands. Not a generic checklist.

## Realized risks (found and fixed)

**Tick-counter desync silently stopped ghost movement.** Ghost movement and Pacman's movement each run on their own frame-counter cycle so ghosts can move slower than the player. Early implementations relied on both counters staying in phase (both being multiples of the same base interval) to know when to trigger a ghost move. Two separate real-world triggers broke that assumption: restarting from the menu (one counter got reset, the other didn't) and natural level transitions (the cycle length itself changes per level, which could force an early, out-of-phase reset). Both caused ghosts to stop moving with no error or crash — just silent, hard-to-diagnose behavior.
- *Mitigation applied*: the ghost-move trigger no longer depends on staying in phase with the player's counter at all — it's checked independently every frame. Removes the whole class of bug rather than patching each trigger individually.
- *Lesson*: when two independent timers must coordinate, prefer checking each condition independently over relying on their periods staying aligned — alignment assumptions break silently, not loudly.

**Movement-render mismatch caused inconsistent collisions.** After ghost movement was smoothed (interpolated between grid cells instead of snapping), the ghost's logical grid position updated instantly at the start of a move, while its on-screen position took much longer to visually arrive. Collision checks used the logical (already-arrived) position, so Pacman could "die" to a ghost that visually hadn't gotten there yet, or walk straight through one still mid-glide with no collision registering.
- *Mitigation applied*: collision checks now use the ghost's currently-interpolated (rounded) position, recomputed every frame, so what's checked matches what's drawn.

**Skip-level cheat crashed at the last level.** The cheat allowed incrementing past the last valid level index and then unconditionally tried to load that (nonexistent) level's config, raising `IndexError`.
- *Mitigation applied*: the load-next-level call is now conditional on there being a next level at all.

**Restarting a run after death/win left stale state.** Player lives, score, position, and the maze weren't recreated when returning to the menu and pressing Play again — a player could restart with 0 lives already set from the previous death, ending the new run instantly.
- *Mitigation applied*: a dedicated `set_game()` reset routine now recreates player/maze/pacgums/ghosts and is called both at startup and whenever the menu is re-entered.

**`setup.cfg` had quietly loosened the flake8 line-length limit to 100.** The assignment requires adherence to "the flake8 coding standard," which by default caps lines at 79 characters. A `setup.cfg` in the repo root raised that to 100, so `make lint` was passing against a relaxed standard rather than flake8's real default — a gap that would only surface if a reviewer ran flake8 without that file, or asked why line length didn't match PEP 8 as the README claimed.
- *Mitigation applied*: `setup.cfg` removed and all resulting `E501` violations (58 lines across 7 files) fixed against the real 79-character default.

## Standing risks (not fully mitigated, worth tracking)

**External `mazegenerator` dependency.** Per the assignment, this package is owned by another group, must be used as-is, and gets reinstalled fresh during peer review. If its API changes between now and defense, `maze_pacgum.py`'s integration breaks with no warning from our side. *Mitigation*: pin the exact version we're developing against if a `requirements.txt`/`Makefile install` step doesn't already do so — worth double-checking before submission.

**Levels after the first aren't actually randomized.** `switch_level()` in `game.py` regenerates every non-first-level maze with a hardcoded seed of `0`, so every playthrough produces the identical level 2, level 3, etc. Only level 1's seed is config-driven (`con['seed']`). Not caught yet by manual playtesting because a fixed layout still "works" — it just isn't the randomized-per-level behavior the maze integration implies. Worth deciding whether this is intentional before defense.

**No automated tests.** All verification this project has had is manual playtesting (see [TEST_PLAN.md](TEST_PLAN.md)). Every bug listed above under "realized risks" was found by playing the game, not by a test catching a regression. A change to shared state (the game loop's tick-counter logic in particular) could silently reintroduce any of them.

**Commit message hygiene.** A meaningful fraction of the git history is single-word or non-descriptive commit messages ("nd", "l", "ff", "gg"). This doesn't affect the running game, but makes it harder to answer "why was this change made" if asked in defense — worth being ready to explain specific changes independent of what the commit log says.

**Large parameter-threading pattern in `game.py`.** Loop state (`buttons`, `level_index`, `game_state`, tick counters, cheat toggles) is threaded manually as positional arguments through several handler functions and their return tuples, growing every time a new piece of state was needed. This was the direct cause of at least two bugs this session (a value not being returned/propagated correctly). It currently works, but adding more state the same way will keep increasing that risk — worth considering a small state container if the game grows further.
