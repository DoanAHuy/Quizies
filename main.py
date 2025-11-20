import random
import tkinter as tk
import ttkbootstrap as ttk
from DATA import questions
from tkinter import messagebox
from tkinter import font


#declare variables
root = tk.Tk()
root.O1 = ttk.StringVar()
root.O2 = ttk.StringVar()
root.O3 = ttk.StringVar()
root.O4 = ttk.StringVar()
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
root.quitBtn = tk.Button(root, text="Quit", command=root.quit)

root.nextBtn = tk.Button(root, text="Next", command=lambda: next_question())
root.Button1 = tk.Radiobutton(root, anchor="w", textvariable=root.O1, variable=root.user_selected, value=1,
                              command=lambda: set_choices(1), indicatoron=False)
root.Button2 = tk.Radiobutton(root, anchor="w", textvariable=root.O2, variable=root.user_selected, value=2,
                              command=lambda: set_choices(2), indicatoron=False)
root.Button3 = tk.Radiobutton(root, anchor="w", textvariable=root.O3, variable=root.user_selected, value=3,
                              command=lambda: set_choices(3), indicatoron=False)
root.Button4 = tk.Radiobutton(root, anchor="w", textvariable=root.O4, variable=root.user_selected, value=4,
                              command=lambda: set_choices(4), indicatoron=False)
root.label_feedback = ttk.Label(textvariable=root.feedback, font=("Arial", 15, "bold"),anchor="w")
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

#store user choices
def set_choices(choice):
    root.user_selected.set(choice)
    root.nextBtn.config(state="normal")
#Progess bar
def progress_bar():
    root.Progress.set(root.Progress.get()+1)
    root.ProgressText.set(f"Question {root.Progress.get()}/{len(questions)}")

#load question
def load_questions():
    if len(root.question_index) == len(questions):
        messagebox.showinfo("Quiz complete", f"Final score is {root.score.get()}")
        root.quit()
        return
    root.nextBtn.config(state="disabled")
    root.user_selected.set(0)# reset user choice
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
    length=len(root.question.get())
    width = min(800, 100 + 10 * length)
    root.geometry(f'{width}' + "x180")
    #pair choices with data's options
    root.choices=q["Options"].copy()
    random.shuffle(root.choices)
    root.O1.set(root.choices[0])
    root.O2.set(root.choices[1])
    root.O3.set(root.choices[2])
    root.O4.set(root.choices[3])
    root.nextBtn.config(state="disabled")
    root.feedback.set("") #reset the feedback
    #reenable button
    root.Button1.config(state="normal")
    root.Button2.config(state="normal")
    root.Button3.config(state="normal")
    root.Button4.config(state="normal")


#check the answer
def validate_ans():
    selected_value = root.user_selected.get()
    if selected_value == 0:

        return
    selected_text = [root.O1.get(), root.O2.get(), root.O3.get(), root.O4.get()][selected_value - 1]
    if selected_text == root.correct_answer:
        root.score.set(root.score.get() + 5)
        root.label_feedback.config(foreground="green")
        root.feedback.set("Correct!")
        print("Correct!")
    else:
        root.label_feedback.config(foreground="red")
        root.feedback.set(f"Incorrect!, Correct answer is {root.correct_answer}")
        print("Incorrect!")

    print(f"selected:{selected_text},correct:{root.correct_answer}")
    disable_choices()
#Next button
def next_question():
    validate_ans()
    root.feedback.set("")
    root.question_index.append(root.current_index)
    root.after(1000,load_questions())
root.next = next_question

#disable after choice
def disable_choices():
    root.Button1.config(state="disabled")
    root.Button2.config(state="disabled")
    root.Button3.config(state="disabled")
    root.Button4.config(state="disabled")

def adjust_font_size(event, root):
    width = event.width
    # Scale font size between 12 and 24 based on window width
    new_size = max(12, min(24, width // 30))
    root.dynamic_font.configure(size=new_size)
    # Optionally adjust wraplength too
    root.label_question.configure(wraplength=width - 100)

#Create start menu
def menu():
    root.menu = tk.Menu(root)
    root.menu.add_command(label="New", command=lambda: root.start_game())
    root.menu.add_command(label="Exit", command=root.quit)
    top.config(menu=root.menu)

#Create Widgets
def createWidgets(root, top):
    top.geometry("600x300")
    top.resizable(True, True)
    root.dynamic_font = font.Font(family="Arial", size=14)
    # Configure grid for centering
    for i in range(7):
        top.grid_columnconfigure(i, weight=1)
    for i in range(10):
        top.grid_rowconfigure(i, weight=1)
    #auto resize
    top.bind("<Configure>", lambda event: adjust_font_size(event, root))
    # Question label
    root.label_question = ttk.Label(textvariable=root.question, font=(root.dynamic_font), wraplength=500, anchor="center")
    root.label_question.grid(column=1, row=2, columnspan=5, pady=10)

    # Progress label
    root.label_progress = ttk.Label(textvariable=root.ProgressText, font=("Arial", 10))
    root.label_progress.grid(column=1, row=1, columnspan=5)

    # Score label
    root.label_score = ttk.Label(text="Score:", font=("Arial", 10))
    root.label_score.grid(column=4, row=3, sticky="e")
    root.label_score_value = ttk.Label(textvariable=root.score, font=("Arial", 10))
    root.label_score_value.grid(column=5, row=3, sticky="w")

    # Feedback label
    root.label_feedback.grid(column=2, row=3, columnspan=5, pady=10)

    # Control buttons
    root.quitBtn.grid(column=2, row=9, pady=10)
    root.nextBtn.grid(column=4, row=9, pady=10)

#Create choices

    root.Button1.grid(column=2, row=4, columnspan=3, sticky="w", padx=20, pady=5)
    root.Button2.grid(column=2, row=5, columnspan=3, sticky="w", padx=20, pady=5)
    root.Button3.grid(column=2, row=6, columnspan=3, sticky="w", padx=20, pady=5)
    root.Button4.grid(column=2, row=7, columnspan=3, sticky="w", padx=20, pady=5)



menu()
root.mainloop()