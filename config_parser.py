"""Configuration parser for Pacman game settings.

Reads and validates game configuration from a JSON file, supporting
comment lines (prefixed with '#') and falling back to sensible defaults
for any missing or invalid values.
"""

import json
from typing import Dict, Any

# Default configuration values for the Pacman game.
DEFAULT_CONFIG: Dict[str, Any] = {
    "highscore_filename": "pc.json",
    "levels": [
        {"width": 20, "height": 15},
        {"width": 20, "height": 15},
        {"width": 20, "height": 15},
        {"width": 20, "height": 15},
        {"width": 20, "height": 15},
        {"width": 20, "height": 15},
        {"width": 20, "height": 15},
        {"width": 20, "height": 15},
        {"width": 20, "height": 15},
        {"width": 20, "height": 15}
    ],
    "lives": 3,
    "pacgum": 42,
    "points_per_pacgum": 10,
    "points_per_super_pacgum": 50,
    "points_per_ghost": 200,
    "seed": 42,
    "level_max_time": 90
}

# Maze sizes outside these bounds break the generator or overflow the
# 1920x1080 window, so level dimensions are clamped into them.
MIN_WIDTH, MAX_WIDTH = 15, 30
MIN_HEIGHT, MAX_HEIGHT = 11, 24


def read_config(filename: str) -> Dict[str, Any]:
    """Read and validate a game configuration file.

    Loads a JSON configuration file, strips comment lines (lines starting
    with '#'), and validates each key against DEFAULT_CONFIG. Missing keys,
    invalid types, and negative numeric values are replaced with their
    corresponding defaults, with warnings printed to stdout.

    For the 'levels' key, each level's width and height are individually
    validated and clamped to defaults if negative.

    Args:
        filename: Path to the JSON configuration file.

    Returns:
        A dictionary of validated configuration values. If the file cannot
        be read or parsed, a copy of DEFAULT_CONFIG is returned.
    """
    try:
        with open(filename, 'r') as file:
            lines = file.readlines()

            v_lines = []
            for line in lines:
                if not line.strip().startswith('#'):
                    v_lines.append(line)

            clear_sp = ''.join(v_lines)
            config_data = json.loads(clear_sp)
            valid_config = dict(DEFAULT_CONFIG)

            for key, default_val in DEFAULT_CONFIG.items():
                if key not in config_data:
                    print(f"Warning: Missing key '{key}'. "
                          f"Using default: {default_val}")
                    continue

                val = config_data[key]

                if not isinstance(val, type(default_val)):
                    print(f"Warning: Invalid type for '{key}'. Expected "
                          f"{type(default_val)}. Using default: {default_val}")
                    continue

                if type(default_val) in (int, float) and val < 0:
                    print(f"Warning: Negative value for '{key}'. "
                          f"Using default: {default_val}")
                    continue

                if key == "levels":
                    valid_config[key] = validate_levels(val)
                    continue

                valid_config[key] = val

            return valid_config

    except FileNotFoundError:
        print(f"Error: Configuration file '{filename}' could not be found. "
              "Using default values.")
        return dict(DEFAULT_CONFIG)
    except json.JSONDecodeError as e:
        print(f"Error: File '{filename}' contains invalid JSON. "
              f"Details: {e}. Using default values.")
        return dict(DEFAULT_CONFIG)
    except Exception as e:
        print(f"An unexpected error occurred while reading file: {e}. "
              "Using default values.")
        return dict(DEFAULT_CONFIG)


def validate_levels(levels: list) -> list[Dict[str, int]]:
    """Validate a config 'levels' list, clamping each entry to safe values.

    Non-dict entries and non-integer or out-of-range dimensions are
    replaced with the 20x15 defaults, with a warning printed for each.

    Args:
        levels: The raw 'levels' value from the config file.

    Returns:
        A list of {'width': int, 'height': int} entries safe to play.
    """
    valid_levels = []
    for i, level in enumerate(levels):
        if not isinstance(level, dict):
            print(f"Warning: Level {i + 1} is not an object. "
                  "Using default: 20x15.")
            valid_levels.append({"width": 20, "height": 15})
            continue
        w = level.get("width", 20)
        h = level.get("height", 15)
        if not isinstance(w, int) or not MIN_WIDTH <= w <= MAX_WIDTH:
            print(f"Warning: Invalid width in level {i + 1} "
                  f"(allowed: {MIN_WIDTH}-{MAX_WIDTH}). Using default: 20.")
            w = 20
        if not isinstance(h, int) or not MIN_HEIGHT <= h <= MAX_HEIGHT:
            print(f"Warning: Invalid height in level {i + 1} "
                  f"(allowed: {MIN_HEIGHT}-{MAX_HEIGHT}). Using default: 15.")
            h = 15
        valid_levels.append({"width": w, "height": h})
    return valid_levels
