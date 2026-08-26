"""Persistent highscore storage for the Pacman game.

Loads, saves, and updates the top-10 highscore list kept as a JSON
file on disk, tolerating missing or unreadable files.
"""

import json
from typing import Any


def save_high_scores(file_name: str, scores: list[dict[str, Any]]) -> None:
    """Write the high score list to a JSON file, printing on failure.

    Args:
        file_name: Path to the JSON file to write.
        scores: List of {'name': str, 'score': int} entries to save.
    """
    try:
        with open(file_name, 'w') as file:
            json.dump(scores, file)
    except Exception as e:
        print(f"Error saving high scores: {e}")


def load_high_scores(file_name: str) -> list[dict[str, Any]]:
    """Read the high score list from a JSON file.

    Args:
        file_name: Path to the JSON file to read.

    Returns:
        The list of {'name': str, 'score': int} entries, or an empty
        list if the file is missing or unreadable.
    """
    try:
        with open(file_name, 'r') as file:
            loaded: list[dict[str, Any]] = json.load(file)
            return loaded
    except Exception as e:
        print(f"Error loading high scores: {e}")
        return []


def add_high_score(file_name: str, name: str, score: int) -> None:
    """Insert a new score, keep the top 10, and persist the list.

    Args:
        file_name: Path to the JSON high score file.
        name: Player name to record.
        score: Player score to record.
    """
    high_scores = load_high_scores(file_name)
    high_scores.append({'name': name, 'score': score})
    high_scores = sorted(
        high_scores, key=lambda entry: entry['score'], reverse=True)[:10]
    save_high_scores(file_name, high_scores)
