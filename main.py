import tkinter as tk
import random

class Game:
    def __init__(self):
        self.numbers = [n for n in random.sample(range(10000, 20001), 5) if n % 2 and n % 3]
        self.bank = 0
        self.current_number = self.numbers[0]
        self.player_points = 0
        self.ai_points = 0
        self.current_player = "human"
        self.winner = None

    def divide_by(self, divisor):
        if divisor == 2:
            self.opponent_scores()
        elif divisor == 3:
            self.scores()
        new_number = self.current_number // divisor
        if new_number % 10 in (0, 5):
            self.bank += 1
        self.current_number = new_number
        if new_number <= 10:
            self.game_over()

    def scores(self):
        if self.current_player == "human":
            self.player_points += 3
        else:
            self.ai_points += 3

    def opponent_scores(self):
        if self.current_player == "human":
            self.ai_points += 2
        else:
            self.player_points += 2

    def game_over(self):
        self.winner = "human" if self.player_points > self.ai_points else "ai"
        self.current_player = "human"
        self.bank += self.current_number
        self.current_number = 0

    def switch_player(self):
        if self.current_player == "human":
            self.current_player = "ai"
        else:
            self.current_player = "human"

    def alpha_beta_search(self, state, depth, alpha, beta, maximizing_player):
        if depth == 0 or state.current_number <= 10:
            return state.bank + 5 * state.player_points - 3 * state.ai_points

        if maximizing_player:
            max_eval = -float("inf")
            for action in [2, 3]:
                state.divide_by(action)
                state.switch_player()
                eval = self.alpha_beta_search(state, depth - 1, alpha, beta, False)
                state.switch_player()
                state.current_number = self.current_number
                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return max_eval

        else:
            min_eval = float("inf")
            for action in [2, 3]:
                state.divide_by(action)
                state.switch_player()
                eval = self.alpha_beta_search(state, depth - 1, alpha, beta, True)
                state.switch_player()
                state.current_number = self.current_number
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return min_eval

    def ai_move(self):
        best_eval = -float("inf")
        best_action = 0
        for action in [2, 3]:
            state = Game()
            state.current_number = self.current_number
            state.current_player = "ai"
            state.divide_by(action)
            eval = self.alpha_beta_search(state, 3, best_eval, best_eval, False)
            if eval > best_eval:
                best_eval = eval
                best_action = action
        self.divide_by(best_action)

class Application(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.game = Game()
        self.title("Number Game")
        self.geometry("400x300")
        self.create_widgets()

    def create_widgets(self):
        self.current_number_label = tk.Label(self, text=f"Current number: {self.game.current_number}")
        self.current_number_label.pack()


        self.player_points_label = tk.Label(self, text=f"Player points: {self.game.player_points}")
        self.player_points_label.pack()

        self.ai_points_label = tk.Label(self, text=f"AI points: {self.game.ai_points}")
        self.ai_points_label.pack()

        self.bank_label = tk.Label(self, text=f"Bank: {self.game.bank}")
        self.bank_label.pack()

        self.button_frame = tk.Frame(self)
        self.button_frame.pack()

        self.divide_by_2_button = tk.Button(self.button_frame, text="Divide by 2", command=self.divide_by_2)
        self.divide_by_2_button.grid(row=0, column=0)

        self.divide_by_3_button = tk.Button(self.button_frame, text="Divide by 3", command=self.divide_by_3)
        self.divide_by_3_button.grid(row=0, column=1)

        self.ai_move_button = tk.Button(self.button_frame, text="AI move", command=self.ai_move)
        self.ai_move_button.grid(row=0, column=2)
        self.winner_label = tk.Label(self, text="")
        self.winner_label.pack()

    def divide_by_2(self):
        self.game.divide_by(2)
        self.update_labels()

    def divide_by_3(self):
        self.game.divide_by(3)
        self.update_labels()

    def ai_move(self):
        self.game.ai_move()
        self.update_labels()
        if self.game.winner is None:
            self.game.ai_move()
            self.update_labels()
        else:
            self.winner_label.config(text=f"Winner: {self.game.winner}")

    def update_labels(self):
        self.current_number_label.config(text=f"Current number: {self.game.current_number}")
        self.player_points_label.config(text=f"Player points: {self.game.player_points}")
        self.ai_points_label.config(text=f"AI points: {self.game.ai_points}")
        self.bank_label.config(text=f"Bank: {self.game.bank}")
        if self.game.winner is None:
            self.winner_label.config(text="")
        else:
            self.winner_label.config(text=f"Winner: {self.game.winner}")

if __name__ == "__main__":
    app = Application()
    app.mainloop()