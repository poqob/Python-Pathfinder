# 🤖 Roomba Pathfinding AI Simulator

This project is a comprehensive **Autonomous Pathfinding** simulation developed using Python and Pygame. It visualizes popular algorithms like **A\***, **RRT**, and **RRT\***, simulating a robot (Roomba) navigating a static map to reach a target.

## 🌟 Features

* **Multi-Algorithm Support:** Switch between A\* (A-Star), RRT, and RRT\* algorithms.
* **Image Processing-Based Map:** Automatically converts any black-and-white image (`map.png`) into an obstacle matrix.
* **Built-in Map Editor:** Create and save custom maps with an integrated tool.
* **History System:** Saves drawn paths in JSON format and allows replaying them via a visual interface.
* **Dynamic UI:** Side panel menu for browsing past routes and viewing details.

## 🚀 Installation

Requires Python 3.x and necessary libraries.

1. **Clone the Repository:**
    ```bash
    git clone https://github.com/poqob/roomba-pathfinder.git
    cd roomba-pathfinder
    ```

2. **Install Requirements:**
    ```bash
    pip install -r requirements.txt
    ```

3. **Run the Application:**
    ```bash
    python main.py
    ```

## 🎮 Usage and Controls

The simulation starts with A\* algorithm selected.

| Key | Action | Description |
| :--- | :--- | :--- |
| **Left Click** | Set Target | Selects target point and calculates path. |
| **1** | A\* Mode | Switches to A\* algorithm (grid-based, shortest path). |
| **2** | RRT Mode | Switches to RRT algorithm (random tree, fast exploration). |
| **3** | RRT\* Mode | Switches to RRT\* algorithm (optimized tree). |
| **H** | History Panel | Toggles history panel. |
| **Left/Right Arrow**| Navigation | Browse history records (when history mode is active). |

## 🧠 Algorithms

### 1. A\* (A-Star) Algorithm
Grid-based, guarantees shortest path from start to target. Moves cell-by-cell, drawing optimal path around obstacles.

![A\* Algorithm](https://github.com/poqob/Python-Pathfinder/raw/main/presentation/a_star.png)

### 2. RRT (Rapidly-exploring Random Tree)
Sampling-based, builds a tree by selecting random points. Finds a path but it's often zigzagged and doesn't guarantee shortest path. Fast in large spaces.

![RRT Algorithm](https://github.com/poqob/Python-Pathfinder/raw/main/presentation/rtt.png)

### 3. RRT\* (RRT Star)
Optimized version of RRT. New nodes check neighbors for possible rewiring, smoothing the path over time.

![RRT\* Algorithm](https://github.com/poqob/Python-Pathfinder/raw/main/presentation/rrt_star.png)

## 🛠 Tools

### 🗺️ Map Editor
Run `map_creator.py` to create custom maps.
* **Left Click:** Draw walls.
* **Right Click:** Erase.
* **Save:** Saves as `assets/map.png`.

![Map Editor](https://github.com/poqob/Python-Pathfinder/raw/main/presentation/map_create.png)

### 📜 History and Log System
Each successful path calculation is saved in `history.json`. Press **'H'** to open the side panel and view past attempts, algorithms used, and timestamps.

![History Panel](https://github.com/poqob/Python-Pathfinder/raw/main/presentation/history.png)

## 📂 Project Structure

```text
../
├── assets/                 # Visual assets and maps
│   ├── map.png
│   ├── roomba.png
│   └── ...
├── src/                    # Source code
│   ├── history_manager.py  # JSON read/write operations
│   ├── pathfinder_manager.py # Algorithm management
│   ├── romba_sprite.py     # Robot movement physics
│   ├── rrt_algorithms.py   # RRT and RRT\* implementation
│   ├── ui_manager.py       # UI drawing
│   └── utils.py            # Image processing tools
├── presentation/           # README screenshots
│   ├── demo.gif
│   ├── astar_demo.png
│   ├── rrt_demo.png
│   └── ...
├── history.json            # Log file
├── main.py                 # Main execution file
├── map_creator.py          # Map creator tool
└── requirements.txt        # Library requirements