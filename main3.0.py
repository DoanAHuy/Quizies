import tkinter as tk
import ttkbootstrap as ttk
import pyglet
import random
from DATA import questions

# Variables
pyglet.font.add_directory("MicrosoftAptosFonts")# font path
pyglet.options['win32_gdi_font'] = True #fix font path
FILENAME="answer.txt"


root = ttk.Window(themename="cosmo")
root.title("Quizies")
root.geometry("700x500")
root.configure(bg="#98FF98")

question_text = tk.StringVar()
root.O1 = tk.StringVar()
root.O2 = tk.StringVar()
root.O3 = tk.StringVar()
root.O4 = tk.StringVar()
feedback_text = tk.StringVar()
score_text = tk.StringVar(value="Score: 0")
progress_text = tk.StringVar(value="Question 0")
progress_value = tk.IntVar(value=0)
user_selected = tk.IntVar(value=0)

score = 0
question_index=[]
current_question = None

#Functions

def start_game():
    global score
    score = 0
    progress_value.set(0)
    score_text.set("Score: 0")
    progress_text.set("Question 0")
    load_question()
    question_index.clear()
    with open(FILENAME, "w", encoding="utf-8") as f:
        f.write("")
def load_question():
    global current_question
    if len(question_index) == len(questions):
        show_summary_window()
        return
    while True:
        index = random.randint(0, len(questions) - 1)
        if index not in question_index:
            question_index.append(index)
            current_index = index
            break
    current_question = questions[current_index]
    question_text.set(current_question["Quest"])
    # pair choices with data.py
    root.choices = current_question["Options"].copy()
    random.shuffle(root.choices)
    root.O1.set(root.choices[0])
    root.O2.set(root.choices[1])
    root.O3.set(root.choices[2])
    root.O4.set(root.choices[3])
    feedback_text.set("")
    user_selected.set(0)

def set_choices(choice):
    user_selected.set(choice)

def validate_answer():
    global score
    selected = user_selected.get()
    correct_option = current_question["Answer"]

    # Determine correctness
    if selected == correct_option:
        feedback_text.set("Correct")
        score += 5
        score_text.set(f"Score: {score}")
        result = "Correct"
    else:
        feedback_text.set("Wrong")
        result = "Wrong"

    # Record to file
    with open(FILENAME, "a", encoding="utf-8") as f:
        f.write(f"Q: {current_question['Quest']}\n")
        f.write(f"Your answer: {root.choices[selected-1] if selected else 'None'}\n")
        f.write(f"Correct answer: {current_question['Answer']}\n")
        f.write(f"Result: {result}\n\n")

def next_question():
    validate_answer()
    progress_value.set(progress_value.get() + 1)
    progress_text.set(f"Question {progress_value.get()}")
    if progress_value.get() < len(questions):
        load_question()
    else:
        show_summary_window()

# ---------------- UI Functions ---------------- #

