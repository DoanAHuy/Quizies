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
        root.nextBtn.config(text="Next question")
    else:
        root.question_index.append(root.current_index)
        load_questions()
        root.next_mode = 'check'
        root.nextBtn.config(text="Check question")
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
    #pair choices with data's options
    root.choices=q["Options"].copy()
    random.shuffle(root.choices)
    root.O1.set(root.choices[0])
    root.O2.set(root.choices[1])
    root.O3.set(root.choices[2])
    root.O4.set(root.choices[3])
    root.nextBtn.config(state="disabled")
    root.feedback.set("") #reset the feedback


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

#Create Widgets
def createWidgets(root,top):
    # setting question frames
    def create_question_frames(container):
        frame = ttk.Frame(container)
        frame['borderwidth'] = 5
        frame['relief'] = 'solid'

        # Progress label
        root.label_progress = ttk.Label(
            frame,
            textvariable=root.ProgressText,
            font=("Aptos ExtraBold", 12)
        )
        root.label_progress.grid(column=0, row=0, columnspan=2, sticky="ew")

        # Question label
        root.label_question = ttk.Label(
            frame,
            textvariable=root.question,
            font=("Aptos ExtraBold", 15),
            wraplength=600,
            anchor="center",
            justify="center"
        )
        root.label_question.grid(column=0, row=1, columnspan=2, pady=10, sticky="nsew")

        frame.columnconfigure(0, weight=1)
        frame.columnconfigure(1, weight=1)

        # Auto-fit content to window
        def adjust_widgets(event):
            new_width = event.width - 50

            # Question label auto-fit
            root.label_question.config(wraplength=new_width)
            size = max(12, int(event.height / 30))
            root.label_question.config(font=("Aptos ExtraBold", size))

            # Feedback label auto-fit (if created)
            if hasattr(root, "label_feedback"):
                root.label_feedback.config(wraplength=new_width)
                fb_size = max(10, int(event.height / 40))
                root.label_feedback.config(font=("Aptos ExtraBold", fb_size, "bold"))

        root.bind("<Configure>", adjust_widgets)

        return frame

    #setting choices frame
    def create_buttons_frames(container):
        frame = ttk.Frame(container)
        frame['borderwidth'] = 5
        frame['relief'] = 'solid'
        frame.columnconfigure(0, weight=1)
        # Create multiple choices
        root.Button1 = ttk.Radiobutton(frame, style='info.Outline.Toolbutton', textvariable=root.O1,
                                       variable=root.user_selected, value=1, command=lambda: set_choices(1))
        root.Button2 = ttk.Radiobutton(frame, style='info.Outline.Toolbutton', textvariable=root.O2,
                                       variable=root.user_selected, value=2, command=lambda: set_choices(2))
        root.Button3 = ttk.Radiobutton(frame, style='info.Outline.Toolbutton', textvariable=root.O3,
                                       variable=root.user_selected, value=3, command=lambda: set_choices(3))
        root.Button4 = ttk.Radiobutton(frame, style='info.Outline.Toolbutton', textvariable=root.O4,
                                       variable=root.user_selected, value=4, command=lambda: set_choices(4))
        root.Button1.grid(column=0, row=0,sticky='w' , padx=20, pady=5)
        root.Button2.grid(column=0, row=1,sticky='w' , padx=20, pady=5)
        root.Button3.grid(column=0, row=2,sticky='w' , padx=20, pady=5)
        root.Button4.grid(column=0, row=3,sticky='w' , padx=20, pady=5)

        # buttons style
        style = ttk.Style()
        style.configure('info.Outline.Toolbutton', font=("Aptos ExtraBold", 12))

        return frame

    def create_interaction_frames(container):
        frame = ttk.Frame(container)
        frame['borderwidth'] = 5
        frame['relief'] = 'solid'
        # Control buttons
        root.quitBtn = ttk.Button(frame, text="Quit", command=root.quit)
        root.nextBtn = ttk.Button(frame, text="Next", command=lambda: next_question())
        root.quitBtn.grid(column=0, row=1,padx=10, pady=10)
        root.nextBtn.grid(column=1, row=1,padx=10, pady=10)
        # Score label
        root.label_score = ttk.Label(frame,text="Score:", font=("Arial", 14))
        root.label_score.grid(column=0, row=2,sticky="e")
        root.label_score_value = ttk.Label(frame,textvariable=root.score, font=("Arial", 12))
        root.label_score_value.grid(column=1, row=2,sticky="w")
        return frame
    def create_feedback_frame(container):
        frame = ttk.Frame(container)
        root.label_feedback = ttk.Label(
            frame,
            textvariable=root.feedback,
            font=("Aptos ExtraBold", 12, "bold"),
            foreground="green",
            anchor="center",
            justify="center"
        )
        root.label_feedback.grid(row=0, column=0, sticky="ew", padx=5, pady=5)
        frame.columnconfigure(0, weight=1)
        return frame

    # layout on the root window
    root.rowconfigure(0, weight=2)  # Question
    root.rowconfigure(1, weight=2)  # Choices
    root.rowconfigure(2, weight=1)  # Feedback
    root.rowconfigure(3, weight=1)  # Interaction
    root.columnconfigure(0, weight=1)

    questions_frame = create_question_frames(root)
    questions_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

    buttons_frame = create_buttons_frames(root)
    buttons_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)

    feedback_frame = create_feedback_frame(root)
    feedback_frame.grid(row=2, column=0, sticky="ew", padx=10, pady=5)

    interaction_frame = create_interaction_frames(root)
    interaction_frame.grid(row=3, column=0, sticky="ew", padx=10, pady=10)


    # Auto-fit content to window
    def adjust_widgets(event):
        new_width = event.width - 50
        # Question label auto-fit
        root.label_question.config(wraplength=new_width)
        size = max(12, int(event.height / 30))
        root.label_question.config(font=("Aptos ExtraBold", size))
        # Feedback label auto-fit
        root.label_feedback.config(wraplength=new_width)
        fb_size = max(10, int(event.height / 40))
        root.label_feedback.config(font=("Aptos ExtraBold", fb_size, "bold"))

    root.bind("<Configure>", adjust_widgets)


def create_main_window():
    root.geometry("750x700")
    root.resizable(True,True)
    menu()
    root.mainloop()

if __name__ == "__main__":
    create_main_window()