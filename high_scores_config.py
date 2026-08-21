import json

def save_high_scores(file_name: str, scores: list):
    try:
        with open(file_name, 'w') as file:
            json.dump(scores, file)
    except Exception as e:
        print(f"Error saving high scores: {e}")

def load_high_scores(file_name: str):
    try:
        with open(file_name, 'r') as file:
            return json.load(file)
    except Exception as e:
        print(f"Error loading high scores: {e}")
        return []

def add_high_score(file_name: str, name: str, score: int):
    high_scores = load_high_scores(file_name)
    high_scores.append({'name': name, 'score': score})
    save_high_scores(file_name, high_scores)
