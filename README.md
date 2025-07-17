# ⚽ Terminal Soccer Showdown

A real-time, two-player soccer game playable directly in your terminal. Built with Python sockets for a classic head-to-head multiplayer experience.

---

## ✨ Features

- **Multiplayer Gameplay** – Connect with a friend over a local network to compete in real-time.
- **Live Field Visualization** – ASCII-based field updates after every move to show player positions and ball location.
- **Simple Controls** – Input numbers (1–6) to pass, shoot, or defend.
- **Penalty System** – Strategic depth with consequences for invalid actions.
- **Game Reset** – Restart seamlessly after a match without restarting the server.

---

## 🚀 Getting Started

### ✅ Requirements

- Python 3.x installed on both machines
- Local or network connection between players

### 📦 Installation

1. **Clone the Repository**  
   ```bash
   git clone https://github.com/your-username/soccer-terminal-game.git
   cd soccer-terminal-game
   ```

2. **(Optional) Create a Virtual Environment**  
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

---

## 🌹 How to Play

### 🎯 Objective

Score 5 goals before your opponent does.

### 👣 Game Flow

1. **Start the Server**  
   In Terminal 1:
   ```bash
   python3 Server.py
   ```

2. **Start Player 1 Client**  
   In Terminal 2:
   ```bash
   python3 Client.py
   ```

3. **Start Player 2 Client**  
   In Terminal 3:
   ```bash
   python3 Client.py
   ```

> The game will begin automatically once both players are connected.

---

### 🎮 Controls

| Action       | Valid Inputs | Description                                                                 |
|--------------|--------------|-----------------------------------------------------------------------------|
| **Pass**     | 1, 2, 3      | Moves the ball toward the opponent's goal. Risk of interception.            |
| **Shoot**    | 4, 5, 6      | Attempt to score when you're at the goal line.                             |
| **Defend**   | 1–6          | Predict your opponent's move to regain possession.                         |

---

### ❗ Penalty Rules

- **Passing in the Shooting Phase** → Penalty! Possession switches, ball resets to your goal line.
- **Shooting in the Passing Phase** → Penalty! Possession switches, ball resets to your goal line.

---

### 🔄 Restarting

After a game ends:
- Type `reset_game` to restart
- Or type `exit` to quit

---

## 👨‍💼 Authors

- **Gurumanie Singh** – Multiplayer Networking & Client View  
- **Dawud Benedict** – Game Logic & Field Visualization
