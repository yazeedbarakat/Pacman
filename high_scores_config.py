import json
from typing import Any


def save_high_scores(file_name: str, scores: list[dict[str, Any]]) -> None:
    try:
        with open(file_name, 'w') as file:
            json.dump(scores, file)
    except Exception as e:
        print(f"Error saving high scores: {e}")


def load_high_scores(file_name: str) -> list[dict[str, Any]]:
    try:
        with open(file_name, 'r') as file:
            loaded: list[dict[str, Any]] = json.load(file)
            return loaded
    except Exception as e:
        print(f"Error loading high scores: {e}")
        return []


def add_high_score(file_name: str, name: str, score: int) -> None:
    high_scores = load_high_scores(file_name)
    high_scores.append({'name': name, 'score': score})
    high_scores = sorted(high_scores, key=lambda entry: entry['score'], reverse=True)[:10]
    save_high_scores(file_name, high_scores)
