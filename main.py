import customtkinter as ctk
import random
import tkinter as tk
from typing import Optional

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")


class Node:
    def __init__(self, current_player, number, humain_points, ai_points, bank, dady, child_div2=None, child_div3=None):
        self.current_player = current_player
        self.number = number
        self.humain_points = humain_points
        self.ai_points = ai_points
        self.bank = bank
        self.child_div2 = child_div2
        self.child_div3 = child_div3
        self.dady = dady


class GameTree:
    def _init__(self, RootNode):
        self.RootNode = RootNode
        self.starter = ""

    def display_game_tree(self, node, divisor, level=0):
        if node is None:
            return

        print(
            "|" * level + f"div : {divisor}, Nœud: {node.number}, Joueur: {node.current_player}, Points Humain: {node.humain_points}, Points IA: {node.ai_points}, Banque: {node.bank}, heuristic : {heuristic_function(node)}")

        if node.child_div2 is not None:
            self.display_game_tree(node.child_div2, 2, level + 1)
        if node.child_div3 is not None:
            self.display_game_tree(node.child_div3, 3, level + 1, )

    def build_gameTree(self, node: Node, level=3, dady=0):
        if level == 0:
            return None
        else:
            if node.number % 2 != 0 and node.number % 3 != 0:
                if (dady == 2):
                    node.child_div2 = None
                elif (dady == 3):
                    node.child_div3 = None
            else:
                node_div2 = None
                node_div3 = None
                if (node.number % 2 == 0):
                    num = node.number / 2
                    if (num <= 10):
                        if (node.current_player == "human"):
                            node_div2 = Node("ai", num,
                                             node.humain_points + (2 if node.current_player == "human" else 0),
                                             node.ai_points + (2 if node.current_player == "ai" else 0) + node.bank, 0,
                                             2, None, None)
                        else:
                            node_div2 = Node("human", num, node.humain_points + (
                                2 if node.current_player == "human" else 0) + node.bank,
                                             node.ai_points + (2 if node.current_player == "ai" else 0), 0, 2, None,
                                             None)
                    else:
                        node_div2 = Node("ai" if node.current_player == "human" else "human", num,
                                         node.humain_points + (2 if node.current_player == "human" else 0),
                                         node.ai_points + (2 if node.current_player == "ai" else 0),
                                         node.bank + 1 if str(node.number).endswith(('0', '5')) else 0, 2)
                        self.build_gameTree(node_div2, level - 1, 2)
                    node.child_div2 = node_div2
                if (node.number % 3 == 0):
                    num = node.number / 3
                    if (num <= 10):
                        if (node.current_player == "human"):
                            node_div3 = Node("ai", num, node.humain_points + (3 if node.current_player == "ai" else 0),
                                             node.ai_points + node.bank + (3 if node.current_player == "human" else 0),
                                             0, 3, None, None)
                        else:
                            node_div3 = Node("human", num,
                                             node.humain_points + (3 if node.current_player == "ai" else 0) + node.bank,
                                             node.ai_points + (3 if node.current_player == "human" else 0), 0, 3, None,
                                             None)
                    else:
                        node_div3 = Node("ai" if node.current_player == "human" else "human", num,
                                         node.humain_points + (3 if node.current_player == "ai" else 0),
                                         node.ai_points + (3 if node.current_player == "human" else 0),
                                         node.bank + 1 if str(node.number).endswith(('0', '5')) else 0, 3)
                        self.build_gameTree(node_div3, level - 1, 3)
                    node.child_div3 = node_div3


def heuristic_function(node: Node):
    if node.number % 3 == 0 and node.dady == 3:
        if node.current_player == "ai":
            return 3 + node.ai_points - node.humain_points
        else:
            return node.ai_points - (node.humain_points + 3)
    if node.number % 2 == 0 and node.dady == 2:
        if node.current_player == "human":
            return 2 + node.ai_points - node.humain_points
        else:
            return node.ai_points - (node.humain_points + 2)
    if node.number <= 10:
        if node.current_player == "human":
            return (node.ai_points + node.bank) - node.humain_points
        else:
            return node.ai_points - (node.humain_points + node.bank)
    return node.ai_points - node.humain_points


def min_max(node, depth, maximizing_player):
    if depth == 0 or node.child_div2 is None and node.child_div3 is None:
        return (heuristic_function(node), node)

    if maximizing_player:
        max_eval = float('-inf')
        best_node = None
        for child in [node.child_div2, node.child_div3]:
            if child is not None:
                (eval, _) = min_max(child, depth - 1, False)
                if (eval > max_eval):
                    max_eval = eval
                    best_node = child
        return (max_eval, best_node)
    else:
        min_eval = float('inf')
        best_node = None
        for child in [node.child_div2, node.child_div3]:
            if child is not None:
                (eval, _) = min_max(child, depth - 1, True)
                if (eval < min_eval):
                    min_eval = eval
                    best_node = child
        return (min_eval, best_node)


