# A\* Pathfinding Visualizer

This project implements an interactive visualizer for the A\* (A-star) pathfinding algorithm using Python and Pygame. It allows users to construct obstacle maps in real time, visualize the search process, and observe the optimal path calculated between two nodes on a grid.

![](https://github.com/YohannPardes/A-star-pathfinding-algorythm/blob/master/GIF.gif)
---

## 🔍 Features

* **Interactive Grid-Based Interface**
  Click to toggle walls (obstacles) on a 2D grid.

* **Real-Time Visualization**
  Watch the A\* algorithm in action as it expands nodes and finds the optimal path.

* **Diagonal Movement Support**
  Supports both cardinal (up, down, left, right) and diagonal movement with distinct movement costs.

* **Color-Coded Feedback**

  * 🟩 Green: Visited nodes (explored)
  * 🟨 Yellow: Final shortest path
  * ⬛ Black: Obstacles/walls
  * ⚪ Light gray: Unvisited grid cells

---

## 📌 How to Use

### 🖥 Controls

| Action                    | Description                         |
| ------------------------- | ----------------------------------- |
| `Mouse Left Click`        | Toggle walls (click any cell)       |
| `SPACE` (keyboard)        | Start the A\* pathfinding algorithm |
| `Window Close` (X button) | Exit the application                |

---

## 🚀 Getting Started

### Prerequisites

Make sure you have **Python 3.7+** installed. You also need the `pygame` library.

### Installation

```bash
git clone https://github.com/yourusername/a-star-pathfinding-visualizer.git
cd a-star-pathfinding-visualizer
pip install pygame
python main.py
```
