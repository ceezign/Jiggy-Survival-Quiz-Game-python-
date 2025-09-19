# 🎮 Jiggy Survival Quiz Game

An interactive quiz web app built with Python classes and a Gradio web interface.
Play in Survival Mode — keep answering until you lose!

⸻

🚀 Features
 • Fetches live questions from OpenTriviaDB API (https://opentdb.com/)
 • Choose your username, difficulty (easy / medium / hard), and number of questions
 • Survival gameplay — one wrong answer ends the game
 • Leaderboard (saved locally in leaderboard.json)
 • Tracks score, time taken, difficulty
 • Clean modular codebase

![Jiggy Survival Quiz Game Demo](images/screenshot.png) (images/screenshot.png)
![](images/screenshot1.png)

🧩 Code Overview

models.py
 • Question: holds text, options, correct answer.
 • Quiz: manages state — current question, score, next question, check answers, 
      and summary.

utils.py
 • fetch_questions(n, difficulty): pulls multiple-choice questions from OpenTrivia API.
 • load_leaderboard(): loads leaderboard from leaderboard.json.
 • update_leaderboard(entry): saves new score, sorts top 10 by score/time.

main.py
 • start_quiz(): initializes a new quiz with username, difficulty, and question count.
 • submit_answer(): checks the answer, updates score, or ends game on wrong choice.
 • show_leaderboard(): displays formatted leaderboard.
 • Gradio UI: provides text input for username, dropdown for difficulty, slider for question count, clickable answer buttons, live score, feedback, and leaderboard.

⸻
![](images/screenshot2.png)
![](images/screenshot3.png)


🏆 Leaderboard

Leaderboard is automatically saved to leaderboard.json.

📌 Example Flow
 1. Enter username: Jiggy
 2. Select difficulty: medium
 3. Choose number of questions: 10
 4. Click answers until wrong ❌
 5. View final score + updated leaderboard 🏆

⸻

🛠 Future Improvements
 • Add categories (Sports, History, Science, etc.)
 • Separate leaderboards per difficulty
 • Add timer per question
 • Multiplayer or tournament mode