import tkinter as tk
import ttkbootstrap as ttk
import pyglet
import random
import sys,os
from DATA import questions

# Variables
def resource_path(relative_path):
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

font_path = resource_path("Aptos-ExtraBold.ttf")
pyglet.font.add_file(font_path)
pyglet.options['win32_gdi_font'] = True #fix font path
FILENAME="answer.txt"

root = ttk.Window(themename="cosmo")
root.configure(background="#c6f0dd")
ttk.Style().configure("Custom.TFrame", background="#c6f0dd")
root.title("Quizies")
root.geometry("750x700")

# style
style = ttk.Style()
# Frames
style.configure("Custom.TFrame", background="#c6f0dd")
style.configure("Body.TFrame", background="#c6f0dd")


# Labels
style.configure("Custom.TLabel", background="#c6f0dd", foreground="black")

# Buttons
style.configure("Custom.TButton", background="#c6f0dd", foreground="black")
style.configure( "Hover.TButton",background="#f0ddc6",foreground="black",font=("Aptos ExtraBold",16))
style.map("Hover.TButton",background=[("active", "#c8c6f0")],foreground=[("active", "black")])

# Radiobuttons
style.configure("custom.Toolbutton", background="#f1c8db", foreground="black",font=("Aptos ExtraBold",13))
style.map("custom.Toolbutton",background=[("active", "#c8c6f0"), ("selected", "#ae2d69")])
#Progress Bar
style.configure("Custom.Horizontal.TProgressbar", troughcolor="#c6f0dd",bordercolor="#c6f0dd",background="#6fbf8b",lightcolor="#6fbf8b",darkcolor="#6fbf8b")
style.configure("Score.TLabel",background="#c6f0dd",foreground="black",font=("Aptos ExtraBold", 12, "bold"))

main_bg = ttk.Frame(root,style="Custom.TFrame")
main_bg.pack(fill="both", expand=True)

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
    progress_text.set(f"Question 0 of {len(questions)}")
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

def next_question():
    validate_answer()
    progress_value.set(progress_value.get() + 1)
    progress_text.set(f"Question {progress_value.get()} of {len(questions)}")

    if progress_value.get() < len(questions):
        load_question()
    else:
        show_summary_window()

def validate_answer():
    global score
    selected = user_selected.get()
    if selected == 0:
        feedback_text.set("No option selected")
        result = "None"
    else:
        chosen_answer = root.choices[selected - 1]
        correct_answer = current_question["Answer"]

        if chosen_answer == correct_answer:
            feedback_text.set("Correct")
            score += 5
            score_text.set(f"Score: {score}")
            result = "Correct"
        else:
            feedback_text.set("Wrong")
            result = "Wrong"

        # Record to file
        with open(FILENAME, "a", encoding="utf-8") as f:
            f.write(f"Question {progress_value.get()}: {current_question['Quest']}\n")
            f.write(f"Your answer: {chosen_answer}\n")
            f.write(f"Correct answer: {correct_answer}\n")
            f.write(f"Result: {result}\n\n")



def create_widgets(parent):
    parent.grid_rowconfigure(0, weight=2)  # question area
    parent.grid_rowconfigure(1, weight=2)  # buttons
    parent.grid_rowconfigure(2, weight=1)  # status/progress
    parent.grid_rowconfigure(3, weight=1)  # navigation
    parent.grid_columnconfigure(0, weight=1)

    # Question
    question_frame = ttk.Frame(parent, style="Custom.TFrame",padding =10)
    question_frame.grid(row=0, column=0, sticky="nsew")
    question_label=ttk.Label(question_frame, textvariable=question_text,
             font=("Aptos ExtraBold", 16, "bold"), style="Custom.TLabel",wraplength=700,justify="center", anchor="center")
    question_label.pack(expand=True)
