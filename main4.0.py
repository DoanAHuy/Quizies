import tkinter as tk
import ttkbootstrap as ttk
import pyglet
import random
import sys,os
from DATA import questions
from PIL import Image, ImageTk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import re
from collections import defaultdict

def resource_path(filename):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, filename)
    return os.path.join(os.path.abspath("."), filename)

# Variables
logo_path=resource_path("logo.jpg")
logo=Image.open(logo_path)
logo=logo.resize((297, 243), Image.Resampling.LANCZOS)
font_path = resource_path("Aptos-ExtraBold.ttf")
pyglet.font.add_file(font_path)
pyglet.options['win32_gdi_font'] = True #fix font path
FILENAME="answer.txt"

root = ttk.Window(themename="cosmo")
root.configure(background="#FEF2F2")
ttk.Style().configure("Custom.TFrame", background="#FEF2F2")
root.title("Quizies")
root.geometry("750x800")
root.iconbitmap("app_logo.ico")

# style
style = ttk.Style()
# Frames
style.configure("Custom.TFrame", background="#FEF2F2")
style.configure("Body.TFrame", background="white")
style.configure("Pink.TLabel",background="#FEF2F2")

# Labels
style.configure("Custom.TLabel", background="#FEF2F2", foreground="black")

# Buttons
style.configure("Custom.TButton", background="#FEF2F2", foreground="black")
style.configure( "Hover.TButton",background="#f0ddc6",foreground="black",font=("Aptos ExtraBold",16))
style.map("Hover.TButton",background=[("active", "#c8c6f0")],foreground=[("active", "black")])
style.configure("Start_button.TButton", background="#08B36A", font=("Aptos ExtraBold",14))
# Radiobuttons
style.configure("custom.Toolbutton", background="#f1c8db", foreground="black",font=("Aptos ExtraBold",13))
style.map("custom.Toolbutton",background=[("active", "#c8c6f0"), ("selected", "#ae2d69")])
#Progress Bar
style.configure("Custom.Horizontal.TProgressbar", troughcolor="#FEF2F2",bordercolor="#FEF2F2",background="#6fbf8b",lightcolor="#6fbf8b",darkcolor="#6fbf8b")
style.configure("Score.TLabel",background="#FEF2F2",foreground="black",font=("Aptos ExtraBold", 12, "bold"))

main_bg = ttk.Frame(root,style="Custom.TFrame")
main_bg.pack(fill="both", expand=True)
tkimage=ImageTk.PhotoImage(logo)

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
    progress_value.set(1)
    score_text.set("Score: 0")
    progress_text.set(f"Question 1 of {len(questions)}")  # Update label

    question_index.clear()

    with open(FILENAME, "a", encoding="utf-8") as f:
        f.write("\n" + "=" * 20 + " NEW ATTEMPT " + "=" * 20 + "\n")

    load_question()
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

    next_val = progress_value.get() + 1
    progress_value.set(next_val)

    if next_val <= len(questions):
        progress_text.set(f"Question {next_val} of {len(questions)}")
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
            feedback_text.set("Incorrect")
            result = "Incorrect"

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
#Progress
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
    buttons_frame = ttk.Frame(parent, style="Body.TFrame")
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


def plot_statistics(parent_frame):
    question_map = {q["Quest"]: i for i, q in enumerate(questions)}
    total_questions = len(questions)

    # Initialize empty counters for all 20 questions
    correct_counts = [0] * total_questions
    incorrect_counts = [0] * total_questions
    num_attempts = 0  # Counter for students
    # Find the text after the last "NEW ATTEMPT" separator
    try:
        with open(FILENAME, "r", encoding="utf-8") as f:
            content = f.read()

        # COUNT ATTEMPTS: Count how many times the separator appears
        num_attempts = content.count("NEW ATTEMPT")

        # FIND ANSWERS: Regex to find Question Text and Result
        matches = re.findall(r"Question \d+: (.*?)\n.*?Result: (\w+)", content, re.DOTALL)

        if not matches:
            ttk.Label(parent_frame, text="No data to plot yet.", font=("Aptos", 14)).pack(pady=20)
            return

        for q_text, result in matches:
            q_text = q_text.strip()

            # Map the text from file back to its ID
            if q_text in question_map:
                idx = question_map[q_text]
                if result == "Correct":
                    correct_counts[idx] += 1
                else:
                    incorrect_counts[idx] += 1
            else:
                #If text in file doesn't match DATA.py exactly
                print(f"Warning: Unknown question found: {q_text[:20]}...")

    except FileNotFoundError:
        ttk.Label(parent_frame, text="No data file found.", font=("Aptos", 14)).pack(pady=20)
        return

    # 3. PLOT
    labels = [f"Q{i + 1}" for i in range(total_questions)]  # Labels Q1 to Q20

    fig, ax = plt.subplots(figsize=(9, 4.5), dpi=100)


    indices = range(total_questions)
    bar_width = 0.6

    # Stacked Bars
    p1 = ax.bar(indices, correct_counts, bar_width, label='Correct', color='#4CAF50')
    p2 = ax.bar(indices, incorrect_counts, bar_width, bottom=correct_counts, label='Incorrect', color='#F44336')

    # TITLE: Shows exact number of Students/Attempts
    ax.set_title(f'Class Statistics: {num_attempts} Student Attempts', fontsize=11, fontweight='bold')

    ax.set_ylabel('Count')
    ax.set_xticks(indices)
    ax.set_xticklabels(labels, rotation=45, fontsize=8)

    # Force Y-axis to be integers (0, 1, 2...)
    max_height = max(max(correct_counts) + max(incorrect_counts), 1) + 1
    ax.set_yticks(range(0, int(max_height)))

    ax.legend(loc='upper right', fontsize=8)
    plt.grid(axis='y', linestyle='--', alpha=0.3)  # Horizontal grid lines for easier reading
    plt.tight_layout()


    canvas = FigureCanvasTkAgg(fig, master=parent_frame)
    canvas.draw()
    canvas.get_tk_widget().pack(fill="both", expand=True)


