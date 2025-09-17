""" Contain core classes: Question and Quiz"""

from dataclasses import dataclass
from typing import List, Dict, Any, Optional
import time

@dataclass
class Question:
    """ Represents one multiple-choice question"""
    text: str
    option: List[str]
    answer: int

class Quiz:
    """ Manages the quiz logic in SURVIVAL MODE:
    - User keeps answering until they get one wrong
    - Score increases for each correct answer.
    """
    def __init__(self, questions: List[Question], username: str, difficulty: str):
        if not questions:
            raise ValueError("Quiz must have at least one question")
        self.questions = questions
        self.username = username
        self.difficulty = difficulty
        self.index = 0
        self.score = 0
        self.start_time: Optional[float] = None
        self.end_time: Optional[float] = None

    def next_question(self)-> Optional[Question]:
        """ Return current question (without advancing)."""
        if self.start_time is None:
            self.start_time = time.time()
        if self.index < len(self.questions):
            return self.questions[self.index]
        return None

    def submit(self, choice: int)->Dict[str, Any]:
        """ Submit answer choice (0-based index).
        - if wrong: quiz ends immediately.
        - if correct: score++, advance to next question.
        """

        if self.index >= len(self.questions):
            return {"Finished": True, "message": "Quiz already finished"}

        q = self.questions[self.index]
        is_correct = (choice == q.answer)

        if is_correct:
            self.index += 1
            self.score += 1
            if self.index >= len(self.questions):
                self.end_time = time.time()
                return {"is_correct": True, "finished": True, "next_question": None}
            else:
                return {"is_correct": True, "finished": False,
                        "next_question": self.questions[self.index]}
        else:
            self.end_time = time.time()
            return {"is_correct": False, "finished": True, "next_question": None}

    def summary(self):
        """Return Final game stats."""

        total = len(self.questions)
        time_taken = (self.end_time or time.time()) - (self.start_time or time.time())

        return {
            "Username": self.username,
            "Difficulty": self.difficulty,
            "Score": self.score,
            "_questions": total,
            "Accuracy": (self.score / total * 100.0) if total else 0.0,
            "Time_taken": round(time_taken, 1)
        }