def alpha_beta_search(node, depth, alpha, beta, maximizing_player):
    if depth == 0 or (node.child_div2 is None and node.child_div3 is None):
        return (heuristic_function(node), node)

    best_node = None

    if maximizing_player:
        value = float('-inf')
        for child in [node.child_div2, node.child_div3]:
            if child is not None:
                eval, child_node = alpha_beta_search(child, depth - 1, alpha, beta, False)
                if eval > value:
                    value = eval
                    best_node = child_node
                alpha = max(alpha, value)
                if beta <= alpha:
                    break  # Beta cut-off
        return (value, best_node)
    else:
        value = float('inf')
        for child in [node.child_div2, node.child_div3]:
            if child is not None:
                eval, child_node = alpha_beta_search(child, depth - 1, alpha, beta, True)
                if eval < value:
                    value = eval
                    best_node = child_node
                beta = min(beta, value)
                if beta <= alpha:
                    break
        return (value, best_node)

class Game:
    def __init__(self):
        self.numbers = [n for n in range(10002, 20001, 6) if n % 6 == 0]
        self.current_number = None
        random.shuffle(self.numbers)
        self.numbers = self.numbers[:5]
        self.winner = None
        self.gameTree = GameTree()
        self.currentNode: Optional[Node] = None
        self.algo = ""

    def reset_game(self):
        random.shuffle(self.numbers)
        self.current_number = None
        self.winner = None
        self.gameTree = GameTree()
        self.currentNode = None

    def choose_number(self, number):
        if number in self.numbers:
            self.current_number = number

    def divide_by(self, divisor):
        if (divisor == 2 and self.currentNode.child_div2 != None):
            self.currentNode = self.currentNode.child_div2
            self.gameTree.build_gameTree(self.currentNode, 5, 2)

        elif (divisor == 3 and self.currentNode.child_div3 != None):
            self.currentNode = self.currentNode.child_div3
            self.gameTree.build_gameTree(self.currentNode, 5, 3)
        print(self.currentNode.child_div2, self.currentNode.child_div3)


