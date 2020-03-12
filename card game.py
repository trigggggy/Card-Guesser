# TIE-02100 Johdatus ohjelmointiin
# TIE-02106 Introduction to Programming
# 272571 Sanghun Lee (sanghun.lee@tuni.fi)

'''
This program is a simple number guessing card game. when the game initializes, it automatically generates pseudo random numbers with 'random'. 
When player answers number between 1-9 and then submit, the fucntion 'submit_answer' will check if the value is correct or not. 
if answer is correct, specific card image is opened then entry and button of it will be disabled.
Player can win this game by answering every cards before it's life going under 0.
If there's no more life, program, itself disables every entries and buttons except for start and finish game button.

This GUI program is scalable by deciding how many cards player is guessing. Number of cards can be decided by 'CARD_NUMBER'
'''

from tkinter import *
import random
import math


CARD_PIC = [ "0.png", "1.png", "2.png", "3.png", "4.png", "5.png", "6.png", "7.png" , "8.png" , "9.png"  ]

LIFE = 10
CARD_NUMBER = 9



class Dicegame:
    def __init__(self):
        self.__window = Tk()
        self.__window.title("Card guessing game")

        self.__cardpics = []
        for picfile in CARD_PIC:
            pic = PhotoImage(file=picfile)
            self.__cardpics.append(pic)

        #Card pictures
        self.__cardpiclabels = []
        for i in range(CARD_NUMBER):
            new_label = Label(self.__window)
            new_label.grid(row=1, column=i)
            self.__cardpiclabels.append(new_label)

        #Answer input entries
        self.__answerentries = []
        for i in range(CARD_NUMBER):
            new_entry = Entry(self.__window, width=2)
            new_entry.grid(row=2, column=i)
            self.__answerentries.append(new_entry)

        #Answer submit buttons
        self.__submitbuttons = []
        self.__toggle = [0] * CARD_NUMBER
        for i in range(CARD_NUMBER):
            new_button = Button(self.__window, command=lambda k=i: (self.submit_answer(k)))
            new_button.grid(row=3, column=i)
            self.__submitbuttons.append(new_button)

        Button(self.__window, text="new game", command=self.initialize_game)\
            .grid(row=0, column=math.floor(CARD_NUMBER/2), sticky=W+E+N)
        Button(self.__window, text="Close", command=self.__window.destroy)\
            .grid(row=6, column=math.floor(CARD_NUMBER/2), sticky=W+E+S)

        #life label
        self.__lifelabel  = Label(self.__window)
        self.__lifelabel.grid(row=4, column=0, columnspan=CARD_NUMBER)
        self.__gamesituationtext=""

        #Game status info label
        self.__infolabel = Label(self.__window)
        self.__infolabel.grid(row=5, columnspan=CARD_NUMBER, sticky=W+E+S)
        self.initialize_game()

    def initialize_game(self):
        self.__turn = 0
        self.__life = LIFE
        self.corrects = 0

        #Show the empty card image
        for label in self.__cardpiclabels:
            label.configure(image=self.__cardpics[0])
        
        #Setting random numbers
        self.__cards = [0] * CARD_NUMBER
        for i in range(len(self.__cards)):
            self.__cards[i] = random.randint(1, 9)

        self.__gamesituationtext = ""

        self.reset_inputs()

        self.update_ui_texts()


    def reset_inputs(self):
        # Setting all the buttons and entries to initial state.
        for button in self.__submitbuttons:
            button.configure(text="Submit")      
            button.configure(state=NORMAL)
        for entry in self.__answerentries:
            entry.delete(0, END)
            entry.configure(state=NORMAL)

    def update_ui_texts(self):
        # Displaying player's life
        self.__lifetext = str(self.__life)+" life left."
        self.__lifelabel.configure(text=self.__lifetext)
        #updating system message
        self.__infolabel.configure(text=self.__gamesituationtext)

    def submit_answer(self, num):


        try:
            input_val = int(self.__answerentries[num].get())
            #check input_val
            if input_val > 9:
                self.__gamesituationtext = "You must enter number from 1 to 9"
                self.__answerentries[num].delete(0, END)
            elif input_val < 1:
                self.__gamesituationtext = "You must enter number from 1 to 9"
                self.__answerentries[num].delete(0, END)
            else: 
                # check answer is correct. If correct, add 1 point to life. If not, remove 1 point from life.
                if input_val == self.__cards[num]:
                    self.__life+=1
                    self.__cardpiclabels[num].configure(image=self.__cardpics[self.__cards[num]])
                    #Disable entry and button for the correct one
                    self.__gamesituationtext = "You got 1 point"
                    self.__answerentries[num].configure(state=DISABLED)
                    self.__submitbuttons[num].configure(state=DISABLED)


                    self.corrects += 1
                    if self.corrects == CARD_NUMBER:
                        self.__gamesituationtext = "Congratz!! You won the game, start new game please"
                        for button in self.__submitbuttons:
                            button.configure(text="DISABLED")      
                            button.configure(state=DISABLED) 

                else:
                    self.__life-=1
                    self.__gamesituationtext = "You lost 1 point"
                    if self.__life <= 0:
                        self.__gamesituationtext = "You lost the game, start new game please"
                        for button in self.__submitbuttons:
                            button.configure(text="DISABLED")      
                            button.configure(state=DISABLED)
        except ValueError:
            self.__gamesituationtext = "You must enter number from 1 to 9"
            self.__answerentries[num].delete(0, END)

        
        self.update_ui_texts()
    
    
    
    def start(self):
        self.__window.mainloop()

def main():
    ui = Dicegame()
    ui.start()


main()
