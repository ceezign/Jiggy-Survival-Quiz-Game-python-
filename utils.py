"""Helper functions for fetching questions and managing leaderboard."""

import requests
import json
import random
from models import Question

LEADERBOARD_FILE = "leaderboard.json"


def fetch_questions(num: int, difficulty: str):
    """Fetch num questions from OpenTrivia API"""
    url = (f"https://opentdb.com/api.php?amount={num}&difficulty={difficulty}&"
           f"type=multiple")
    response = requests.get(url)
    data = response.json()

    questions = []
    for item in data["results"]:
        question_text = item["question"]
        correct = item["correct_answer"]
        options = item["incorrect_answers"] + [correct]
        random.shuffle(options)
        questions.append(Question(question_text, options, correct))

    return questions


def load_leaderboard():
    try:
        with open(LEADERBOARD_FILE, "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return []


def update_leaderboard(entry: dict):
    leaderboard = load_leaderboard()
    leaderboard.append(entry)

    # sort by score (desc), then by time (asc)
    leaderboard.sort(key=lambda x: (-x["score"], x["time"]))

    leaderboard = leaderboard[:10]  # keep top 10
    with open(LEADERBOARD_FILE, "w") as file:
        json.dump(leaderboard, file, indent=2)

    return leaderboard