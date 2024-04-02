import customtkinter as ctk
from PIL import Image, ImageTk
import random

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")


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
        self.current_player = "ai" if self.current_player == "human" else "human"

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


class Application(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.game = Game()
        self.title("Number Game")
        self.configure(bg="#2D2D2D")
        self.resizable(False, False)

        human_image = Image.open("human.png")
        self.human_icon = ctk.CTkImage(light_image=human_image, dark_image=human_image, size=(50, 50))

        ai_image = Image.open("robot.png")
        self.ai_icon = ctk.CTkImage(light_image=ai_image, dark_image=ai_image, size=(50, 50))

        self.create_widgets()

    def create_widgets(self):
        label_options = {"text_color": "white", "bg_color": "#2D2D2D"}
        button_options = {"fg_color": "#5B5B5B", "hover_color": "#3D3D3D", "text_color": "white", "bg_color": "#2D2D2D",
                          "corner_radius": 10}

        # Game Info Frame
        self.game_info_frame = ctk.CTkFrame(self, bg_color="#2D2D2D")
        self.game_info_frame.pack(pady=10, fill="x", padx=10)

        self.current_number_label = ctk.CTkLabel(self.game_info_frame,
                                                 text=f"Current number: {self.game.current_number}", **label_options)
        self.current_number_label.pack(pady=5)

        # Afficher les points du joueur avec icône
        self.player_points_frame = ctk.CTkFrame(self, bg_color="#2D2D2D")
        self.player_points_frame.pack(pady=5, fill="x", padx=10)
        self.player_icon_label = ctk.CTkLabel(self.player_points_frame, text="", image=self.human_icon,
                                              bg_color="#2D2D2D")
        self.player_icon_label.pack(side="left", padx=10)
        self.player_points_label = ctk.CTkLabel(self.player_points_frame,
                                                text=f"Player points: {self.game.player_points}", **label_options)
        self.player_points_label.pack(side="left")

        self.ai_points_frame = ctk.CTkFrame(self, bg_color="#2D2D2D")
        self.ai_points_frame.pack(pady=5, fill="x", padx=10)
        self.ai_icon_label = ctk.CTkLabel(self.ai_points_frame, text="", image=self.ai_icon, bg_color="#2D2D2D")
        self.ai_icon_label.pack(side="left", padx=10)
        self.ai_points_label = ctk.CTkLabel(self.ai_points_frame, text=f"AI points: {self.game.ai_points}",
                                            **label_options)
        self.ai_points_label.pack(side="left")

        self.bank_label = ctk.CTkLabel(self.game_info_frame, text=f"Bank: {self.game.bank}", **label_options)
        self.bank_label.pack(pady=5)

        # Actions Frame
        self.actions_frame = ctk.CTkFrame(self, bg_color="#2D2D2D")
        self.actions_frame.pack(pady=20, fill="x", padx=10)

        self.divide_by_2_button = ctk.CTkButton(self.actions_frame, text="Divide by 2", command=self.divide_by_2,
                                                **button_options)
        self.divide_by_2_button.pack(side="left", padx=10)

        self.divide_by_3_button = ctk.CTkButton(self.actions_frame, text="Divide by 3", command=self.divide_by_3,
                                                **button_options)
        self.divide_by_3_button.pack(side="left", padx=10)

        self.ai_move_button = ctk.CTkButton(self.actions_frame, text="AI move", command=self.ai_move, **button_options)
        self.ai_move_button.pack(side="left", padx=10)

        self.play_again_btn = ctk.CTkButton(self.actions_frame, text="Play again", command=self.play_again,
                                            state="disabled", **button_options)
        self.play_again_btn.pack(side="left", padx=10)

        # Status Frame
        self.status_frame = ctk.CTkFrame(self, bg_color="#2D2D2D")
        self.status_frame.pack(pady=10, fill="x", padx=10)

        self.winner_label = ctk.CTkLabel(self.status_frame, text="", **label_options)
        self.winner_label.pack(pady=5)

    def divide_by_2(self):
        self.game.divide_by(2)
        self.update_labels()

    def divide_by_3(self):
        self.game.divide_by(3)
        self.update_labels()

    def ai_move(self):
        self.game.ai_move()
        self.update_labels()

    def play_again(self):
        self.game = Game()
        self.update_labels()
        self.play_again_btn.configure(state=ctk.DISABLED)

    def update_labels(self):
        self.current_number_label.configure(text=f"Current number: {self.game.current_number}")
        self.player_points_label.configure(text=f"Player points: {self.game.player_points}")
        self.ai_points_label.configure(text=f"AI points: {self.game.ai_points}")
        self.bank_label.configure(text=f"Bank: {self.game.bank}")
        if self.game.winner:
            self.winner_label.configure(text=f"Winner: {self.game.winner}")
            self.play_again_btn.configure(state=ctk.NORMAL)
        else:
            self.winner_label.configure(text="")
            self.play_again_btn.configure(
                state=ctk.DISABLED)


if __name__ == "__main__":
    app = Application()
    app.mainloop()