#PRogress
    progress_frame = ttk.Frame(question_frame, style="Custom.TFrame")
    progress_frame.pack(fill="x", pady=(5, 0))

    progress_label = ttk.Label(
        progress_frame, textvariable=progress_text,
        font=("Aptos ExtraBold", 12), style="Score.TLabel"
    )
    progress_label.pack(side="top", pady=2)

    ttk.Progressbar(
        progress_frame, orient="horizontal", mode="determinate",
        maximum=len(questions), variable=progress_value,
        style="Custom.Horizontal.TProgressbar"
    ).pack(fill="x", padx=20, pady=5)

    def update_wraplength(event):
        new_length = event.width - 40
        if new_length < 200:
            new_length = 200
        question_label.configure(wraplength=new_length)
    parent.bind("<Configure>", update_wraplength)
    question_frame.config(height=120)
    question_frame.pack_propagate(False)
    #Buttons
    buttons_frame = ttk.Frame(parent, style="Custom.TFrame")
    buttons_frame.grid(row=1, column=0, sticky="nsew", pady=5)
    buttons_frame['borderwidth'] = 5
    buttons_frame['relief'] = 'solid'
    buttons_frame.grid_columnconfigure(0, weight=1)

    # Create multiple choices
    root.Button1 = ttk.Radiobutton(buttons_frame, style='custom.Toolbutton', textvariable=root.O1,
                                   variable=user_selected, value=1, command=lambda: set_choices(1))
    root.Button2 = ttk.Radiobutton(buttons_frame, style='custom.Toolbutton', textvariable=root.O2,
                                   variable=user_selected, value=2, command=lambda: set_choices(2))
    root.Button3 = ttk.Radiobutton(buttons_frame, style='custom.Toolbutton', textvariable=root.O3,
                                   variable=user_selected, value=3, command=lambda: set_choices(3))
    root.Button4 = ttk.Radiobutton(buttons_frame, style='custom.Toolbutton', textvariable=root.O4,
                                   variable=user_selected, value=4, command=lambda: set_choices(4))

    for i, btn in enumerate([root.Button1, root.Button2, root.Button3, root.Button4]):
        btn.grid(column=0, row=i, sticky="w", padx=20, pady=5)
    # Navigation

    nav_frame = ttk.Frame(parent, style="Custom.TFrame", padding=20)
    nav_frame.grid(row=3, column=0, sticky="ew")

    nav_frame.grid_columnconfigure(0, weight=1)
    nav_frame.grid_columnconfigure(1, weight=1)

    root.quit_button = ttk.Button(nav_frame, text="Quit", style="Hover.TButton", command=root.quit)
    root.quit_button.grid(row=0, column=0, sticky="w", padx=20, pady=5)

    root.next_button = ttk.Button(nav_frame, text="Next ➡", style="Hover.TButton", command=next_question)
    root.next_button.grid(row=0, column=1, sticky="e", padx=20, pady=5)


def show_summary_window():
    root.next_button.configure(state="disabled")
    root.quit_button.configure(state="disabled")

    sum_win = tk.Toplevel()
    sum_win.title("Quiz Summary")
    sum_win.geometry("500x700")

    # Content area
    content = ttk.Frame(sum_win, style="Custom.TFrame", padding=10)
    content.pack(fill="both", expand=True)

    text_frame = ttk.Frame(content, style="Custom.TFrame")
    text_frame.pack(fill="both", expand=True)

    scrollbar = ttk.Scrollbar(text_frame, orient="vertical")
    scrollbar.pack(side="right", fill="y")

    answer_text = tk.Text(
        text_frame, wrap="word", yscrollcommand=scrollbar.set,
        font=("Aptos ExtraBold", 10), bg="#c6f0dd"
    )
    answer_text.pack(fill="both", expand=True)
    scrollbar.config(command=answer_text.yview)

    answer_text.insert("1.0", f"Final Score: {score}\n\n")
    try:
        with open(FILENAME, "r", encoding="utf-8") as f:
            contents = f.read()
        answer_text.insert("end", contents)
    except FileNotFoundError:
        answer_text.insert("end", "No answers recorded.\n")
    answer_text.insert("end", "\nThanks for playing!\n")
    answer_text.config(state="disabled")

    nav_frame = ttk.Frame(sum_win, style="Custom.TFrame", padding=10)
    nav_frame.pack(side="bottom", fill="x")

    nav_frame.grid_columnconfigure(0, weight=1)
    nav_frame.grid_columnconfigure(1, weight=1)

    ttk.Button(nav_frame, text="Play Again", bootstyle="success",
               command=lambda: restart_quiz(sum_win)).grid(row=0, column=0, sticky="w", padx=10)
    ttk.Button(nav_frame, text="Close", bootstyle="danger",
               command=root.destroy).grid(row=0, column=1, sticky="e", padx=10)

def restart_quiz(window):
    window.destroy()
    root.next_button.configure(state="normal")
    root.quit_button.configure(state="normal")
    start_game()


def create_main_window():
    start_frame = ttk.Frame(main_bg, style="Custom.TFrame",padding=50)
    start_frame.pack(fill="both", expand=True)

    ttk.Label(start_frame, text="Press here to start",
             font=("Aptos ExtraBold", 20, "bold"), style="Custom.TLabel").pack(pady=20)

    ttk.Button(start_frame, text="Start Quiz ▶", bootstyle="success",
               command=lambda: start_game_ui(start_frame)).pack(pady=10)

    root.mainloop()

def start_game_ui(start_frame):
    start_frame.destroy()

    ttk.Style().configure("main.TFrame",background="#c6f0dd")
    for widget in main_bg.winfo_children():
        widget.destroy()
    main_bg.grid_rowconfigure(0, weight=0)
    main_bg.grid_rowconfigure(2, weight=0)
    main_bg.grid_rowconfigure(1, weight=1)

    main_frame = ttk.Frame(main_bg, style="Custom.TFrame")
    main_frame.pack(fill="both", expand=True, padx=20, pady=20)
    create_widgets(main_frame)
    start_game()

# ---------------- Run App ---------------- #
if __name__ == "__main__":
    create_main_window()