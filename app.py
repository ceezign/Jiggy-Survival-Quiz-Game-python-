"""Gradio interface for the quiz game """

import gradio as gr
from models import Quiz
from utils import fetch_questions, update_leaderboard, load_leaderboard


# Game Functions
def start_quiz(username, difficulty, num_questions):
    if not username:
        return None, "⚠️ Please enter a username.", "", "", "", "", "", ""

    questions = fetch_questions(num_questions, difficulty)
    quiz = Quiz(questions, username, difficulty)

    question_text, options = quiz.get_current_question()
    return (
        quiz,
        f"**{question_text}**",
        options[0], options[1], options[2], options[3],
        f"Score: {quiz.score}",
        "✅ Game Started!"
    )


def submit_answer(choice, quiz):
    if not quiz:
        return (None, "⚠️ No active quiz. Please start again.",
                "", "", "", "", "", "")

    correct = quiz.questions[quiz.current_index].answer
    if choice.strip().lower() == correct.strip().lower():
        quiz.score += 1
        quiz.current_index += 1
        if quiz.current_index < len(quiz.questions):
            q_text, options = quiz.get_current_question()
            return (
                quiz,
                f"**{q_text}**",
                options[0], options[1], options[2], options[3],
                f"Score: {quiz.score}",
                "✅ Correct!"
            )
        else:
            result = quiz.summary()
            update_leaderboard(result)
            return (
                None,
                f"🎉 You completed all {len(quiz.questions)} questions!",
                "", "", "", "",
                f"Final Score: {quiz.score}",
                "🏆 Game Over"
            )
    else:
        result = quiz.summary()
        update_leaderboard(result)
        return (
            None,
            f"❌ Wrong Answer! The correct answer was: {correct}",
            "", "", "", "",
            f"Final Score: {quiz.score}",
            "💀 Game Over"
        )


def show_leaderboard():
    leaderboard = load_leaderboard()
    if not leaderboard:
        return "No scores yet."
    lines = []
    for i, entry in enumerate(leaderboard, start=1):
        lines.append(
            f"{i}. {entry['username']} — {entry['score']} pts "
            f"({entry['difficulty']}) in {entry['time']}s"
        )
    return "\n".join(lines)


# Gradio UI
with gr.Blocks(css=".gradio-container {font-family: Arial; background: #f9f9f9;}") as demo:
    gr.Markdown("# 🎮 Jiggy Survival Quiz Game")
    gr.Markdown("Answer until you lose! 🚀")

    with gr.Row():
        username = gr.Textbox(label="Enter Username")
        difficulty = gr.Dropdown(["easy", "medium", "hard"], value="easy",
                                 label="Difficulty")
        num_questions = gr.Slider(5, 20, step=1, value=5,
                                  label="Number of Questions")
        start_btn = gr.Button("Start Quiz", variant="primary")

    quiz_state = gr.State()
    question_md = gr.Markdown()
    opt1 = gr.Button("", visible=True)
    opt2 = gr.Button("", visible=True)
    opt3 = gr.Button("", visible=True)
    opt4 = gr.Button("", visible=True)
    score_md = gr.Markdown("Score: 0")
    feedback_md = gr.Markdown()

    gr.Markdown("## 🏆 Leaderboard")
    leaderboard_md = gr.Markdown(show_leaderboard())

    # Events
    start_btn.click(
        start_quiz,
        inputs=[username, difficulty, num_questions],
        outputs=[quiz_state, question_md, opt1, opt2, opt3, opt4, score_md,
                 feedback_md]
    )

    for btn in [opt1, opt2, opt3, opt4]:
        btn.click(
            submit_answer,
            inputs=[btn, quiz_state],
            outputs=[quiz_state, question_md, opt1, opt2, opt3, opt4, score_md, feedback_md]
        ).then(show_leaderboard, outputs=[leaderboard_md])

demo.launch()