class Application(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Number Division Game")
        self.geometry("400x300")
        self.game = Game()
        self.create_widgets()
        self.update_labels()

    def choose_algo(self, number):
        if hasattr(self, 'start_frame') and self.start_frame.winfo_exists():
            self.start_frame.destroy()

        self.algo_frame = ctk.CTkFrame(self)
        self.algo_frame.pack(pady=20)

        algo_label = ctk.CTkLabel(self.algo_frame, text="Which algo?")
        algo_label.pack()

        min_max_button = ctk.CTkButton(self.algo_frame, text="Min-Max",
                                       command=lambda: self.associate_algo("min-max", number))
        min_max_button.pack(side=tk.LEFT, padx=10)

        alpha_beta_button = ctk.CTkButton(self.algo_frame, text="Alpha Beta",
                                          command=lambda: self.associate_algo("alpha-beta", number))
        alpha_beta_button.pack(side=tk.RIGHT, padx=10)

    def associate_algo(self, algo, number):
        self.algo = algo
        self.algo_frame.destroy()
        self.choose_starter(number)

    def choose_starter(self, number):
        self.starter_frame = ctk.CTkFrame(self)
        self.starter_frame.pack(pady=20)

        starter_label = ctk.CTkLabel(self.starter_frame, text="Who starts?")
        starter_label.pack()

        human_button = ctk.CTkButton(self.starter_frame, text="Human", command=lambda: self.start_game(number, "human"))
        human_button.pack(side=tk.LEFT, padx=10)

        ai_button = ctk.CTkButton(self.starter_frame, text="AI", command=lambda: self.start_game(number, "ai"))
        ai_button.pack(side=tk.RIGHT, padx=10)

    def create_widgets(self):
        self.start_frame = ctk.CTkFrame(self)
        self.start_frame.pack(pady=20)

        self.numbers_label = ctk.CTkLabel(self.start_frame, text="Choose a starting number:")
        self.numbers_label.pack()

        self.numbers_buttons = []
        for number in self.game.numbers:
            btn = ctk.CTkButton(self.start_frame, text=str(number),
                                command=lambda n=number: self.choose_algo(n))
            btn.pack(pady=2)
            self.numbers_buttons.append(btn)

    def update_log(self, message):
        self.log_text.configure(state='normal')
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.configure(state='disabled')
        self.log_text.see(tk.END)

    def start_game(self, number, starter):
        self.starter_frame.pack_forget()
        self.game.choose_number(number)
        for btn in self.numbers_buttons:
            btn.pack_forget()
        self.numbers_label.pack_forget()
        self.play_frame = ctk.CTkFrame(self)
        self.play_frame.pack(pady=20)

        self.current_number_label = ctk.CTkLabel(self.play_frame, text="")
        self.current_number_label.pack()

        self.player_points_label = ctk.CTkLabel(self.play_frame, text="")
        self.player_points_label.pack()

        self.ai_points_label = ctk.CTkLabel(self.play_frame, text="")
        self.ai_points_label.pack()

        self.bank_label = ctk.CTkLabel(self.play_frame, text="")
        self.bank_label.pack()

        self.divide_by_2_button = ctk.CTkButton(self.play_frame, text="Divide by 2", command=lambda: self.divide_by(2))
        self.divide_by_2_button.pack(side=tk.LEFT, padx=10)

        self.divide_by_3_button = ctk.CTkButton(self.play_frame, text="Divide by 3", command=lambda: self.divide_by(3))
        self.divide_by_3_button.pack(side=tk.RIGHT, padx=10)

        self.log_frame = ctk.CTkFrame(self)
        self.log_frame.pack(pady=20, fill='both', expand=True)

        self.log_text = ctk.CTkTextbox(self.log_frame, height=10,
                                       state='disabled')  # state='disabled' pour empêcher l'édition
        self.log_text.pack(side=tk.LEFT, fill='both', expand=True)

        self.log_scroll = tk.Scrollbar(self.log_frame, command=self.log_text.yview)
        self.log_scroll.pack(side=tk.RIGHT, fill='y')

        self.log_text.configure(yscrollcommand=self.log_scroll.set)
        self.game.gameTree.RootNode = Node("human" if starter == "ai" else "ai", number, 0, 0, 0, 0, None, None)
        self.game.gameTree.starter = starter
        self.game.gameTree.build_gameTree(self.game.gameTree.RootNode, 2)

        self.game.gameTree.display_game_tree(self.game.gameTree.RootNode, 0)
        self.game.currentNode = self.game.gameTree.RootNode
        self.update_log(f"AI use : {self.algo}")
        self.update_log(f"Start Player : {starter.upper()}")

        if (self.game.currentNode.current_player == "human"):
            print("AI play")
            (_, node_b) = min_max(self.game.currentNode, 4, True)
            if (node_b == None):
                print("AI tombe sur un None")
            self.divide_by(2 if node_b == self.game.currentNode.child_div2 else 3)

        self.update_labels()

    def update_labels(self):
        if self.game.currentNode is not None:
            self.current_number_label.configure(text=f"Current Number: {self.game.currentNode.number}")
            self.player_points_label.configure(text=f"Player Points: {self.game.currentNode.humain_points}")
            self.ai_points_label.configure(text=f"AI Points: {self.game.currentNode.ai_points}")
            self.bank_label.configure(text=f"Bank: {self.game.currentNode.ai_points}")

    def open_popup(self):
        self.popup = ctk.CTkToplevel(self)
        self.popup.title("Game Result")

        player_label = ctk.CTkLabel(self.popup, text=f"Player Score: {self.game.currentNode.humain_points}")
        player_label.pack()

        ai_label = ctk.CTkLabel(self.popup, text=f"AI Score: {self.game.currentNode.ai_points}")
        ai_label.pack()

        bank_label = ctk.CTkLabel(self.popup, text=f"Bank : {self.game.currentNode.bank}")
        bank_label.pack()

        self.close_button = ctk.CTkButton(self.popup, text="Play Again", command=self.reset_and_play_again)
        self.close_button.pack(pady=20)

        self.popup.grab_set()
        self.popup.wait_window()

    def reset_and_play_again(self):
        if self.popup:
            self.popup.destroy()
            self.popup = None

        self.game.reset_game()

        if hasattr(self, 'play_frame') and self.play_frame.winfo_exists():
            self.play_frame.destroy()

        if hasattr(self, 'log_frame') and self.log_frame.winfo_exists():
            self.log_frame.destroy()

        self.create_widgets()
        self.update_labels()

    def divide_by(self, divisor):
        node = self.game.currentNode
        self.game.divide_by(divisor)
        if (node != self.game.currentNode):
            if divisor == 2:
                self.update_log(f"{self.game.currentNode.current_player.upper()} play : div 2")
            else:
                self.update_log(f"{self.game.currentNode.current_player.upper()} play : div 3")
            if (self.game.currentNode.child_div2 == None and self.game.currentNode.child_div3 == None):
                self.update_labels()
                self.open_popup()
            elif (self.game.currentNode.current_player == "human"):
                print("AI play")
                if self.algo == "min-max":
                    (_, node_b) = min_max(self.game.currentNode, 4, True)
                else:
                    (_, node_b) = alpha_beta_search(self.game.currentNode, 4, float('-inf'), float('inf'), True)
                if (node_b == None):
                    print("AI tombe sur un None")
                self.divide_by(2 if node_b == self.game.currentNode.child_div2 else 3)

        self.update_labels()


if __name__ == "__main__":
    app = Application()
    app.mainloop()