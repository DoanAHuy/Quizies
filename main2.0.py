import random
import tkinter as tk
import pyglet
import ttkbootstrap as ttk
from ttkbootstrap import TkFrame
from DATA import questions

pyglet.options['win32_gdi_font'] = True
#path for font
pyglet.font.add_directory("MicrosoftAptosFonts")
FILENAME="answer.txt"
#declare variables
root = ttk.Window(themename="cosmo")
root.O1 = tk.StringVar()
root.O2 = tk.StringVar()
root.O3 = tk.StringVar()
root.O4 = tk.StringVar()
root.correct_answer = ""
root.user_selected = tk.IntVar(root, 1)
root.question = tk.StringVar()
root.score = tk.IntVar(root, 0)
root.title('Quizzies')
root.question_index=[]
top = root.winfo_toplevel()
root.Progress = tk.IntVar()
root.ProgressText= tk.StringVar()
root.feedback = tk.StringVar()
root.next_mode = 'check'
style = ttk.Style()

#start quiz
def start_game():
    if not hasattr(root, 'widgets_created'):
        createWidgets(root, top)
        root.widgets_created = True
    load_questions()
    root.score.set(0)
    root.Progress.set(0)
    root.question_index.clear()

root.start_game = start_game
#Next button
def next_question():
    if root.next_mode == 'check':
        validate_ans()
        root.next_mode = 'next'
        root.next_button.config(text="Next question")
    else:
        root.question_index.append(root.current_index)
        load_questions()
        root.next_mode = 'check'
        root.next_button.config(text="Check question")
#store user choices
def set_choices(choice):
    root.user_selected.set(choice)
    root.next_button.config(state="normal")
#Progess bar
def progress_bar():
    root.Progress.set(root.Progress.get()+1)
    root.ProgressText.set(f"Question {root.Progress.get()}/{len(questions)}")

#load question
def load_questions():
    if len(root.question_index) == len(questions):
        show_summary_window()
        return
    root.next_button.configure(state="disabled")
    root.user_selected.set(0)# reset user choice
    enable_choices()
#random question
    while True:
        index = random.randint(0, len(questions) - 1)
        if index not in root.question_index:
            root.current_index = index
            break

    progress_bar()
    q = questions[root.current_index]
    root.correct_answer = q["Answer"]
    root.question.set(q["Quest"])
    #pair choices with data.py
    root.choices=q["Options"].copy()
    random.shuffle(root.choices)
    root.O1.set(root.choices[0])
    root.O2.set(root.choices[1])
    root.O3.set(root.choices[2])
    root.O4.set(root.choices[3])
    root.next_button.config(state="disabled")
    root.feedback.set("") #reset the feedback


#check the answer
def validate_ans():
    disable_choices()
    selected_value = root.user_selected.get()
    if selected_value == 0:
        root.feedback.set("")
        return
    selected_text = [root.O1.get(), root.O2.get(), root.O3.get(), root.O4.get()][selected_value - 1]
    if selected_text == root.correct_answer:
        root.score.set(root.score.get() + 5)
        root.feedback_label.config(foreground="green")
        root.feedback.set("Correct!")
        with open("answer.txt","a", encoding="utf-8") as file:
            file.write(selected_text + '\n')
        print("Correct!")
    else:
        root.feedback_label.config(foreground="red")
        root.feedback.set(f"Incorrect!, Correct answer is {root.correct_answer}")
        with open("answer.txt","a", encoding="utf-8") as file:
            file.write(selected_text + '\n' + '\n')
        #style.map('custom.Toolbutton', background=[('disabled','red'),])
        print("Incorrect!")

    print(f"selected:{selected_text},correct:{root.correct_answer}")

#disable after choice
def disable_choices():
    root.Button1.config(state="disabled")
    root.Button2.config(state="disabled")
    root.Button3.config(state="disabled")
    root.Button4.config(state="disabled")
#reset state after question
def enable_choices():
    root.Button1.config(state="normal")
    root.Button2.config(state="normal")
    root.Button3.config(state="normal")
    root.Button4.config(state="normal")

#Create start menu
def menu():
    root.menu = tk.Menu(root)
    root.menu.add_command(label="New", command=lambda: root.start_game())
    root.menu.add_command(label="Exit", command=root.quit)
    top.config(menu=root.menu)

def show_summary_window():
        # Create a summary window
        Sum_win = tk.Toplevel(root)
        Sum_win.title("Summary")
        Sum_win.geometry("500x400")
        Summary_text=ttk.Label(Sum_win,text=f'Quiz completed,your final score is {root.score.get()}!')
        Summary_text.pack(pady=10)
        show_button = ttk.Button(Sum_win,bootstyle="info",text='Show selected answer', command=lambda: show_answer_file(Sum_win))
        show_button.pack(pady=10)
        # exit button
        close_button = tk.Button(Sum_win, text="Exit Application", command=root.destroy)
        close_button.pack(pady=10)
