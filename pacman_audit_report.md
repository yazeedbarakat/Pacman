# Pac-Man Project Audit Report

> Full code review, subject compliance verification, bug analysis, and unused code/asset inventory.
> Reviewed on: 2026-08-28

---

## Table of Contents

1. [Executive Summary](#executive-summary)
2. [Subject Compliance Checklist](#subject-compliance-checklist)
3. [Lint & Static Analysis Results](#lint--static-analysis-results)
4. [Bugs Found](#bugs-found)
5. [Unused Code](#unused-code)
6. [Unused Asset Files](#unused-asset-files)
7. [Code Quality Observations](#code-quality-observations)
8. [Config Parser Testing](#config-parser-testing)
9. [High Score System Testing](#high-score-system-testing)
10. [README Compliance](#readme-compliance)
11. [Makefile Compliance](#makefile-compliance)
12. [Project Management Docs](#project-management-docs)
13. [Risk Summary for Peer Review](#risk-summary-for-peer-review)

---

## Executive Summary

The project is a **functional and well-structured** Pac-Man implementation. The core gameplay loop works: menu → play → win/lose → name entry → menu. Ghost AI uses BFS pathfinding with escape/chase/respawn states. Cheat mode has 6 functional toggles. Config parsing is robust with proper defaults.

**Key strengths:**
- Clean modular architecture (8 focused source files)
- Comprehensive error handling (no tracebacks on bad config, missing files, etc.)
- Good documentation: docstrings on every function, detailed README, thorough project management docs
- `mypy` passes cleanly with the required flags

**Key concerns for peer review:**
- **11 flake8 violations** remain (the subject makes `make lint` mandatory)
- Entry point is `game.py` but the subject specifies `pac-man.py`
- Levels after the first use a hardcoded seed `0` (not random as the subject requires)
- `add_high_score()` does **not** validate name length or score type server-side
- Several unused asset files bloat the repo

---

## Subject Compliance Checklist

| Requirement | Status | Details |
|---|---|---|
| **Entry point**: `python3 pac-man.py config.json` | ⚠️ **MISMATCH** | File is named `game.py`, not `pac-man.py` |
| Exactly 1 argument (config file) | ✅ | [game.py:27-29](file:///home/rsn026/Desktop/Pacman/game.py#L27-L29) |
| No Python tracebacks on errors | ✅ | All paths wrapped in try/except |
| JSON config with `#` comment support | ✅ | [config_parser.py:61-63](file:///home/rsn026/Desktop/Pacman/config_parser.py#L61-L63) |
| Faulty config → clamp to defaults, log, continue | ✅ | Tested: missing keys, invalid types, negative values, out-of-range dims |
| At least 10 levels | ✅ | Config has 10 levels |
| Level 1 uses fixed seed from config | ✅ | [game.py:60](file:///home/rsn026/Desktop/Pacman/game.py#L60) uses `con['seed']` |
| Subsequent levels randomly generated | ❌ **FAIL** | [game.py:134](file:///home/rsn026/Desktop/Pacman/game.py#L134) uses hardcoded seed `0` |
| External maze generator (unmodified) | ✅ | Uses `mazegenerator-2.1.0-py3-none-any.whl` |
| Persistent highscore (JSON file) | ✅ | [high_scores_config.py](file:///home/rsn026/Desktop/Pacman/high_scores_config.py) |
| Highscore: robust to file errors | ✅ | Returns `[]` on corrupt/missing file |
| Highscore: name max 10 chars, alphanumeric+spaces | ⚠️ **PARTIAL** | Input enforced in game loop, but `add_high_score()` has no validation |
| Highscore: top 10 only | ✅ | [high_scores_config.py:54-55](file:///home/rsn026/Desktop/Pacman/high_scores_config.py#L54-L55) |
| Highscore: display in menu | ✅ | High Scores button on main menu |
| 4 ghosts, one per corner | ✅ | [game.py:87-88](file:///home/rsn026/Desktop/Pacman/game.py#L87-L88) |
| Player starts in middle | ✅ | [pacman_setup.py:54](file:///home/rsn026/Desktop/Pacman/pacman_setup.py#L54) |
| Pacgums in corridors | ✅ | [maze_pacgum.py:103-106](file:///home/rsn026/Desktop/Pacman/maze_pacgum.py#L103-L106) |
| Super-pacgums in 4 corners | ✅ | [maze_pacgum.py:98-112](file:///home/rsn026/Desktop/Pacman/maze_pacgum.py#L98-L112) |
| Super-pacgum makes ghosts edible | ✅ | [game.py:194-196](file:///home/rsn026/Desktop/Pacman/game.py#L194-L196) |
| Ghost chase behavior | ✅ | BFS pathfinding in [ghost.py:125-172](file:///home/rsn026/Desktop/Pacman/ghost.py#L125-L172) |
| Ghost flee when edible | ✅ | Manhattan distance maximization in [ghost.py:174-200](file:///home/rsn026/Desktop/Pacman/ghost.py#L174-L200) |
| Ghost respawn after eaten | ✅ | [ghost.py:101-113](file:///home/rsn026/Desktop/Pacman/ghost.py#L101-L113) |
| 3 starting lives | ✅ | Config default |
| Lose life on ghost touch | ✅ | [game.py:216-221](file:///home/rsn026/Desktop/Pacman/game.py#L216-L221) |
| Game over at 0 lives | ✅ | `pacman.respawn()` returns False |
| Win level when all pacgums eaten | ✅ | [game.py:197-205](file:///home/rsn026/Desktop/Pacman/game.py#L197-L205) |
| Win game when all levels cleared | ✅ | [game.py:199-203](file:///home/rsn026/Desktop/Pacman/game.py#L199-L203) |
| Time limit per level | ✅ | 90 seconds default, HUD countdown |
| Pause and resume | ✅ | ESC key → submenu with Continue/Save&Quit |
| Score/lives/level/time HUD | ✅ | All 4 displayed during gameplay |
| Main menu: Play, High Scores, Instructions, Exit | ✅ | [displays.py:97-120](file:///home/rsn026/Desktop/Pacman/displays.py#L97-L120) |
| Cheat mode | ✅ | 6 cheats: skip level, extra life, shadow, invincibility, pause timer, speed boost |
| WASD + arrow key movement | ✅ | [game.py:494-501](file:///home/rsn026/Desktop/Pacman/game.py#L494-L501) |
| Makefile: install, run, debug, clean, lint | ✅ | All 5 mandatory rules present |
| `.gitignore` | ⚠️ **INCOMPLETE** | Only `__pycache__`, missing `.mypy_cache` and `*.pyc` |
| Docstrings (Google style) | ✅ | Every function/method/class has docstrings |
| README in English | ✅ | |
| Project management directory | ✅ | 4 documents in `project_management/` |

---

## Lint & Static Analysis Results

### mypy (required flags)
```
✅ Success: no issues found in 9 source files
```

### flake8 — ❌ 11 violations

| File | Line | Code | Description |
|---|---|---|---|
| [game.py](file:///home/rsn026/Desktop/Pacman/game.py#L182) | 182 | E221 | Multiple spaces before operator |
| [game.py](file:///home/rsn026/Desktop/Pacman/game.py#L187) | 187 | E501 | Line too long (83 > 79) |
| [game.py](file:///home/rsn026/Desktop/Pacman/game.py#L189) | 189 | E501 | Line too long (83 > 79) |
| [game.py](file:///home/rsn026/Desktop/Pacman/game.py#L212) | 212 | E272 | Multiple spaces before keyword |
| [game.py](file:///home/rsn026/Desktop/Pacman/game.py#L225) | 225 | E128 | Continuation line under-indented |
| [game.py](file:///home/rsn026/Desktop/Pacman/game.py#L256) | 256 | E203 | Whitespace before `:` |
| [game.py](file:///home/rsn026/Desktop/Pacman/game.py#L256) | 256 | E231 | Missing whitespace after `:` |
| [game.py](file:///home/rsn026/Desktop/Pacman/game.py#L401) | 401 | E303 | Too many blank lines (3) |
| [game.py](file:///home/rsn026/Desktop/Pacman/game.py#L444) | 444 | E203 | Whitespace before `:` |
| [pacman_setup.py](file:///home/rsn026/Desktop/Pacman/pacman_setup.py#L136) | 136 | E501 | Line too long (83 > 79) |
| [pacman_setup.py](file:///home/rsn026/Desktop/Pacman/pacman_setup.py#L138) | 138 | E501 | Line too long (83 > 79) |

> [!WARNING]
> `make lint` **will fail** during peer review. The subject states lint must pass. All 11 violations are in `game.py` (9) and `pacman_setup.py` (2).

---

## Bugs Found

### 🔴 Critical

#### 1. `draw_pacgums()` radius variable not reset (latent bug)
**File:** [maze_pacgum.py:127-136](file:///home/rsn026/Desktop/Pacman/maze_pacgum.py#L127-L136)

```python
rad = 3                          # set once before loop
for pacgum in pacgums:
    if not pacgum.eaten:
        if isinstance(pacgum, SuperPacgum):
            rad = 6              # ← set to 6, never reset to 3
        pygame.draw.circle(... rad)
```

`rad` is set to `3` once outside the loop. When a `SuperPacgum` is encountered, `rad` is changed to `6` but **never reset to 3** for subsequent regular pacgums. Currently not visibly broken because `place_pacgums()` appends super-pacgums **after** all regular ones, so the enlarged radius only affects the 4 corner super-pacgums. However, if the list order ever changes (e.g., shuffling), all regular pacgums after the first super-pacgum would render at the wrong size.

**Should be:**
```python
if isinstance(pacgum, SuperPacgum):
    rad = 6
else:
    rad = 3
```

---

#### 2. Levels 2–10 are NOT randomly generated
**File:** [game.py:134](file:///home/rsn026/Desktop/Pacman/game.py#L134)

```python
maze = m.maze_loader((maze_width, maze_height), 0)  # hardcoded seed
```

The subject says: *"the first level is composed of a maze generated with a fixed seed, then, each subsequent level is composed of a maze randomly generated."* All subsequent levels use seed `0`, making them deterministic and identical across playthroughs.

**Should use:** `random.randint(0, 2**31)` or similar for levels 2+.

---

#### 3. `add_high_score()` has no server-side validation
**File:** [high_scores_config.py:44-56](file:///home/rsn026/Desktop/Pacman/high_scores_config.py#L44-L56)

The subject says names must be max 10 chars (alphanumeric + spaces) and scores must be non-negative integers. While the game loop enforces character filtering during input, the `add_high_score()` function itself accepts:
- Names longer than 10 characters → **accepted**
- Negative scores → **accepted**
- Non-integer scores (strings) → **accepted**
- Non-ASCII unicode characters → **accepted** (Arabic chars are in `pc.json`)

This means a corrupted or hand-edited `pc.json` could contain invalid data that persists forever.

---

### 🟡 Medium

#### 4. Pacman spawn infinite loop on degenerate mazes
**File:** [pacman_setup.py:55-57](file:///home/rsn026/Desktop/Pacman/pacman_setup.py#L55-L57)

```python
if self.grid[self.center[1]][self.center[0]] == 0xF:
    while self.grid[self.center[1]][self.center[0]] == 0xF:
        self.center = (self.center[0] - 1, self.center[1])
```

If the center cell and all cells to its left are solid walls (0xF), this while loop runs forever, or eventually accesses a negative index (wrapping to the right side of the grid in Python, potentially finding a non-wall cell — undefined behavior). No bounds check or timeout exists.

---

#### 5. Config with 0 levels causes `IndexError`
**File:** [game.py:43](file:///home/rsn026/Desktop/Pacman/game.py#L43)

If a config specifies `"levels": []`, `get_level_config(0)` will raise `IndexError`. The config parser doesn't enforce a minimum level count.

---

#### 6. Non-ASCII characters accepted in player names
**File:** [game.py:517-520](file:///home/rsn026/Desktop/Pacman/game.py#L517-L520)

```python
if (len(player_name) < 10
        and (event.unicode.isalnum()
             or event.unicode == ' ')):
```

Python's `.isalnum()` returns `True` for Unicode letters (Arabic, Chinese, etc.), not just ASCII. The current `pc.json` already contains Arabic names (`مم`, `نخو`, `منم`). The subject likely means ASCII alphanumeric only.

---

### 🟢 Low

#### 7. `button_collision()` uses `range()` for float coordinates
**File:** [game.py:256-267](file:///home/rsn026/Desktop/Pacman/game.py#L256-L267)

Uses `range(start_x, end_x + 1)` for collision. `Rect` coordinates from pygame are integers so this works, but it's an unusual pattern. `rect.collidepoint(pos)` is the standard pygame approach and more readable.

#### 8. Typo in parameter name: `buttuns`
**File:** [game.py:238](file:///home/rsn026/Desktop/Pacman/game.py#L238)

```python
def handle_submenu(player_name: str, buttuns: tuple[pygame.Rect, ...])
```

Also `butten` at [game.py:256](file:///home/rsn026/Desktop/Pacman/game.py#L256).

---

## Unused Code

### Unused Function Parameters

| File | Line | Function | Unused Parameter | Notes |
|---|---|---|---|---|
| [game.py](file:///home/rsn026/Desktop/Pacman/game.py#L237) | 237 | `handle_submenu()` | `player_name` | Docstring says "kept for call-site symmetry" |
| [game.py](file:///home/rsn026/Desktop/Pacman/game.py#L237) | 237 | `handle_submenu()` | `buttuns` | Docstring says "kept for call-site symmetry" |
| [pacman_setup.py](file:///home/rsn026/Desktop/Pacman/pacman_setup.py#L122) | 122 | `draw_pacman()` | `speed_boost` | Parameter accepted but never read in function body |

### Module-level Global: `level`
**File:** [game.py:67](file:///home/rsn026/Desktop/Pacman/game.py#L67)

```python
level = 0
```

This module-level `level` variable is used only in the initial `make_ghosts()` call at line 99. After that, `main()` uses its own local `level_index`. The global `level` is **never updated**, so the first `make_ghosts()` call always passes `level=0`. This is harmless but misleading — it looks like global state management but isn't.

---

## Unused Asset Files

The following asset files exist in the repository but are **never referenced** by any source code:

| File | Size | Notes |
|---|---|---|
| `assets/ghosts/blue.png` | 138 KB | Large ghost image — `blue_ghost.png` (180 B) is used instead |
| `assets/ghosts/pink.png` | 141 KB | Large ghost image — `pinky.png` (192 B) is used instead |
| `assets/ghosts/purple.png` | 142 KB | Large ghost image — not referenced anywhere |
| `assets/ghosts/red.png` | 139 KB | Large ghost image — `blinky.png` (183 B) is used instead |
| `assets/menu/pacman.png` | 217 KB | Different from `pac-man.png` (143 KB) which IS used |
| `assets/other/apple.png` | 171 B | Collectible sprite — never used in game |
| `assets/other/dot.png` | 108 B | Dot sprite — pacgums drawn as circles instead |
| `assets/other/strawberry.png` | 201 B | Collectible sprite — never used in game |
| `assets/fonts/SourceCodePro-Bold.otf` | 134 KB | Font file — never loaded by any code |

**Total wasted space:** ~715 KB (mostly the 4 large ghost PNGs)

---

## Code Quality Observations

### Strengths
- **Every function and class has Google-style docstrings** with Args/Returns sections
- **Clean error handling chain**: config errors → defaults, asset errors → clean exit, runtime errors → clean exit
- **Ghost AI is well-designed**: BFS chasing, Manhattan escape, random wandering with backtrack prevention
- **Interpolated rendering** for both Pacman and ghosts (smooth movement, not grid-snapping)
- **Modular separation**: rendering is fully decoupled from logic (ghost.py vs ghost_renderer.py)

### Concerns
- **Heavy use of global state** in `game.py` — 7 global variables mutated by `set_game()` and `switch_level()`
- **Parameter threading anti-pattern** — `handle_playing_buttons()` takes 8 params and returns 8 values. Risk of mismatch noted in their own [RISK_ANALYSIS.md](file:///home/rsn026/Desktop/Pacman/project_management/RISK_ANALYSIS.md)
- **`time.time()` for ghost timers** — Ghost escape/respawn durations use wall-clock time rather than frame-counting. This means pausing the game (ESC) does NOT pause the edible/respawn timers — ghosts continue their timers while paused
- **No `__main__` guard on module-level code** — Lines 27-68 of `game.py` execute at import time (arg parsing, pygame init, maze generation). This makes the module un-importable for testing

---

## Config Parser Testing

All tests passed:

| Test Case | Result |
|---|---|
| Valid config with all keys | ✅ Parsed correctly |
| Config with `#` comment lines | ✅ Comments stripped, values parsed |
| Missing config file | ✅ Returns defaults, logs error message |
| Invalid JSON content | ✅ Returns defaults, logs error message |
| Missing individual keys | ✅ Each missing key logs warning, uses default |
| Negative numeric values (`lives: -5`) | ✅ Clamped to default (3) |
| Invalid type (`lives: "three"`) | ✅ Falls back to default |
| Width below min (5) | ✅ Clamped to default (20) |
| Width above max (50) | ✅ Clamped to default (20) |
| Height below min (5) | ✅ Clamped to default (15) |
| Height above max (50) | ✅ Clamped to default (15) |
| Non-dict level entry | ✅ Falls back to 20×15 |

> [!NOTE]
> Only line-level `#` comments are supported (entire line is a comment). Inline comments like `{"key": 42 # comment}` are **not** supported, but the subject only requires lines starting with `#`.

---

## High Score System Testing

| Test Case | Result | Notes |
|---|---|---|
| Load from valid file | ✅ | |
| Load from missing file | ✅ Returns `[]` | |
| Load from corrupt file | ✅ Returns `[]` | |
| Save and re-load | ✅ | |
| Top 10 enforcement | ✅ | 11th entry dropped |
| Sorting (descending) | ✅ | |
| Negative score validation | ❌ **Accepted** | Should be rejected per subject |
| Non-integer score validation | ❌ **Accepted** | Should be rejected per subject |
| Name > 10 chars validation | ❌ **Accepted** | 20-char name stored without truncation |
| Name character validation | ❌ **Accepted** | No filtering on the storage side |

> [!IMPORTANT]
> The game's UI correctly limits name input to 10 alphanumeric+space characters. But the `add_high_score()` function has **zero validation**, so a manually edited `pc.json` (or a programmatic call) can inject invalid data.

---

## README Compliance

| Required Section | Present? | Notes |
|---|---|---|
| First line: italicized activity credit | ✅ | `*This activity has been created as part of the 42 curriculum by aalrousa, ybarakat.*` |
| Description section | ✅ | |
| Instructions section | ✅ | With install, run, debug, lint, clean |
| Resources section | ✅ | References + AI usage statement |
| Configuration section | ✅ | Full schema table with defaults |
| Highscore section | ✅ | Explains persistence, validation, top 10, rationale |
| Maze Generation section | ✅ | Package integration, seed progression, wall encoding |
| Implementation section | ✅ | Per-file technical summary |
| General Software Architecture | ✅ | Mermaid diagram + module responsibilities |
| Project Management section | ✅ | With link to directory |
| Written in English | ✅ | |

---

## Makefile Compliance

| Rule | Present? | Correct? |
|---|---|---|
| `install` | ✅ | Installs pygame, flake8, mypy, and the `.whl` file |
| `run` | ✅ | `python3 game.py config.json` |
| `debug` | ✅ | `python3 -m pdb game.py config.json` |
| `clean` | ✅ | Removes `__pycache__`, `.mypy_cache`, `*.pyc` |
| `lint` | ✅ | `flake8 .` and `mypy` with required flags |
| `lint-strict` (optional) | ✅ | `mypy . --strict` |

---

## Project Management Docs

All 4 documents present in [project_management/](file:///home/rsn026/Desktop/Pacman/project_management):

| Document | Quality | Notes |
|---|---|---|
| [TIMELINE.md](file:///home/rsn026/Desktop/Pacman/project_management/TIMELINE.md) | ✅ Good | 5 phases derived from git history, with dates |
| [TEAM_ORG.md](file:///home/rsn026/Desktop/Pacman/project_management/TEAM_ORG.md) | ✅ Good | Per-file commit attribution with roles |
| [RISK_ANALYSIS.md](file:///home/rsn026/Desktop/Pacman/project_management/RISK_ANALYSIS.md) | ✅ Excellent | Realized + standing risks, honest about gaps |
| [TEST_PLAN.md](file:///home/rsn026/Desktop/Pacman/project_management/TEST_PLAN.md) | ✅ Good | Manual test checklist covering golden path, edge cases, cheats |

> [!NOTE]
> The risk analysis honestly acknowledges the lack of automated tests, non-random level seeds, and commit message quality issues — shows good self-awareness.

---

## Risk Summary for Peer Review

### Things a reviewer will likely catch immediately

1. **`make lint` fails** — 11 flake8 violations. Fix these before defense.
2. **Entry point name** — Subject says `pac-man.py`, you have `game.py`. The Makefile works, but a reviewer running the subject's exact command will get `No such file`.
3. **Arabic names in `pc.json`** — Visible evidence that non-ASCII is accepted.

### Things a reviewer might test

4. **Level randomness** — Playing levels 2+ twice reveals identical mazes.
5. **Ghost timers during pause** — Edible/respawn countdown continues while ESC-paused.
6. **Config modification during defense** — The subject says *"The game configuration will be updated during the defense."* If they set `"levels": []` or extreme values, there could be crashes.

### Things that are correct and defensible

- All 6 cheat mode toggles work correctly
- Config parser handles every error gracefully
- High score persistence, loading, and top-10 enforcement all work
- Ghost AI (BFS chase, Manhattan escape, respawn) is sound
- Score never decreases
- Lives, score, and level carry over between levels
- Interpolated rendering is smooth

---

*Report generated by automated code analysis and manual review. No files were modified.*