def show_summary_window():
    root.next_button.configure(state="disabled")
    root.quit_button.configure(state="disabled")

    sum_win = tk.Toplevel()
    sum_win.title("Quiz Summary")
    sum_win.geometry("600x750")

    #NAVIGATION BUTTONS (Create & Pack FIRST)
    nav_frame = ttk.Frame(sum_win, style="Custom.TFrame", padding=10)
    nav_frame.pack(side="bottom", fill="x")

    nav_frame.grid_columnconfigure(0, weight=1)
    nav_frame.grid_columnconfigure(1, weight=1)

    ttk.Button(nav_frame, text="Play Again", bootstyle="success",
               command=lambda: restart_quiz(sum_win)).grid(row=0, column=0, sticky="w", padx=10)
    ttk.Button(nav_frame, text="Close", bootstyle="danger",
               command=root.destroy).grid(row=0, column=1, sticky="e", padx=10)

    #TABS (Create & Pack SECOND)
    tab_control = ttk.Notebook(sum_win)
    tab_control.pack(side="top", expand=True, fill="both")

    tab1 = ttk.Frame(tab_control)
    tab2 = ttk.Frame(tab_control)

    tab_control.add(tab1, text='My Results')
    tab_control.add(tab2, text='Class Statistics')

    #TAB 1 CONTENT (Text Summary)
    content = ttk.Frame(tab1, style="Custom.TFrame", padding=10)
    content.pack(fill="both", expand=True)

    text_frame = ttk.Frame(content, style="Custom.TFrame")
    text_frame.pack(fill="both", expand=True)

    scrollbar = ttk.Scrollbar(text_frame, orient="vertical")
    scrollbar.pack(side="right", fill="y")

    answer_text = tk.Text(
        text_frame, wrap="word", yscrollcommand=scrollbar.set,
        font=("Aptos ExtraBold", 10), bg="#FEF2F2"
    )
    answer_text.pack(fill="both", expand=True)
    scrollbar.config(command=answer_text.yview)

    try:
        with open(FILENAME, "r", encoding="utf-8") as f:
            full_content = f.read()
            # Split by the separator to find the latest attempt
            attempts = full_content.split("==================== NEW ATTEMPT ====================")
            last_attempt = attempts[-1] if len(attempts) > 1 else full_content

        answer_text.insert("1.0", f"Final Score: {score}\n\n")
        answer_text.insert("end", last_attempt.strip())
    except FileNotFoundError:
        answer_text.insert("end", "No answers recorded.\n")

    answer_text.config(state="disabled")

    # TAB 2 CONTENT (Graph)
    plot_statistics(tab2)

def restart_quiz(window):
    window.destroy()
    root.next_button.configure(state="normal")
    root.quit_button.configure(state="normal")
    start_game()

def create_main_window():
    start_frame = ttk.Frame(main_bg, style="Custom.TFrame", padding=50)
    start_frame.pack(fill="both", expand=True)

    start_frame.grid_rowconfigure(0, weight=1)
    start_frame.grid_rowconfigure(1, weight=1)
    start_frame.grid_rowconfigure(2, weight=1)
    start_frame.grid_columnconfigure(0, weight=1)

    # Logo with tk.Label so background shows
    logo_label = tk.Label(start_frame, image=tkimage, bg="#FEF2F2")
    logo_label.grid(row=0, column=0, pady=0)

    # Text
    title_label = ttk.Label(start_frame, text="Press here to start",
                            font=("Aptos ExtraBold", 24, "bold"),
                            style="Pink.TLabel")
    title_label.grid(row=1, column=0, pady=20)

    # Button
    start_button = ttk.Button(start_frame, text="Start Quiz ▶", style="Start_button.TButton",
                              command=lambda: start_game_ui(start_frame))
    start_button.grid(row=2, column=0, pady=10)

    root.mainloop()

def start_game_ui(start_frame):
    start_frame.destroy()

    ttk.Style().configure("main.TFrame",img="logo.png")
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
    #Reset attempts to 0 on launch
    with open(FILENAME, "w", encoding="utf-8") as f:
        f.write("")

    create_main_window()