import tkinter as tk
import tkinter.ttk as ttk
from PIL import ImageTk, Image  
import os
import random
import time
from re import search


WIDTH = 500
HEIGHT = 500

DEALER_1_X = 40
DEALER_1_Y = 40

DEALER_2_X = 130
DEALER_2_Y = 40

DEALER_3_X = 220
DEALER_3_Y = 40

DEALER_4_X = 310
DEALER_4_Y = 40

DEALER_5_X = 400
DEALER_5_Y = 40

PLAYER_1_X = 40
PLAYER_1_Y = 235

PLAYER_2_X = 130
PLAYER_2_Y = 235

PLAYER_3_X = 220
PLAYER_3_Y = 235

PLAYER_4_X = 310
PLAYER_4_Y = 235

PLAYER_5_X = 400
PLAYER_5_Y = 235

HIT_POS_X = 40
HIT_POS_Y = 350

STAND_POS_X = 70
STAND_POS_Y = 350

DEALER_POSITIONS_ARRAY = [[DEALER_1_X, DEALER_1_Y], [DEALER_2_X, DEALER_2_Y], [DEALER_3_X, DEALER_3_Y], [DEALER_4_X, DEALER_4_Y], [DEALER_5_X, DEALER_5_Y]]
PLAYER_POSITIONS_ARRAY = [[PLAYER_1_X, PLAYER_1_Y], [PLAYER_2_X, PLAYER_2_Y], [PLAYER_3_X, PLAYER_3_Y], [PLAYER_4_X, PLAYER_4_Y], [PLAYER_5_X, PLAYER_5_Y]]

cards = ["king1", "king2", "king3", "king4", "queen1", "queen2", "queen3", "queen4", "jack1", "jack2", "jack3", "jack4",
         "ace1", "ace2", "ace3", "ace4", "two_1", "two_2", "two_3", "two_4", "three_1", "three_2", "three_3", "three_4",
         "four_1", "four_2", "four_3", "four_4", "five_1", "five_2", "five_3", "five_4", "six_1", "six_2", "six_3", "six_4",
         "seven_1", "seven_2", "seven_3", "seven_4", "eight_1", "eight_2", "eight_3", "eight_4", "nine_1", "nine_2", "nine_3", "nine_4",
         "ten_1", "ten_2", "ten_3", "ten_4"]

used_cards = []

placeholder_card_img = "sprites/card_placeholder.png"
flipped_card_img = "sprites/card_back.png"

about_message = '''Welcome to Blackjack (21)! This is a simple computer version of the game Blackjack (21) designed in the style of the classic 
Microsoft Card games that used to be included in Windows Operating Systems in the past. Specifically, this game was designed in the style of the 
Windows XP version of these card games such as Solitaire. The goal is to get a higher score than your opponent without going over 21.'''


