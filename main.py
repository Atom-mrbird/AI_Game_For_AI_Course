import tkinter as tk
import random

class Game:
    def __init__(self, master):
        self.master = master
        self.master.title("Number Game")
        self.master.geometry("300x200")
        self.bank = 0
        self.player_points = 0
        self.opponent_points = 0
        self.current_number = 0
        self.game_over = False
        self.create_widgets()

    def create_widgets(self):
        self.start_label = tk.Label(self.master, text="Choose a number to start the game:")
        self.start_label.pack()

        self.start_button = tk.Button(self.master, text="Start", command=self.start_game)
        self.start_button.pack()

        self.number_label = tk.Label(self.master, text="")
        self.number_label.pack()

        self.divide_by_2_button = tk.Button(self.master, text="Divide by 2", command=lambda: self.divide_number(2))
        self.divide_by_2_button.pack()

        self.divide_by_3_button = tk.Button(self.master, text="Divide by 3", command=lambda: self.divide_number(3))
        self.divide_by_3_button.pack()

        self.result_label = tk.Label(self.master, text="")
        self.result_label.pack()

    def start_game(self):
        self.game_over = False
        self.bank = 0
        self.player_points = 0
        self.opponent_points = 0
        self.current_number = random.choice([n for n in range(10000, 20001) if n % 2 == 0 and n % 3 == 0])
        self.number_label.config(text=f"Current number: {self.current_number}")
        self.start_button.config(state="disabled")

    def divide_number(self, divisor):
        if self.game_over:
            return
        if self.current_number % divisor == 0:
            self.current_number //= divisor
            if divisor == 2:
                self.opponent_points += 2
            else:
                self.player_points += 3
            if self.current_number % 10 == 0:
                self.bank += 1
            self.number_label.config(text=f"Current number: {self.current_number}")
            self.result_label.config(text=f"Your points: {self.player_points}, Opponent's points: {self.opponent_points}, Bank points: {self.bank}")
            if self.current_number <= 10:
                self.game_over = True
                self.opponent_points += self.bank
                self.result_label.config(text=f"Game over! Your points: {self.player_points}, Opponent's points: {self.opponent_points}")
                self.start_button.config(state="normal")

root = tk.Tk()
game = Game(root)
root.mainloop()