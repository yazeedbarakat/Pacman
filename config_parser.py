import json
import sys
from typing import Dict, Any

DEFAULT_CONFIG = {
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

def read_config(filename: str) -> Dict[str, Any]:
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
                    print(f"Warning: Missing key '{key}'. Using default: {default_val}")
                    continue
                
                val = config_data[key]

                if not isinstance(val, type(default_val)):
                    print(f"Warning: Invalid type for '{key}'. Expected {type(default_val)}. Using default: {default_val}")
                    continue
                
                if type(default_val) in (int, float) and val < 0:
                    print(f"Warning: Negative value for '{key}'. Using default: {default_val}")
                    continue

                if key == "levels":
                    valid_levels = []
                    i = 0
                    for level in val:
                        w = level.get("width", 20)
                        h = level.get("height", 15)

                        if w < 0: 
                            print(f"Warning: Negative width in level {i+1}. Using default: 20.")
                            w = 20
                        if h < 0: 
                            print(f"Warning: Negative height in level {i+1}. Using default: 15.")
                            h = 15

                        valid_levels.append({"width": w, "height": h})
                        i += 1
                        
                    valid_config[key] = valid_levels
                    continue

                valid_config[key] = val

            return valid_config

    except FileNotFoundError:
        print(f"Error: Configuration file '{filename}' could not be found. Using default values.")
        return dict(DEFAULT_CONFIG)
    except json.JSONDecodeError as e:
        print(f"Error: File '{filename}' contains invalid JSON. Details: {e}. Using default values.")
        return dict(DEFAULT_CONFIG)
    except Exception as e:
        print(f"An unexpected error occurred while reading file: {e}. Using default values.")
        return dict(DEFAULT_CONFIG)