class App(tk.Frame):
    
    total_score = 0
    hit_number = 0
    ace_11_check = False
    
    dealer_score = 0
    dealer_hit_num = 0
    dealer_facedown_card = ""
    
    def __init__(self, window):
         
        super().__init__(window)
        window.title("Blackjack (21)")
        window.geometry("{}x{}".format(WIDTH, HEIGHT))
        
        menu_bar = tk.Menu(window)
        game_menu = tk.Menu(menu_bar, tearoff=0)
        game_menu.add_command(label="New Game", command=lambda: self.new_game(window))
        game_menu.add_separator()
        game_menu.add_command(label="Exit", command=window.destroy)
        menu_bar.add_cascade(label="Game", menu=game_menu)
        
        help_menu = tk.Menu(window)
        help_menu = tk.Menu(menu_bar, tearoff=0)
        help_menu.add_command(label="About", command=lambda: self.about_msg_box())
        menu_bar.add_cascade(label="Help", menu=help_menu)
        
        window.configure(bg="green", menu=menu_bar)

        self.background_setup(window)
        
        self.deal_cards(window)
        
        self.dealer_cards(window)
        
        print("total score: ", self.total_score)
                
        self.hit_button = tk.Button(window, text="Hit",  state=tk.NORMAL, command=lambda: self.hit(window))
        self.hit_button.place(x=HIT_POS_X, y=HIT_POS_Y)
        
        self.stand_button = tk.Button(window, text="Stand", state=tk.NORMAL, command=lambda: self.add_dealer_cards(window))
        self.stand_button.place(x=STAND_POS_X, y=STAND_POS_Y)
        
            


    def new_game(self, window):
        for widget in window.winfo_children():
            if ((type(widget) == tk.Label) or (type(widget) == tk.Button)):
                widget.destroy()
        
        self.total_score = 0
        self.hit_number = 0
        
        self.dealer_score = 0
        self.dealer_hit_num = 0
        self.dealer_facedown_card = ""
        
        self.background_setup(window)
        
        self.deal_cards(window)
        
        self.dealer_cards(window)
        
        print("total score: ", self.total_score)
                
        self.hit_button = tk.Button(window, text="Hit",  state=tk.NORMAL, command=lambda: self.hit(window))
        self.hit_button.place(x=HIT_POS_X, y=HIT_POS_Y)
        
        self.stand_button = tk.Button(window, text="Stand", command=lambda: self.add_dealer_cards(window))
        self.stand_button.place(x=STAND_POS_X, y=STAND_POS_Y)
        

    # deal cards to the player
    def deal_cards(self, window):
        
        # Player Card 1 
        card1_str = random.choice(cards)
        card1 = Image.open("sprites/{}.png".format(card1_str))
        ph = ImageTk.PhotoImage(card1, master=window)
        label1 = tk.Label(window, image=ph)
        label1.image = ph
        label1.place(x=PLAYER_1_X, y=PLAYER_1_Y)
        window.after(500, window.update())
        
        # Player Card 2
        card2_str = random.choice(cards)
        card2 = Image.open("sprites/{}.png".format(card2_str))
        ph1 = ImageTk.PhotoImage(card2, master=window)
        label2 = tk.Label(window, image=ph1)
        label2.image = ph1
        label2.place(x=PLAYER_2_X, y=PLAYER_2_Y)
        window.after(500, window.update())
        
        
        # find card 1's and 2's value
        self.total_score += self.get_card_value(self.total_score, card1_str)
        self.total_score += self.get_card_value(self.total_score, card2_str)
        


    # gives the player an additional card
    def hit(self, window):
        
        
        pos_x, pos_y = 0, 0
        hit_value = 0

        hit_card_str = random.choice(cards)
        hit_card = Image.open("sprites/{}.png".format(hit_card_str))
        hit_ph = ImageTk.PhotoImage(hit_card, master=window)
        hit_label = tk.Label(window, image=hit_ph)
        hit_label.image = hit_ph
        
        
        hit_value = self.get_card_value(self.total_score, hit_card_str)
        
        # Check if ace value can still be 11 in the context of the code
        if ((self.ace_11_check == True) and (self.total_score+hit_value > 21) and ((self.total_score-10)+hit_value < 21)):
            self.total_score -= 10
            self.ace_11_check = False
            print("wtf")
        
        if (self.hit_number == 0):
            pos_x, pos_y = PLAYER_3_X, PLAYER_3_Y
            self.total_score += hit_value
        elif (self.hit_number == 1):
            pos_x, pos_y = PLAYER_4_X, PLAYER_4_Y
            self.total_score += hit_value
        else:
            pos_x, pos_y = PLAYER_5_X, PLAYER_5_Y
            self.total_score += hit_value
        print("total score: ", self.total_score)
        hit_label.place(x=pos_x, y=pos_y)
        self.hit_number += 1
        
        if (self.total_score > 21):
            self.end_msg_box(window)
            
        if (self.total_score == 21):
            self.add_dealer_cards(window)

    
    
    # Get the value of a given card
    def get_card_value(self, score, card_str):
        
        if (("king" in card_str) or ("queen" in card_str) 
            or ("jack" in card_str) or ("ten" in card_str)):  
            card_value = 10
        elif ("ace" in card_str):
            if (score + 11 > 21):
                card_value = 1
            else:
                card_value = 11
                # self.ace_11_check = True # Try to figure out how to do this without making a duplicate function
        elif ("two" in card_str):
            card_value = 2
        elif ("three" in card_str):
            card_value = 3
        elif ("four" in card_str):
            card_value = 4
        elif ("five" in card_str):
            card_value = 5
        elif ("six" in card_str):
            card_value = 6
        elif ("seven" in card_str):
            card_value = 7
        elif ("eight" in card_str):
            card_value = 8
        elif ("nine" in card_str):
            card_value = 9
        
        return card_value
    
    
    # Generate the dealer's cards
    def dealer_cards(self, window):
        # Player Card 1 
        card1_str = random.choice(cards)
        card1 = Image.open("sprites/{}.png".format(card1_str))
        ph = ImageTk.PhotoImage(card1, master=window)
        label1 = tk.Label(window, image=ph)
        label1.image = ph
        label1.place(x=DEALER_1_X, y=DEALER_1_Y)
        window.after(500, window.update())
        
        self.dealer_score += self.get_card_value(self.dealer_score, card1_str)
        print("dealer_score: ", self.dealer_score)
        card2_str = random.choice(cards)
        natural_check = self.get_card_value(self.dealer_score, card2_str)
        print("natural_check: ", natural_check)
        print("dealer_score now if natural check is applied: ", natural_check + self.dealer_score)
        if ((natural_check + self.dealer_score == 21) or (self.total_score == 21)):
            print("Dealer should win or player had 21 or they had it equal?")
            self.dealer_score += natural_check
            card2 = Image.open("sprites/{}.png".format(card2_str))
            ph1 = ImageTk.PhotoImage(card2, master=window)
            label2 = tk.Label(window, image=ph1)
            label2.image = ph1
            label2.place(x=DEALER_2_X, y=DEALER_2_Y)
            window.after(500, window.update())
            self.end_msg_box(window)
        else:
            card2 = Image.open(flipped_card_img)
            ph2 = ImageTk.PhotoImage(card2, master=window)
            label2 = tk.Label(window, image=ph2)
            label2.image = ph2
            label2.place(x=DEALER_2_X, y=DEALER_2_Y)
            self.dealer_facedown_card = card2_str
            window.after(500, window.update())
        
        
    # add dealer cards once the player stands
    def add_dealer_cards(self, window):
        self.hit_button['state'] = tk.DISABLED
        self.stand_button['state'] = tk.DISABLED
        
        pos_x, pos_y = 0, 0
        deal_hit_value = 0
        deal_hit_card_str = ""
        
        while (self.dealer_score < 17 and self.dealer_hit_num <= 3):
            if (self.dealer_hit_num == 0):
                deal_hit_card_str = self.dealer_facedown_card
            else:
                deal_hit_card_str = random.choice(cards)
            
            deal_hit_card = Image.open("sprites/{}.png".format(deal_hit_card_str))
            deal_hit_ph = ImageTk.PhotoImage(deal_hit_card, master=window)
            deal_hit_label = tk.Label(window, image=deal_hit_ph)
            deal_hit_label.image = deal_hit_ph
            
            
            deal_hit_value = self.get_card_value(self.dealer_score, deal_hit_card_str)
            
            if (self.dealer_hit_num == 0):
                pos_x, pos_y = DEALER_2_X, DEALER_2_Y
                self.dealer_score += deal_hit_value
            elif (self.dealer_hit_num == 1):
                pos_x, pos_y = DEALER_3_X, DEALER_3_Y
                self.dealer_score += deal_hit_value
            elif (self.dealer_hit_num == 2):
                pos_x, pos_y = DEALER_4_X, DEALER_4_Y
                self.dealer_score += deal_hit_value
            else:
                pos_x, pos_y = DEALER_5_X, DEALER_5_Y
                self.dealer_score += deal_hit_value
                
            print("dealer score: ", self.dealer_score)
            deal_hit_label.place(x=pos_x, y=pos_y)
            self.dealer_hit_num += 1
            
            window.after(500, window.update())
            
        self.end_msg_box(window)
        
    # Set up initial background
    def background_setup(self, window):
        
        dealer_text = tk.Label(window, text="Dealer:", bg="green"
                               , fg="white")
        dealer_text.config(font=(20))
        dealer_text.place(x=10, y=10)

        you_text = tk.Label(window, text="You:", bg="green"
                               , fg="white")
        you_text.config(font=(20))
        you_text.place(x=10, y=200)
        
        for i in range(len(DEALER_POSITIONS_ARRAY)):
            dealer_placeholder_card = Image.open(placeholder_card_img)
            dealer_ph = ImageTk.PhotoImage(dealer_placeholder_card, master=window)
            dealer_label = tk.Label(window, image=dealer_ph)
            dealer_label.image = dealer_ph
            dealer_label.place(x=DEALER_POSITIONS_ARRAY[i][0], y=DEALER_POSITIONS_ARRAY[i][1])
            
        for i in range(len(PLAYER_POSITIONS_ARRAY)):
            player_placeholder_card = Image.open(placeholder_card_img)
            player_ph = ImageTk.PhotoImage(player_placeholder_card, master=window)
            player_label = tk.Label(window, image=player_ph)
            player_label.image = player_ph
            player_label.place(x=PLAYER_POSITIONS_ARRAY[i][0], y=PLAYER_POSITIONS_ARRAY[i][1])

        
    # Help message box
    def about_msg_box(self):
        msgbox = tk.messagebox.showinfo(title="About this Game", message=about_message)
        return msgbox
    
    # Game Over message box
    def end_msg_box(self, window):
        end_message = "You Lose! You have a score of {} and the dealer has a score of {}".format(self.total_score, self.dealer_score)
        
        
        if ((self.total_score > self.dealer_score) and (self.total_score <= 21)):
            end_message = "You Win! You have a score of {} and the dealer has a score of {}".format(self.total_score, self.dealer_score)
        elif ((self.dealer_score > 21) and (self.total_score <= 21)):
            end_message = "You Win! The dealer went over"
        elif (self.total_score > 21):
            end_message = "You Lose! You went over"
        elif (self.total_score == self.dealer_score):
            end_message = "Game Over! It's a draw"
        
        msgbox = tk.messagebox.askquestion(title="Game Over", message=end_message+". Would you like to play again?")
        if (msgbox == 'yes'):
            self.new_game(window)
            
        return msgbox
    
    
    

root = tk.Tk()
app = App(root)
app.mainloop()