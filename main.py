import ttkbootstrap as ttk
import tkinter as tk
from tkinter import messagebox, ttk
from ttkbootstrap import Style
from Questions import questions
root = tk.Tk()

#window
root.geometry("800x600")
root.title("Quizies")
#changestyle
style = Style(theme='litera')
style.configure('TLabel', font=("times new roman", 20))
style.configure('TButton', font=("times new roman", 20))

#frame
tframe = ttk.Frame(root, style="warning.TFrame")
tframe.pack(pady=40)
mframe = ttk.Frame(root,)
mframe.pack(pady=50)

#function
def show_question():
    question = questions[current_quest]
    q_label.config(text=question["question"])

    choices=question["choices"]
    for i in range(4):
        c_buttons[i].config(text=choices[i], state="normal")

    fb_lbl.config(text="")
    next_btn.config(state="disabled")
def check_answer(choice):
    question = questions[current_quest]
    user_selected = c_buttons[choice].cget("text")

    if user_selected == question["answer"]:
        global score
        score += 1
        score_lbl.config(text="score: {}/{}".format(score, len(questions)))
        c_buttons[choice].config(style="success.TLabel")
        fb_lbl.config(text="The answer is correct!", foreground="green")
    else:
        fb_lbl.config(text="The answer is wrong!", foreground="red")
    for button in c_buttons:
        button.config(state="disabled")
    next_btn.config(state="normal")

def next_question():
    global current_quest
    current_quest += 1
    if current_quest < len(questions):
        show_question()
    else:
        messagebox.showinfo("All the questions has been completed !", "Well done! Final score: {}/{}".format(score, len(questions)))
        root.destroy()
#varible
current_quest=0
#questionline
q_label = ttk.Label(
    tframe,
    style='inverse.TLabel',
    anchor='center',
    wraplength=500,
    padding=10
)
q_label.pack(pady=10)
#buttons
c_buttons = []
for i in range(4):
    button = ttk.Button(
        mframe,
        style='outline.TButton',
        command=lambda i=i: check_answer(i),
    )
    button.pack(pady=10)
    c_buttons.append(button)
next_btn = ttk.Button(
    root,
    text="Next",
    command=next_question,
    state="disabled"
)
next_btn.pack(pady=10)
#feedbacks
fb_lbl = ttk.Label(
    root,
    anchor='center',
    padding=10
)
fb_lbl.pack(pady=10)
score = 0
score_lbl = ttk.Label(
    root,
    text="score: 0/{}".format(len(questions)),
    anchor='center',
    padding=10
)
score_lbl.pack(pady=10)

#start
show_question()
root.mainloop()

