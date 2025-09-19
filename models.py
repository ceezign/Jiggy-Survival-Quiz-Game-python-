""" Contain core classes: Question and Qiz """
import time


class Question:
    """Represents one multiple-choice question"""
    def __init__(self, text: str, options: list[str], answer: str):
        self.text = text
        self.options = options
        self.answer = answer  # correct answer string


class Quiz:
    """
    Manages the quiz logic in SURVIVAL MODE:
    - User answer till they get one wrong
    - Score increases for each correct answer
    """
    def __init__(self, questions: list[Question], username: str, difficulty: str):
        self.questions = questions
        self.username = username
        self.difficulty = difficulty
        self.current_index = 0
        self.score = 0
        self.start_time = time.time()

    def get_current_question(self):
        """Return current question text and options"""
        if self.current_index < len(self.questions):
            q = self.questions[self.current_index]
            return q.text, q.options
        return None, None

    def check_answer(self, choice: str):
        """Check if answer is correct"""
        question = self.questions[self.current_index]
        return choice.strip().lower() == question.answer.strip().lower()

    def next_question(self):
        """Move to next question"""
        self.current_index += 1
        return self.get_current_question()

    def summary(self):
        """Return quiz result summary"""
        elapsed = round(time.time() - self.start_time, 2)
        return {
            "username": self.username,
            "difficulty": self.difficulty,
            "score": self.score,
            "total": len(self.questions),
            "time": elapsed,
        }