import tkinter as tk
import random

class Game:
    def __init__(self, master):
        self.master = master
        self.master.title("Number Game")
        self.bank = 0
        self.player_points = 0
        self.opponent_points = 0
        self.current_number = None
        self.generate_numbers()
        self.create_widgets()

    def generate_numbers(self):
        self.numbers = [i for i in range(10000, 20001) if i % 2 == 0 and i % 3 == 0]
        self.current_number = random.choice(self.numbers)

    def create_widgets(self):
        self.label = tk.Label(self.master, text=f"Current number: {self.current_number}")
        self.label.pack()

        self.divide_by_2_button = tk.Button(self.master, text="Divide by 2", command=self.divide_by_2)
        self.divide_by_2_button.pack()

        self.divide_by_3_button = tk.Button(self.master, text="Divide by 3", command=self.divide_by_3)
        self.divide_by_3_button.pack()

        self.quit_button = tk.Button(self.master, text="Quit", command=self.master.quit)
        self.quit_button.pack()

    def divide_by_2(self):
        if self.current_number % 2 == 0:
            self.opponent_points += 2
            self.current_number //= 2
            self.update_label()
            self.check_game_end()
        else:
            print("Cannot divide by 2")

    def divide_by_3(self):
        if self.current_number % 3 == 0:
            self.player_points += 3
            self.current_number //= 3
            self.update_label()
            self.check_game_end()
        else:
            print("Cannot divide by 3")

    def update_label(self):
        self.label.config(text=f"Current number: {self.current_number}")

    def check_game_end(self):
        if self.current_number <= 10:
            self.player_points += self.bank
            self.bank = 0
            self.end_game()

    def end_game(self):
        if self.player_points > self.opponent_points:
            result = "You win!"
        elif self.player_points < self.opponent_points:
            result = "You lose!"
        else:
            result = "It's a draw!"
        self.label.config(text=f"Game over! {result}")
        self.divide_by_2_button.config(state="disabled")
        self.divide_by_3_button.config(state="disabled")

root = tk.Tk()
game = Game(root)
root.mainloop()