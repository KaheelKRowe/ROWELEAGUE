# 🏀 Basketball General Manager Simulation (ROWELEAGUE)

A Python-based basketball general manager simulation game that models league operations, player development, team management, and season progression.

---

## 🚀 Overview

This project is a command-line simulation engine where users take control of a basketball team and manage all aspects of a franchise, including roster decisions, drafting, and free agency.

The system simulates a full league environment with AI-controlled teams, player progression, and a structured season lifecycle.

---

## 🎮 Features

### 🧠 Game Simulation

* Probabilistic game outcomes based on team overall ratings
* Full season simulation with 60-game schedules
* Conference and division-based standings

### 🧑‍💼 Team Management

* 15-player roster limit
* Salary cap system with payroll and cap tracking
* Sign and release players
* Free agency system with user and CPU interaction

### 🧬 Player System

* Randomly generated players with:

  * Position-based attributes
  * Weighted overall rating system
  * Potential grading (S–D tiers)
* Career progression and regression system
* Aging system with retirement logic

### 📅 League Lifecycle

* Calendar-based phase system:

  * Regular Season
  * Trade Deadline
  * Playoffs
  * Draft
  * Free Agency
* Automated season transitions

### 🎯 Draft System

* Lottery-based draft order for top picks
* Multi-round draft (48 picks)
* AI drafting logic based on team needs
* User-controlled draft selections

### 🤖 AI Teams

* CPU teams:

  * Evaluate positional needs
  * Sign free agents strategically
  * Draft players based on roster weaknesses
  * Upgrade rosters dynamically

---

## 🏗️ Project Structure

```bash
RLleague.py     # Core simulation engine
RLteam.py       # Team logic (rosters, salary cap)
RLplayer.py     # Player generation and development
RLcalendar.py   # Season phases and date system
RLdraft.py      # Draft logic and AI drafting
RLui.py         # Command-line interface
RLdata.py       # Data (teams, names, positions)
RLmenu.py       # Entry point/game launcher
RLplayoffs.py   # League Playoffs
RLtrades.py     # League trading system
```

---

## 🛠️ Technologies Used

* Python
* Object-Oriented Programming (OOP)
* Randomized simulation/probability systems
* CLI (Command-Line Interface)

---

## ▶️ How to Run

1. Clone the repository:

```bash
git clone https://github.com/KaheelKRowe/ROWELEAGUE.git
```

2. Navigate to the project folder:

```bash
cd ROWELEAGUE
```

3. Run the game:

```bash
python RLmenu.py
```

---

## 🧠 Future Improvements

* Player statistics and box scores
* Trade system
* Save/load game functionality
* Improved UI (GUI or web-based interface)
* More advanced AI decision-making
* Convert the project into a web-based application using Streamlit or Flask once the terminal version is fully complete

---

## 📌 Notes

This project was built to practice:

* Object-oriented programming
* System design and architecture
* Simulation logic and state management

---

## 👤 Author

**Kaheel Rowe**
GitHub: https://github.com/KaheelKRowe

---

⭐ If you found this project interesting, feel free to star the repo!
