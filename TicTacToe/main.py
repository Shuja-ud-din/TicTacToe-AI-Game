import tkinter as tk
import torch
import torch.nn as nn

class TicTacToeNet(nn.Module):
    def __init__(self):
        super().__init__()
        self.model = nn.Sequential(
            nn.Linear(9, 128),
            nn.ReLU(),
            nn.Linear(128, 64),
            nn.ReLU(),
            nn.Linear(64, 9)
        )

    def forward(self, x):
        return self.model(x)

# Load the trained model
model = TicTacToeNet()
model.load_state_dict(torch.load("tictactoe_model.pth"))
model.eval()

# Game logic class
class TicTacToeGame:
    def __init__(self, root):
        self.root = root
        self.board = [0] * 9  # 0: empty, 1: user (X), -1: bot (O)
        self.buttons = []
        self.is_user_turn = True
        self.game_over = False

        self.create_widgets()

    def create_widgets(self):
        # Create buttons
        for i in range(9):
            btn = tk.Button(self.root, text=" ", width=10, height=3,
                            font=("Arial", 20), command=lambda i=i: self.user_move(i))
            btn.grid(row=i // 3, column=i % 3)
            self.buttons.append(btn)

        # Label for results
        self.result_label = tk.Label(self.root, text="", font=("Arial", 18))
        self.result_label.grid(row=3, column=0, columnspan=3)

        # Restart button
        self.restart_button = tk.Button(self.root, text="Restart", font=("Arial", 14),
                                        command=self.restart_game, bg="lightgray")
        self.restart_button.grid(row=4, column=0, columnspan=3, pady=10)

    def user_move(self, index):
        if self.board[index] == 0 and self.is_user_turn and not self.game_over:
            self.board[index] = 1
            self.buttons[index].config(text="X", state="disabled")
            if self.check_winner(1):
                self.show_result("You Win!")
                return
            if self.is_draw():
                self.show_result("It's a Draw!")
                return
            self.is_user_turn = False
            self.root.after(300, self.bot_move)  # Small delay for better UX

    def bot_move(self):
        if self.game_over:
            return

        # Try blocking user win first
        move = self.block_user_win()
        if move is None:
            move = self.make_bot_move()

        if self.board[move] == 0:
            self.board[move] = -1
            self.buttons[move].config(text="O", state="disabled")

        if self.check_winner(-1):
            self.show_result("Bot Wins!")
        elif self.is_draw():
            self.show_result("It's a Draw!")
        else:
            self.is_user_turn = True

    def check_winner(self, player):
        win_conditions = [
            [0,1,2], [3,4,5], [6,7,8],   # Rows
            [0,3,6], [1,4,7], [2,5,8],   # Columns
            [0,4,8], [2,4,6]             # Diagonals
        ]
        for combo in win_conditions:
            if all(self.board[i] == player for i in combo):
                return True
        return False

    def is_draw(self):
        return all(cell != 0 for cell in self.board)

    def show_result(self, message):
        self.result_label.config(text=message)
        self.game_over = True
        for btn in self.buttons:
            btn.config(state="disabled")

    def make_bot_move(self):
        input_tensor = torch.tensor([self.board], dtype=torch.float32)
        with torch.no_grad():
            output = model(input_tensor)
            sorted_indices = torch.argsort(output, descending=True)

        for idx in sorted_indices[0]:
            move = idx.item()
            if self.board[move] == 0:
                return move

        return 0  # Fallback

    def block_user_win(self):
        for i in range(9):
            if self.board[i] == 0:
                self.board[i] = 1
                if self.check_winner(1):
                    self.board[i] = 0
                    return i
                self.board[i] = 0
        return None

    def restart_game(self):
        self.board = [0] * 9
        self.is_user_turn = True
        self.game_over = False
        self.result_label.config(text="")
        for btn in self.buttons:
            btn.config(text=" ", state="normal")


# Launch the GUI
root = tk.Tk()
root.title("Tic-Tac-Toe")
game = TicTacToeGame(root)
root.mainloop()
