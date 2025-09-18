""" Fetching questions and managing leaderboard"""

import requests, random, html, os, json
from models import Question

LEADERBOARD_FILE = "leaderboard.json"

# leaderboard ----

def load_leaderboard():
    """Load leaderboard from file (or return empty list)"""
    if not os.path.exists(LEADERBOARD_FILE):
        return []
    with open(LEADERBOARD_FILE, "r") as file:
        json.dump(file)

def save_leaderboard(data):
    """Save leaderboard list to a json file."""
    with open(LEADERBOARD_FILE, "w") as file:
        json.dump(data, file, indent=2)

def update_leaderboard(entry: dict):
    """Add new entry and return top 10."""
    data = load_leaderboard()
    data.append(entry)
    data.sort(key=lambda x: (-x["score"], x["time_taken"]))
    save_leaderboard(data)
    return data[:10]

# Question Fetching

def fetch_question(num: int=20, difficulty: str="medium"):
    """
    Fetch question from OpenTriviaDB API.
    Default: 20 random multiple-choice questions.
    Difficulty: easy, medium, hard
    """
    url = f"https://opentdb.com/api.php?amount={num}&difficulty={difficulty}&type=multiple"
    response = requests.get(url)
    data = response.json()

    questions = []

    for item in data["results"]:
        question_text = html.unescape(item["question"])
        correct = html.unescape(item["correct_answer"])
        incorrect = [html.unescape(x) for x in item["incorrect_answers"]]

        options = incorrect + [correct]
        random.shuffle(options)

        answer_index = options.index(correct)

        questions.append(Question(question_text, options, answer_index))
        return questions