def show_answer_file(Sum_win):
        root.withdraw()
        #create answer window
        new_win = tk.Toplevel(Sum_win)
        new_win.title("Answer")
        new_win.geometry("500x400")
        # Text widget to display file contents
        text_area = tk.Text(new_win, wrap="word", font=("Aptos ExtraBold", 15))
        text_area.pack(expand=True, fill="both")
        with open("answer.txt", "r", encoding="utf-8") as f:
            content = f.read()
        text_area.insert(tk.END, content)
#Create Widgets
def createWidgets(root,top):
    # Main container
    main_frame = ttk.Frame(root, padding=20)
    main_frame.pack(fill="both", expand=True)
    #style for question
    style.configure("info.TLabel")
    #Question
    root.question_frame = ttk.Labelframe(main_frame,text="Question:", padding=15, style="info.TLabel")
    root.question_frame.pack(fill="x", pady=10)
    root.question_label = ttk.Label(
        root.question_frame,
        textvariable=root.question,
        font=("Aptos ExtraBold", 16),
        anchor="center",
        wraplength=600
    )
    root.question_label.pack(pady=10)
    #Choice frame
    choices_frame = ttk.Frame(main_frame, padding=15)
    choices_frame.pack(fill="x", pady=10)

    # style for buttons
    style.configure("custom.Toolbutton",
                    background="#FF8DC6",
                    foreground="red",
                    font=("Aptos ExtraBold", 14)
                    )

    # Create multiple choices
    root.Button1 = ttk.Radiobutton(choices_frame,style="custom.Toolbutton", textvariable=root.O1, variable=root.user_selected, value=1,
                                   command=lambda: set_choices(1))
    root.Button2 = ttk.Radiobutton(choices_frame,style="custom.Toolbutton", textvariable=root.O2, variable=root.user_selected, value=2,
                                   command=lambda: set_choices(2))
    root.Button3 = ttk.Radiobutton(choices_frame,style="custom.Toolbutton", textvariable=root.O3, variable=root.user_selected, value=3,
                                   command=lambda: set_choices(3))
    root.Button4 = ttk.Radiobutton(choices_frame,style="custom.Toolbutton", textvariable=root.O4, variable=root.user_selected, value=4,
                                   command=lambda: set_choices(4))
    for i, btn in enumerate([root.Button1, root.Button2, root.Button3, root.Button4]):
        btn.pack(anchor="w", pady=5, padx=20)

    # Feedback section
    root.feedback_frame = ttk.Frame(main_frame, padding=10)
    root.feedback_frame.pack(fill="x", pady=10)

    root.feedback_label = ttk.Label(
        root.feedback_frame,
        textvariable=root.feedback,
        font=("Segoe UI", 12),
        bootstyle="secondary"
    )
    root.feedback_label.pack()

    # Score + Progress section
    root.status_frame = ttk.Frame(main_frame, padding=10)
    root.status_frame.pack(fill="x", pady=10)

    root.score_label = ttk.Label(
        root.status_frame,
        textvariable=root.score,
        font=("Segoe UI", 12, "bold"),
        bootstyle="success"
    )
    root.score_label.pack(side="left", padx=10)

    root.progress_label = ttk.Label(
        root.status_frame,
        textvariable=root.ProgressText,
        font=("Segoe UI", 12),
        bootstyle="info"
    )
    root.progress_label.pack(side="right", padx=10)

    # Progress bar
    root.progress_bar = ttk.Progressbar(
        main_frame,
        orient="horizontal",
        mode="determinate",
        length=400,
        maximum=10,
        variable=root.Progress
    )
    root.progress_bar.pack(pady=10)
    #Style for navi button
    style.configure("next.TButton",background="#FF8DC6",foreground="green")
    style.configure("quit.TButton",background="#FF8DC6",foreground="red")
    # Navigation buttons
    nav_frame = ttk.Frame(main_frame, padding=10)
    nav_frame.pack(fill="x", pady=10)
    root.next_button = ttk.Button(
        nav_frame,
        text="Next Question ➡",
        style="next.TButton",
        command=next_question
    )
    root.next_button.pack(side="right", padx=10)

    root.quit_button = ttk.Button(
        nav_frame,
        text="Quit ✖",
        style="quit.TButton",
        command=root.quit
    )
    root.quit_button.pack(side="left", padx=10)

def create_main_window():
    root.geometry("750x700")
    root.resizable(True,True)
    menu()
    root.mainloop()

if __name__ == "__main__":
    create_main_window()