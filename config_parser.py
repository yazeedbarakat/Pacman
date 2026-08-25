import json
import sys
from typing import Dict, Any


DEFAULT_CONFIG = {
    "highscore_filename": "highscore.json",
    "levels": [],
    "lives": 3,
    "pacgum": 42,
    "points_per_pacgum": 10,
    "points_per_super_pacgum": 50,
    "points_per_ghost": 200,
    "seed": 42,
    "level_max_time": 90
}


def read_config(filename: str) -> Dict[str, Any]:
    """Load and validate the game config from a JSON file with '#' comments.

    Missing or mistyped keys fall back to DEFAULT_CONFIG, each with a
    printed warning, so a bad config file degrades instead of crashing.

    Args:
        filename: Path to the JSON config file to read.

    Returns:
        A config dict containing every key from DEFAULT_CONFIG, using
        values from the file where present and valid.
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
                if key in config_data:
                    if isinstance(config_data[key], type(default_val)):
                        valid_config[key] = config_data[key]
                    else:
                        exp_type = type(default_val).__name__
                        msg = (
                            f"Warning: Invalid type for '{key}'. "
                            f"Expected {exp_type}. Using default: "
                            f"{default_val}"
                        )
                        print(msg)
                else:
                    msg = (
                        f"Warning: Missing key '{key}'. "
                        f"Using default: {default_val}"
                    )
                    print(msg)

            return valid_config

    except FileNotFoundError:
        print(f"Error: Configuration file '{filename}' could not be found.")
        sys.exit(0)
    except json.JSONDecodeError as e:
        print(
            f"Error: File '{filename}' contains invalid JSON. Details: {e}"
        )
        sys.exit(0)
    except Exception as e:
        print(f"An unexpected error occurred while reading file: {e}")
        sys.exit(0)
