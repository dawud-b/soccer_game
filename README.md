# ⚽ Terminal Soccer

A real-time, two-player soccer game playable directly in your terminal. Built with Python sockets for a head-to-head multiplayer experience.

---

## ✨ Features

- **Single Player Mode** - Single player mode to play against an AI. No need to input an IP address!
- **Multiplayer Gameplay** – Connect with a friend over a local network to compete in real-time.
- **Live Field Visualization** – ASCII-based field updates after every move to show player positions and ball location.
- **Simple Controls** – Input numbers (1–6) to pass, shoot, or defend.
- **Penalty System** – Consequences for invalid actions.
- **Game Reset** – Restart seamlessly after a match without restarting the server.

---

## Getting Started

### ✅ Requirements

- ***Python 3.10 or newer*** installed on both machines
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

## How to Play

### Single Player Setup

1. In Terminal run:
   ```bash
   python3 Client.py
   ```
   Make sure you are in the same directory that you download Client.py

2. Select solo mode by pressing '1' then Enter.

3. Start playing against the AI!

### Multiplayer Setup

1. **Start the Server**  
   In Terminal 1:
   ```bash
   python3 Server.py
   # Enter your IP
   ```

2. **Start Player 1 Client**  
   In Terminal 2:
   ```bash
   python3 Client.py
   # Input '2' to select multiplayer mode.
   # Enter the same IP as the server
   ```

3. **Start Player 2 Client**  
   In Terminal 3:
   ```bash
   python3 Client.py
   # Input '2' to select multiplayer mode.
   # Enter the same IP as the server
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

### ❗ Rules

- **Objective:** Score 5 goals before your opponent does.
- **Passing in the Shooting Phase** → Penalty! Possession switches, ball resets to your goal line.
- **Shooting in the Passing Phase** → Penalty! Possession switches, ball resets to your goal line.
- Player 1 always starts with ball ownership.
- Player that was scored on gets ball next.
- Player with possession inputs their move first.

---

### 🔄 Restarting

After a game ends:
- Type `reset_game` to restart
- Or type `exit` to quit

---

## 👨‍💼 Authors

- **Dawud Benedict** – Game Logic & Field Visualization
- **Gurumanie Singh** – Multiplayer Networking & Client file  
