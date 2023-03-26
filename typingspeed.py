import ast
import tkinter
from tkinter import *
from datetime import timedelta
import random


class TypingSpeedApp:
    def __init__(self):
        # define start_time as total time for typing and second as decrement
        self.start_time = timedelta(minutes=1, seconds=1)
        self.second = timedelta(minutes=0, seconds=1)
        # create gui
        self.typing_speed_app = Tk()
        self.typing_speed_app.title("Typing Speed Application")
        self.typing_speed_app.minsize(1200, 700)
        self.typing_speed_app.resizable(False, False)
        # define background image
        self.background_image = PhotoImage(file="images/background_image.PNG")
        # create canvas
        self.canvas = Canvas(self.typing_speed_app, width=1200, height=700)
        self.canvas.pack(fill="both", expand=True)
        # set image in canvas
        self.canvas.create_image(0, 0, image=self.background_image, anchor="nw")
        # add a label for title
        self.canvas.create_text(590, 50, text="Welcome to typing speed application", font=("Helvetica", 30),
                                fill="white")
        # add a label for Base text
        self.canvas.create_text(130, 90, text="Base text:", font=("Helvetica", 20), fill="white", state=DISABLED)

        # Define Entry Box for Base text
        self.base_text = tkinter.Text(self.typing_speed_app, font=("Helvetica", 24), width=60, height=3, bd=0,
                                      wrap=tkinter.WORD)
        self.base_text_window = self.canvas.create_window(70, 120, anchor="nw", window=self.base_text)
        # add a label for Type here
        self.canvas.create_text(130, 270, text="Type here:", font=("Helvetica", 20), fill="white")
        # Define Entry Box for Text
        self.type_text = Text(self.typing_speed_app, font=("Helvetica", 24), width=20, height=1, bd=0,
                              wrap=tkinter.WORD, state=DISABLED)
        self.type_text_window = self.canvas.create_window(70, 300, anchor="nw", window=self.type_text)
        # add a label for timer
        self.canvas.create_text(510, 270, text="Timer:", font=("Helvetica", 20), fill="white")
        # Define Entry Box for timer
        self.time_text = Text(self.typing_speed_app, font=("Helvetica", 24), width=5, height=1, bd=0,
                              background="green")
        # set initial value to avoid loosing one second when start button si clicked
        self.time_text.insert(1.0, "01:00")
        self.time_text_window = self.canvas.create_window(470, 300, anchor="nw", window=self.time_text)
        # start button
        self.start = Button(self.typing_speed_app, text="START", font=("Helvetica", 12), bd=0,
                            command=self.update_timer)
        self.start_window = self.canvas.create_window(600, 300, anchor="nw", window=self.start, height=37, width=70)
        # RESET BUTTON
        self.reset = Button(self.typing_speed_app, text="RESET", font=("Helvetica", 12), bd=0, command=self.reset_app)
        self.reset_window = self.canvas.create_window(700, 300, anchor="nw", window=self.reset, height=37, width=70)
        # gold image
        self.gold_image = PhotoImage(file="images/1.PNG")
        self.canvas.create_image(400, 400, anchor="nw", image=self.gold_image)
        self.place1_text = Text(self.typing_speed_app, font=("Helvetica", 24), width=20, height=1, bd=0,
                                wrap=tkinter.WORD)
        self.type_text_window = self.canvas.create_window(490, 420, anchor="nw", window=self.place1_text)
        # silver image
        self.silver_image = PhotoImage(file="images/2.PNG")
        self.canvas.create_image(400, 500, anchor="nw", image=self.silver_image)
        self.place2_text = Text(self.typing_speed_app, font=("Helvetica", 24), width=20, height=1, bd=0,
                                wrap=tkinter.WORD)
        self.place2_text_window = self.canvas.create_window(490, 520, anchor="nw", window=self.place2_text)
        # bronze image
        self.bronze_image = PhotoImage(file="images/3.PNG")
        self.canvas.create_image(400, 600, anchor="nw", image=self.bronze_image)
        self.place3_text = Text(self.typing_speed_app, font=("Helvetica", 24), width=20, height=1, bd=0,
                                wrap=tkinter.WORD)
        self.place3_text_window = self.canvas.create_window(490, 620, anchor="nw", window=self.place3_text)

        # text get from base_text
        self.base_text_get_test = ""
        # this list contain indexes of spaces in text inserted in Base text
        self.space_indexes = ["1.0"]
        # define index for select parts of space_indexes
        self.index = 0
        # attribute contain text get from type_here
        self.text_from_type_text = ""
        # define a bind for space release
        self.type_text.bind("<KeyRelease-space>", self.space_detected)
        # number of correct words
        self.correct_words = 0
        # name list contain users name in descending score order
        self.name = []
        # score list contain score in descending order
        self.score = []
        # in read text from scores.txt as scores_dict
        self.scores_dict = {}
        # scores_dict sorted by value
        self.sorted_by_score_value = {}
        # 3rd score
        self.min = 0

    # show gui
    def main_loop(self):
        self.typing_speed_app.mainloop()

    # read text from text_1.txt, remove [ and ' from start and final; and " " at end for identifying last word from text
    def read_text_file(self):
        # read a random file from files directory
        with open(f'files/text_{random.randint(1, 3)}.txt') as text_file:
            lines = str(text_file.readlines())
        self.base_text.insert(1.0, lines[2:-2] + " ")
        # disable base_text for avoiding text change
        self.base_text.configure(state=DISABLED)
        # get text inserted in base text
        self.base_text_get_test = self.base_text.get(1.0, tkinter.END)

    # update scores in gui
    def update_scores(self):
        # delete all scores
        self.place1_text.delete(1.0, END)
        self.place2_text.delete(1.0, END)
        self.place3_text.delete(1.0, END)
        # open scores.txt as a dictionary scores_dict
        with open("files/scores.txt") as scores:
            self.scores_dict = ast.literal_eval(scores.read())
        # sort descending above dictionary
        self.sorted_by_score_value = {k: v for k, v in sorted(self.scores_dict.items(), key=lambda v: v[1], reverse=True)}
        # based on sorted dictionary create name list and score list
        for key in self.sorted_by_score_value.keys():
            self.name.append(key)
        for value in self.sorted_by_score_value.values():
            self.score.append(value)
        # insert first 3 names and scores in score gui
        self.place1_text.insert(1.0, f"{self.name[0]} score {self.score[0]}")
        self.place2_text.insert(1.0, f"{self.name[1]} score {self.score[1]}")
        self.place3_text.insert(1.0, f"{self.name[2]} score {self.score[2]}")
        # disable places text to avoid change score by edit
        self.place1_text.configure(state=DISABLED)
        self.place2_text.configure(state=DISABLED)
        self.place3_text.configure(state=DISABLED)
        # set for min value 3rd score
        self.min = self.score[2]

    # if user obtain a better score then first 3 already existing score places_text is change
    def change_score_function(self):
        # define gui for new window
        self.change_score = Tk()
        self.change_score.title("Good job!!!")
        self.change_score.minsize(width=200, height=200)
        self.change_score.resizable(False, False)
        # create canvas for new window
        self.canvas_change_score = Canvas(self.change_score, width=600, height=500)
        self.canvas_change_score.pack(fill="both", expand=True)
        # set master for using image in new canvas
        self.background_image_score = PhotoImage(file="images/record.PNG", master=self.canvas_change_score)
        # set image in canvas
        self.canvas_change_score.create_image(0, 0, image=self.background_image_score, anchor="nw")
        # create text in new canvas
        self.canvas_change_score.create_text(300, 50, text="       You set a new record!!! \n Please enter your name"
                                                           " below:",
                                             font=("Helvetica", 20), fill="white", state=DISABLED)
        # create Text in new canvas
        self.new_score_name = Text(self.change_score, font=("Helvetica", 24), width=20, height=1, bd=0,)
        # place cursor in Text
        self.new_score_name.focus_set()
        self.new_score_name_window = self.canvas_change_score.create_window(130, 100, anchor="nw",
                                                                            window=self.new_score_name)
        # create save button in new canvas
        self.save_button = Button(self.change_score, text="Save", font=("Helvetica", 12), bd=0, command=self.save_to_txt)
        self.save_button_window = self.canvas_change_score.create_window(270, 180, anchor="nw", window=self.save_button,
                                                                         height=37, width=70)

    # add new score value in scores.txt file
    def save_to_txt(self):
        # read all from scores.txt
        with open("files/scores.txt", "r") as scores_file:
            data = scores_file.read()
        # remove } and add , "new_name":new_score}
        date_to_write = data[:-1] + "," + f'"{(self.new_score_name.get(1.0, END))[:-1]}":{self.correct_words}' + "}"
        # save nwe score in scores.txt
        with open("files/scores.txt", "w") as scores_file:
            scores_file.write(date_to_write)
        # close new canvas
        self.change_score.destroy()

    # find index of " " in base text and add those in space_interval list
    def find_space_intervals(self):
        idx = '1.0'
        while True:
            idx = self.base_text.search(" ", idx, stopindex=END)
            if not idx:
                break
            last_idx = '%s+%dc' % (idx, 1)
            self.space_indexes.append(idx)
            self.space_indexes.append(last_idx)
            idx = last_idx

    # change background color for words from base text in gray color
    def gray_background(self):
        self.base_text.tag_add("select", self.space_indexes[self.index], self.space_indexes[self.index + 1])
        self.base_text.tag_configure("select", background="gray")
        self.base_text.see(f"{self.space_indexes[self.index]}")

    # when space key is release
    def space_detected(self, event):
        # get text from type here and remove last 2 elements
        self.text_from_type_text = (self.type_text.get(1.0, tkinter.END))[:-2]
        # if text get from type here is identical with word from base text change background to green
        if self.text_from_type_text == self.base_text.get(self.space_indexes[self.index], self.space_indexes[
                                               self.index + 1]):
            self.base_text.tag_add("green", self.space_indexes[self.index], self.space_indexes[self.index + 1])
            self.base_text.tag_configure("green", background="green")
            # add one to number of correct word
            self.correct_words += 1
        # if text get from type here differs with word from base text change word background in red
        elif self.text_from_type_text != self.base_text.get(self.space_indexes[self.index], self.space_indexes[
                     self.index + 1]):

            self.base_text.tag_add("red", self.space_indexes[self.index], self.space_indexes[self.index + 1])
            self.base_text.tag_configure("red", background="red")
        # delete text from type here
        self.type_text.delete(1.0, END)
        # increase index with 2 for select next word with space_indexes
        self.index += 2
        # change background in gray for next word
        self.gray_background()

    # update timer
    def update_timer(self):
        # if type text state is disable make it normal
        if self.type_text['state'] == DISABLED:
            self.type_text.configure(state=NORMAL)
        # place curser in type
        self.type_text.focus_set()
        # if start button state is normal make it disable
        if self.start['state'] == NORMAL:
            self.start.configure(state=DISABLED)
        # string contain start_time - one second (ex 01:00)
        string = str(self.start_time - self.second)[2::]
        # insert above string in time_text
        self.time_text.insert(1.0, string)
        # subtract one second from start_time
        self.start_time -= self.second
        # if 00:00
        if str(self.start_time)[2:4] == "00" and str(self.start_time)[5::] == "00":
            # delete text from type text
            self.type_text.delete(1.0, END)
            # insert in type text number of correct words
            self.type_text.insert(1.0, str(self.correct_words))
            # update gui
            self.typing_speed_app.update()
            # make type text disable
            self.type_text.configure(state=DISABLED)
            # unbind KeyRelease-space
            self.type_text.unbind("<KeyRelease-space>")
            # if current score is better than 3rd score call change_score_function
            if self.correct_words > self.min:
                self.change_score_function()
            # leave method
            pass
        # if timer differ from 00:00
        else:
            # wait 1000ms and update time
            self.time_text.after(1000, self.update_timer)

    # reset app
    def reset_app(self):
        self.typing_speed_app.destroy()
        self.__init__()
        self.read_text_file()
        self.find_space_intervals()
        self.update_scores()
        self.gray_background()
