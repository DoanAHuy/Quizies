import random
import tkinter as tk
from tkinter import messagebox
import pyglet
import ttkbootstrap as ttk
from DATA import questions
pyglet.options['win32_gdi_font'] = True

#path for font
pyglet.font.add_directory("MicrosoftAptosFonts")



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
    validate_ans()
    root.question_index.append(root.current_index)
    root.after(1000,load_questions())
root.next = next_question


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
        root.feedback.set("")
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
#disable after choice
def disable_choices():
    root.Button1.config(state="disabled")
    root.Button2.config(state="disabled")
    root.Button3.config(state="disabled")
    root.Button4.config(state="disabled")

#Create start menu
def menu():
    root.menu = tk.Menu(root)
    root.menu.add_command(label="New", command=lambda: root.start_game())
    root.menu.add_command(label="Exit", command=root.quit)
    top.config(menu=root.menu)

#Create Widgets
def createWidgets(root, top):
    # setting question frames
    def create_question_frames(container):
        frame = ttk.Frame(container)
        frame['borderwidth'] = 5
        frame['relief']='solid'
        # Progress label
        frame.label_progress = ttk.Label(textvariable=root.ProgressText, font=("Aptos ExtraBold", 12))
        frame.label_progress.grid(column=1, row=1, columnspan=5)
        # Question label
        frame.label_question = ttk.Label(textvariable=root.question, font=("Aptos ExtraBold", 15), wraplength=500,
                                        anchor="center")
        frame.label_question.grid(column=1, row=2, sticky=tk.W)



        for widget in root.winfo_children():
            widget.grid(padx=5, pady=10)
        return frame
    #setting choices frame
    def create_buttons_frames(container):
        frame = ttk.Frame(container)
        frame.columnconfigure(0, weight=1)
        # Create multiple choices
        frame.Button1 = ttk.Radiobutton(root, style='info.Outline.Toolbutton', textvariable=root.O1,
                                       variable=root.user_selected, value=1, command=lambda: set_choices(1))
        frame.Button2 = ttk.Radiobutton(root, style='info.Outline.Toolbutton', textvariable=root.O2,
                                       variable=root.user_selected, value=2, command=lambda: set_choices(2))
        frame.Button3 = ttk.Radiobutton(root, style='info.Outline.Toolbutton', textvariable=root.O3,
                                       variable=root.user_selected, value=3, command=lambda: set_choices(3))
        frame.Button4 = ttk.Radiobutton(root, style='info.Outline.Toolbutton', textvariable=root.O4,
                                       variable=root.user_selected, value=4, command=lambda: set_choices(4))
        frame.Button1.grid(column=2, row=4, columnspan=3, sticky="w", padx=20, pady=5)
        frame.Button2.grid(column=2, row=5, columnspan=3, sticky="w", padx=20, pady=5)
        frame.Button3.grid(column=2, row=6, columnspan=3, sticky="w", padx=20, pady=5)
        frame.Button4.grid(column=2, row=7, columnspan=3, sticky="w", padx=20, pady=5)
        # buttons style
        style = ttk.Style()
        style.configure('info.Outline.Toolbutton', font=("Aptos ExtraBold", 12))
        for widget in root.winfo_children():
            widget.grid(padx=5, pady=10)
        return frame

    def create_interaction_frames(container):
        frame = ttk.Frame(container)
        # Control buttons
        frame.quitBtn.grid(column=2, row=8, pady=10)
        frame.nextBtn.grid(column=4, row=8, pady=10)
        # Score label
        frame.label_score = ttk.Label(text="Score:", font=("Arial", 14))
        frame.label_score.grid(column=3, row=1)
        frame.label_score_value = ttk.Label(textvariable=root.score, font=("Arial", 12))
        frame.label_score_value.grid(column=4, row=1)
        # Feedback label
        root.label_feedback = ttk.Label(
            textvariable=root.feedback,
            font=("Aptos ExtraBold", 12, "bold"),
            foreground="green",
            anchor="e"
        )
        root.label_feedback.grid(column=6, row=8, columnspan=5)
        for widget in root.winfo_children():
            widget.grid(padx=5, pady=10)

        return frame

    #auto resize
#top.bind("<Configure>", lambda event: adjust_font_size(event, root))
def create_main_window():
    root.resizable(0, 0)
    # layout on the root window
    root.columnconfigure(0, weight=4)
    root.columnconfigure(1, weight=1)

    questions_frame = create_question_frames(root)
    questions_frame.grid(column=0, row=0)

    button_frame = create_buttons_frames(root)
    button_frame.grid(column=1, row=0)
    menu()
    root.mainloop()

if __name__ == "__main__":
    create_main_window()