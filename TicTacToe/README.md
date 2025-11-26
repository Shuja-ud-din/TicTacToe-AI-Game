# 🧠 Tic-Tac-Toe AI Game (with PyTorch & Tkinter)

This is a classic Tic-Tac-Toe game where a human player plays against an AI bot. The AI is powered by a trained PyTorch neural network model. The game uses `Tkinter` for a simple and interactive graphical interface.

---

## 📁 Project Structure

```
TicTacToe/
├── main.py                # Main game logic and GUI
├── tictactoe_model.pth    # Pre-trained PyTorch model
├── requirements.txt       # Required Python packages
├── README.md              # Project documentation
```

---

## 🧠 Model Overview

- The model is a **Multilayer Perceptron (MLP)** with:
  - Input: 9 values representing the board
  - Hidden Layers: Two dense layers (128 and 64 neurons)
  - Output: 9 values indicating the model's confidence for each move
- Trained on a dataset of Tic-Tac-Toe board states with ideal next moves.

---

## 🔧 Setup Instructions (using `venv`)

### 1. Download the Project

```bash
cd TicTacToe
```

### 2. Create and Activate Virtual Environment

```bash
python -m venv venv

# On Windows
venv\Scripts\activate

# On macOS/Linux
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Run The Game

```bash
python main.py
```
