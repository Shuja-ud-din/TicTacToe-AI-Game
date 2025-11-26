import csv
import numpy as np

def move_to_index(move):
    row, col = map(int, move.split('-'))
    return row * 3 + col

def process_game(moves):
    board = [0] * 9
    samples = []
    for i, move in enumerate(moves):
        if move == '---' or move.strip() == '':
            break
        idx = move_to_index(move)
        player = 1 if i % 2 == 0 else -1  # X starts first (even indices)
        if player == 1:
            board_input = board.copy()
            samples.append((board_input, idx))
        board[idx] = player
    return samples

X_data = []
y_data = []

with open('tictactoe_games.csv', 'r') as f:
    reader = csv.reader(f)
    next(reader)  # skip header
    for row in reader:
        winner = row[0]
        if winner != 'X':  # Optional: only use games where X wins
            continue
        moves = row[1:]
        samples = process_game(moves)
        for board, move in samples:
            X_data.append(board)
            y_data.append(move)

# Convert to numpy arrays
X_np = np.array(X_data, dtype=np.int8)
y_np = np.array(y_data, dtype=np.int8)

# Save for training
np.save('X.npy', X_np)
np.save('y.npy', y_np)

print(f"Saved {len(X_np)} training samples.")
