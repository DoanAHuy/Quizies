import tkinter as tk
import ttkbootstrap as ttk
import random
from DATA import questions

# ---------------- Global Variables ---------------- #
question_text = tk.StringVar()
choices = [tk.StringVar() for _ in range(4)]
feedback_text = tk.StringVar()
score_text = tk.StringVar(value="Score: 0")
progress_text = tk.StringVar(value="Question 0")
progress_value = tk.IntVar(value=0)
user_selected = tk.IntVar(value=0)

score = 0
current_question = None

# ---------------- Core Functions ---------------- #

def start_game():
    """Reset quiz state and load first question."""
    global score
    score = 0
    progress_value.set(0)
    score_text.set("Score: 0")
    progress_text.set("Question 0")
    load_question()

def load_question():
    """Load a random question from DATA."""
    global current_question
    current_question = random.choice(questions)
    question_text.set(current_question["question"])
    for i, opt in enumerate(current_question["options"]):
        choices[i].set(opt)
    feedback_text.set("")
    user_selected.set(0)

def set_choices(choice):
    """Record user selection."""
    user_selected.set(choice)

def validate_answer():
    """Check answer and update score."""
    global score
    selected = user_selected.get()
    if selected == current_question["answer"]:
        feedback_text.set("Correct ✅")
        score += 5
        score_text.set(f"Score: {score}")
    else:
        feedback_text.set("Wrong ❌")

def next_question():
    """Validate and move to next question or summary."""
    validate_answer()
    progress_value.set(progress_value.get() + 1)
    progress_text.set(f"Question {progress_value.get()}")
    if progress_value.get() < len(questions):
        load_question()
    else:
        show_summary_window()

# ---------------- UI Functions ---------------- #

def create_widgets(parent):
    """Build quiz UI inside parent frame."""

    # Question
    question_frame = tk.Frame(parent, bg="#98FF98", padx=15, pady=15)
    question_frame.pack(fill="x", pady=10)

    tk.Label(question_frame, textvariable=question_text,
             font=("Segoe UI", 16, "bold"), bg="#98FF98").pack(pady=10)

    # Choices
    for i in range(4):
        tk.Button(parent, textvariable=choices[i],
                  width=40, bg="#98FF98", fg="black",
                  command=lambda idx=i+1: set_choices(idx)).pack(pady=5)

    # Feedback
    tk.Label(parent, textvariable=feedback_text,
             font=("Segoe UI", 12, "bold"), bg="#98FF98").pack(pady=10)

    # Score + Progress
    status_frame = tk.Frame(parent, bg="#98FF98", padx=10, pady=10)
    status_frame.pack(fill="x", pady=10)

    tk.Label(status_frame, textvariable=score_text,
             font=("Segoe UI", 12, "bold"), bg="#98FF98").pack(side="left", padx=10)

    tk.Label(status_frame, textvariable=progress_text,
             font=("Segoe UI", 12), bg="#98FF98").pack(side="right", padx=10)

    # Progress bar
    ttk.Progressbar(parent, orient="horizontal", mode="determinate",
                    length=400, maximum=len(questions),
                    variable=progress_value, bootstyle="success").pack(pady=10)

    # Navigation
    nav_frame = tk.Frame(parent, bg="#98FF98", padx=10, pady=10)
    nav_frame.pack(fill="x", pady=10)

    ttk.Button(nav_frame, text="Next ➡", bootstyle="info",
               command=next_question).pack(side="right", padx=10)

    ttk.Button(nav_frame, text="Quit ✖", bootstyle="danger",
               command=parent.quit).pack(side="left", padx=10)

def show_summary_window():
    """Display final score with scrollable summary."""
    sum_win = tk.Toplevel()
    sum_win.title("Quiz Summary")
    sum_win.geometry("500x400")

    frame = ttk.Frame(sum_win, padding=10)
    frame.pack(fill="both", expand=True)

    text_frame = ttk.Frame(frame)
    text_frame.pack(fill="both", expand=True)

    scrollbar = ttk.Scrollbar(text_frame, orient="vertical")
    scrollbar.pack(side="right", fill="y")

    answer_text = tk.Text(text_frame, wrap="word",
                          yscrollcommand=scrollbar.set,
                          font=("Segoe UI", 12))
    answer_text.pack(fill="both", expand=True)
    scrollbar.config(command=answer_text.yview)

    answer_text.insert("1.0", f"Final Score: {score}\n")
    answer_text.insert("end", "Thanks for playing!\n")
    answer_text.config(state="disabled")

    nav_frame = ttk.Frame(sum_win, padding=10)
    nav_frame.pack(fill="x")

    ttk.Button(nav_frame, text="Play Again 🔄", bootstyle="success",
               command=lambda: restart_quiz(sum_win)).pack(side="left", padx=10)

    ttk.Button(nav_frame, text="Close ✖", bootstyle="danger",
               command=sum_win.destroy).pack(side="right", padx=10)

def restart_quiz(window):
    """Restart quiz after summary."""
    window.destroy()
    start_game()

def create_main_window():
    """Start screen then quiz."""
    global root
    root = ttk.Window(themename="cosmo")
    root.title("Quizies")
    root.geometry("700x500")
    root.configure(bg="#98FF98")

    start_frame = tk.Frame(root, bg="#98FF98", padx=50, pady=50)
    start_frame.pack(fill="both", expand=True)

    tk.Label(start_frame, text="Press here to start",
             font=("Segoe UI", 20, "bold"), bg="#98FF98").pack(pady=20)

    ttk.Button(start_frame, text="Start Quiz ▶", bootstyle="success",
               command=lambda: start_game_ui(start_frame)).pack(pady=10)

    root.mainloop()

def start_game_ui(start_frame):
    """Destroy start screen and launch quiz UI."""
    start_frame.destroy()
    main_frame = tk.Frame(root, bg="#98FF98", padx=20, pady=20)
    main_frame.pack(fill="both", expand=True)
    create_widgets(main_frame)
    start_game()

# ---------------- Run App ---------------- #
if __name__ == "__main__":
    create_main_window()