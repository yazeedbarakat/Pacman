import json
import sys
from typing import Dict,Any


def read_config(filename: str) -> Dict[str, Any]:

    try:
        with open(filename, 'r') as file:
            lines = file.readlines()

            v_lines = []
            for i in lines:
                if not i.strip().startswith('#'):
                    v_lines.append(i)
            
            clear_sp = ''.join(v_lines)

            # str to dict
            config_data = json.loads(clear_sp)

            return config_data

    except FileNotFoundError:
        print(f"Error: The configuration file '{filename}' could not be found.")
        sys.exit(0)
    except json.JSONDecodeError as e:
        print(f"Error: The file '{filename}' contains invalid JSON formatting. Details: {e}")
        sys.exit(0)
    except Exception as e:
        print(f"An unexpected error occurred while reading the file: {e}")
        sys.exit(0)



if __name__ == "__main__":
    # Check if exactly one argument (the config file) is provided
    if len(sys.argv) != 2:
        print("Usage: python3 pac-man.py <config_file.json>")
        sys.exit(0)

    # Get the filename from the command line arguments
    config_file = sys.argv[1]

    # Call your function to read and parse the file[cite: 4]
    config = read_config(config_file)

    # Print the extracted data to prove it works[cite: 3]
    print("--- Configuration Loaded Successfully ---")
    print(f"Highscore File: {config.get('highscore_filename')}")
    print(f"Lives: {config.get('lives')}")
    print(f"Pacgum Points: {config.get('points_per_pacgum')}")
    print(f"Seed: {config.get('seed')}")
    print(f"Level Max Time: {config.get('level_max_time')} seconds")

    # You can also check how many levels were loaded from the list[cite: 3]
    levels = config.get('levels', [])
    print(f"Total Levels Loaded: {len(levels)}")
