import tkinter as tk
from tkinter import *
from functools import partial
from PIL import ImageTk, Image
import logging, sys
from time import time, sleep, localtime
import argparse
import questionbank
import random
import re
import os

parser = argparse.ArgumentParser(description='This script takes a formatted .txt \
and feeds into a tkinter display, push one button to advance the test. Usage: \
python3 script_name.py quiz_01.txt')
parser.add_argument('filePath', help='A formatted .txt file path')
parser.add_argument("count", help="Number of questions to display randomly")
args = parser.parse_args()

logging.basicConfig(level=logging.DEBUG)


# logging.disable(logging.CRITICAL)

class First_Multiple_Guess(tk.Frame):
    """Simple trivia game: a question with 4 buttons as answers, pick any
       one to advance to the next question.
       Usage: python3 script.py trivia01.txt
       the text file needs to be formatted:
       1. Question line?
       A. answer one
       B. answer 2
       C. answer 3
       D. None of the above
       D
       """

    def __init__(self, file_path, count, parent=None):
        # create widgets and base attributes
        self.filePath = file_path
        self.dirPath = os.path.dirname(file_path)
        self.parent = parent
        self.parent.title("Vishal's Quiz")
        tk.Frame.__init__(self, self.parent)
        self.pack(expand='yes', fill='both')
        self.canvas = tk.Canvas(self)
        self.canvas.config(width=1500, height=700, bg="skyblue")
        self.canvas.pack(expand=True, fill=tk.BOTH)
        self.font = ('monospace', 14)
        self.questions = []
        self.answers = []
        self.solutions = []
        self.count = 0
        self.g_count = 0
        self.a_count = 0
        self.win_count = 0
        self.loss_count = 0
        self.total_count = 0
        self.questions = questionbank.read(self.filePath)
        self.length_quest = len(self.questions)
        self.count = int(count)
        self.rendered = 0
        self.used = []
        self.score = []
        self.frame = None
        self.row = 0
        self.build_puzzle()

    def create_container(self):
        frame = tk.Frame(self.parent, bg="skyblue")
        frame.place(x=0, y=0, relheight=1, relwidth=1)

        canvas = Canvas(frame, bg="skyblue")
        self.frame = Frame(canvas, bg="skyblue")
        myscrollbar = Scrollbar(frame, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=myscrollbar.set)

        myscrollbar.pack(side="right", fill="y")
        canvas.pack(side="left", expand=True, fill=BOTH)
        canvas.create_window((0, 0), window=self.frame, anchor='nw')

        def myfunction(event):
            canvas.configure(scrollregion=canvas.bbox("all"))

        frame.bind("<Configure>", myfunction)

    def build_puzzle(self):
        '''Build and place label and 4 buttons use for loop to
           step through a list answers. Partial funtion to assign the solution
           to each button.'''
        # main loop
        num = random.randint(0, self.length_quest - 1)
        while num in self.used:
            num = random.randint(0, self.length_quest - 1)
        self.used.append(num)
        #num = self.rendered
        quest = self.questions[num]
        self.rendered += 1

        if self.frame:
            for widget in self.frame.winfo_children():
                widget.destroy()
            self.frame.pack_forget()

        self.create_container()

        self.row = 0
        Label(self.frame, text="Question Number " + str(self.rendered) + " of " + str(self.count), font=('monotype', '18','bold'), wraplength=1400, anchor="w", justify="left",
              bg="skyblue").grid(row=self.row, column=0)
        self.row += 1
        self.display_question_text(quest.text)
        index = 65
        options = []
        for opt in quest.options:
            val = IntVar()
            self.display_option_text(chr(index) + ". " + opt, val)
            index += 1
            options.append(val)

        Button(self.frame, text="Submit",
                  command=partial(self.check_ans, options, num),
                  font=self.font).grid(row=self.row, column=0)
        self.row += 1

        self.solution_var = StringVar()
        self.solution_var.set(" \n \n \n ")
        Label(self.frame, textvariable=self.solution_var, font=self.font, wraplength=1400, anchor="w", justify="left", bg="skyblue").grid(
            row=self.row, column=0)
        self.row += 1

    def display_question_text(self, text):
        images = re.findall(r"!!![^!]*!!!", text)
        if len(images) > 0:
            parts = re.split("!!![^!]*!!!", text)
            index = 0
            for part in parts:
                Label(self.frame, text=part, font=self.font, wraplength=1400, anchor="w", justify="left",
                      bg="skyblue").grid(row=self.row, column=0, sticky=W)
                self.row += 1
                if index < len(images):
                    src = images[index][3:-3]
                    im = Image.open(self.dirPath + "/images/" + src)
                    #im.show()
                    img = ImageTk.PhotoImage(im)
                    lbl = tk.Label(self.frame, image=img)
                    lbl.image = img
                    lbl.grid(row=self.row, column=0, sticky=W)
                    self.row += 1
                index += 1
        else:
            Label(self.frame, text=text, font=self.font, wraplength=1400, anchor="w", justify="left",
                  bg="skyblue").grid(row=self.row, column=0, sticky=W)
            self.row += 1

    def display_option_text(self, text, val):
        images = re.findall(r"!!![^!]*!!!", text)
        if len(images) > 0:
            parts = re.split("!!![^!]*!!!", text)
            index = 0
            for part in parts:
                if index == 0:
                    Checkbutton(self.frame, text=part, variable=val, anchor="w", wraplength=1400,
                                justify="left", bg="skyblue").grid(row=self.row, column=0, sticky=W)
                else:
                    Label(self.frame, text=part, font=self.font, wraplength=1400, anchor="w", justify="left",
                      bg="skyblue").grid(row=self.row, column=0, sticky=W)

                self.row += 1
                if index < len(images):
                    src = images[index][3:-3]
                    im = Image.open(self.dirPath + "/images/" + src)
                    #im.show()
                    img = ImageTk.PhotoImage(im)
                    lbl = tk.Label(self.frame, image=img)
                    lbl.image = img
                    lbl.grid(row=self.row, column=0, sticky=W)
                    self.row += 1
                index += 1
        else:
            Checkbutton(self.frame, text=text, variable=val, anchor="w", wraplength=1400,
                        justify="left", bg="skyblue").grid(row=self.row, column=0, sticky=W)
            self.row += 1


    def check_ans(self, options, qid):
        """Comparing the solution to the answer,
           and keep track of wins and losses,
           check for last question."""
        answers = self.questions[qid].answers
        is_pass = True
        index = 65
        chosen = []
        for opt in options:
            if opt.get() == 1:
                chosen.append(chr(index))
                if chr(index) not in answers:
                    is_pass = False
            index += 1

        self.answers.append(chosen)

        self.total_count += 1
        if is_pass:
            self.win_count += 1
            timeout = 1000
        else:
            self.loss_count += 1
            timeout = 12000

        if self.total_count == self.count:
            text = "You choose : " + ",".join(chosen) + " Correct Answer : " + ",".join(answers)
            num = "Topic 2 #" + str(qid -107) if qid > 107 else "Topic 1 #" + str(qid + 1)
            if not is_pass:
                text += "\nQuestion: " + num
            text += '\nCorrect answers: {:.2%}'.format(self.win_count / self.total_count)
            self.solution_var.set(text)
            #Label(self.frame, text=text, font=self.font, wraplength=1400, anchor="w", justify="left", bg="skyblue").grid(row=self.row, column=0)
        else:
            text = "You choose : " + ",".join(chosen) + " Correct Answer : " + ",".join(answers)
            num = "Topic 2 #" + str(qid - 107) if qid > 107 else "Topic 1 #" + str(qid + 1)
            if not is_pass:
                text += "\nQuestion: " + num

            self.solution_var.set(text)
            #Label(self.frame, text=text, font=self.font, wraplength=1400, anchor="w", justify="left",
            #      bg="skyblue").grid(row=self.row, column=0)
            self.canvas.after(timeout, self.build_puzzle)
        self.row += 1


if __name__ == '__main__':
    filePath = args.filePath
    count = args.count
    root = tk.Tk()
    root.geometry("1420x600")
    First_Multiple_Guess(filePath, count, root)
    root.mainloop()