def create_widgets(parent):
    # Question
    question_frame = tk.Frame(parent, bg="#98FF98", padx=15, pady=15)
    question_frame.pack(fill="x", pady=10)

    tk.Label(question_frame, textvariable=question_text,
             font=("Aptos ExtraBold", 16, "bold"), bg="#98FF98").pack(pady=10)
    #Buttons
    buttons_frame = tk.Frame(parent, bg="#98FF98", padx=15, pady=15)
    buttons_frame.pack(fill="x", pady=10)
    buttons_frame['borderwidth'] = 5
    buttons_frame['relief'] = 'solid'
    # Create multiple choices
    root.Button1 = ttk.Radiobutton(buttons_frame, style='custom.Toolbutton', textvariable=root.O1,
                                   variable=user_selected, value=1, command=lambda: set_choices(1))
    root.Button2 = ttk.Radiobutton(buttons_frame, style='custom.Toolbutton', textvariable=root.O2,
                                   variable=user_selected, value=2, command=lambda: set_choices(2))
    root.Button3 = ttk.Radiobutton(buttons_frame, style='custom.Toolbutton', textvariable=root.O3,
                                   variable=user_selected, value=3, command=lambda: set_choices(3))
    root.Button4 = ttk.Radiobutton(buttons_frame, style='custom.Toolbutton', textvariable=root.O4,
                                   variable=user_selected, value=4, command=lambda: set_choices(4))

    root.Button1.grid(column=0, row=0, sticky='w', padx=20, pady=5)
    root.Button2.grid(column=0, row=1, sticky='w', padx=20, pady=5)
    root.Button3.grid(column=0, row=2, sticky='w', padx=20, pady=5)
    root.Button4.grid(column=0, row=3, sticky='w', padx=20, pady=5)
    # Feedback
    tk.Label(parent, textvariable=feedback_text,
             font=("Aptos ExtraBold", 12, "bold"), bg="#98FF98").pack(pady=10)

    # Score + Progress
    status_frame = tk.Frame(parent, bg="#98FF98", padx=10, pady=10)
    status_frame.pack(fill="x", pady=10)

    tk.Label(status_frame, textvariable=score_text,
             font=("Aptos ExtraBold", 12, "bold"), bg="#98FF98").pack(side="left", padx=10)

    tk.Label(status_frame, textvariable=progress_text,
             font=("Aptos ExtraBold", 12), bg="#98FF98").pack(side="right", padx=10)

    # Progress bar
    ttk.Progressbar(parent, orient="horizontal", mode="determinate",
                    length=400, maximum=len(questions),
                    variable=progress_value, bootstyle="success").pack(pady=10)

    # Navigation
    nav_frame = tk.Frame(parent, bg="#98FF98", padx=10, pady=10)
    nav_frame.pack(fill="x", pady=10)

    ttk.Button(nav_frame, text="Next ➡", bootstyle="info",
               command=next_question).pack(side="right", padx=10)

    ttk.Button(nav_frame, text="Quit", bootstyle="danger",
               command=parent.quit).pack(side="left", padx=10)

def show_summary_window():
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
                          font=("Aptos ExtraBold", 12))
    answer_text.pack(fill="both", expand=True)
    scrollbar.config(command=answer_text.yview)

    # Insert final score
    answer_text.insert("1.0", f"Final Score: {score}\n\n")

    # Read and display answer.txt
    try:
        with open(FILENAME, "r", encoding="utf-8") as f:
            contents = f.read()
        answer_text.insert("end", contents)
    except FileNotFoundError:
        answer_text.insert("end", "No answers recorded.\n")

    answer_text.insert("end", "\nThanks for playing!\n")
    answer_text.config(state="disabled")

    nav_frame = ttk.Frame(sum_win, padding=10)
    nav_frame.pack(fill="x")

    ttk.Button(nav_frame, text="Play Again", bootstyle="success",
               command=lambda: restart_quiz(sum_win)).pack(side="left", padx=10)

    ttk.Button(nav_frame, text="Close", bootstyle="danger",
               command=sum_win.destroy).pack(side="right", padx=10)

def restart_quiz(window):
    window.destroy()
    start_game()

def create_main_window():
    start_frame = tk.Frame(root, bg="#98FF98", padx=50, pady=50)
    start_frame.pack(fill="both", expand=True)

    tk.Label(start_frame, text="Press here to start",
             font=("Aptos ExtraBold", 20, "bold"), bg="#98FF98").pack(pady=20)

    ttk.Button(start_frame, text="Start Quiz ▶", bootstyle="success",
               command=lambda: start_game_ui(start_frame)).pack(pady=10)

    root.mainloop()

def start_game_ui(start_frame):
    start_frame.destroy()
    main_frame = tk.Frame(root, bg="#98FF98", padx=20, pady=20)
    main_frame.pack(fill="both", expand=True)
    create_widgets(main_frame)
    start_game()

# ---------------- Run App ---------------- #
if __name__ == "__main__":
    create_main_window()