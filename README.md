# Vacuum Simulator Visualization

This project simulates a robot vacuum cleaner's behavior using reinforcement learning, specifically a **Deep Q-Network (DQN)** algorithm. It evaluates and visualizes the agent's performance, showing its ability to clean a room while avoiding obstacles and optimizing its trajectory.

## Overview

- **Simulation**: A robot vacuum navigates a grid-based room to clean dirt, avoid obstacles, and learn the best strategies through reinforcement learning.
- **Machine Learning**: Utilizes the DQN algorithm, a deep reinforcement learning method, to train the vacuum cleaner agent.
- **Visualization**: Real-time rendering of the robot's actions and its performance metrics over training episodes.

---

## Machine Learning Details

### Algorithm: Deep Q-Network (DQN)
- **Why DQN?**
  - Handles environments with discrete actions (e.g., moving in cardinal directions).
  - Efficiently learns by approximating Q-values with a neural network, avoiding the need for exhaustive state-action pair storage.
  - Incorporates experience replay for stable and efficient learning.

- **How It Works**:
  1. **State Representation**: The robot observes its current position, the room grid layout, dirt locations, and obstacles.
  2. **Action Selection**: The agent selects actions (e.g., move up, down, left, right) using an epsilon-greedy policy.
  3. **Reward Feedback**:
      - **Positive Rewards**: For cleaning a dirt tile.
      - **Negative Rewards**: For hitting obstacles or unnecessary moves.
      - **Zero Rewards**: For neutral actions.
  4. **Experience Replay**: Stores transitions (`state`, `action`, `reward`, `next_state`) in a buffer and samples mini-batches during training to break correlation in the data.
  5. **Q-Network Training**: The neural network updates Q-values by minimizing the Temporal Difference (TD) error:
      \[
      \text{Loss} = \left( r + \gamma \max_{a'} Q(s', a') - Q(s, a) \right)^2
      \]
      Where:
      - \( r \) is the reward.
      - \( \gamma \) is the discount factor.
      - \( Q(s, a) \) is the Q-value for state \( s \) and action \( a \).

---

## Reward System

The reward function is designed to encourage the agent to clean the room efficiently:
- **Positive Reward**: +10 for cleaning a dirt tile.
- **Negative Rewards**:
  - -5 for hitting an obstacle.
  - -1 for every step taken to discourage unnecessary movements.
- **Zero Reward**: 0 for neutral actions that do not directly affect progress.

The cumulative reward per episode reflects the agent's overall performance:
- High positive rewards indicate efficient cleaning.
- Negative rewards suggest suboptimal strategies or frequent collisions.

---

## Training Process

1. **Initialization**:
   - The room grid is randomly initialized with dirt tiles, obstacles, and furniture.
   - The robot starts at a random position.

2. **Exploration and Exploitation**:
   - The agent initially explores the environment (high epsilon value in epsilon-greedy policy).
   - Over time, the agent shifts to exploiting learned strategies (low epsilon value).

3. **Experience Replay**:
   - Transitions are stored in a replay buffer.
   - Mini-batches are sampled during training to update the Q-network.

4. **Learning**:
   - The Q-network is trained using the Mean Squared Error (MSE) loss between the predicted and target Q-values.
   - Training continues for a predefined number of episodes or until convergence.

5. **Evaluation**:
   - The agent’s performance is measured by the cumulative reward per episode and the number of cleaned tiles.

---

## Features

1. **Reinforcement Learning Agent**:
   - Trained using DQN.
   - Learns optimal cleaning paths through trial and error.

2. **Simulated Environment**:
   - Dynamic room layouts with configurable dirt, obstacles, and furniture.

3. **Real-time Visualization**:
   - Pygame-based rendering of the robot’s trajectory, cleaned tiles, and obstacles.

4. **Data Storage and Visualization**:
   - MongoDB stores simulation results.
   - Chart.js visualizes reward trends over episodes.

5. **Frame Capturing**:
   - Frames of the simulation are captured and converted into a video using FFmpeg.

---

## Possible Enhancements

1. **Algorithm Improvements**:
   - Experiment with advanced RL algorithms like Proximal Policy Optimization (PPO) or Advantage Actor-Critic (A2C) for more complex scenarios.
   - Introduce curriculum learning by gradually increasing environment difficulty.

2. **Dynamic Obstacles**:
   - Add moving obstacles to simulate real-world scenarios.

3. **Continuous Environment**:
   - Transition from grid-based navigation to continuous space navigation.

4. **SLAM Integration**:
   - Incorporate Simultaneous Localization and Mapping (SLAM) to improve room mapping and navigation.

5. **Multifunctionality**:
   - Extend functionality to support vacuuming, mopping, and other cleaning modes.

6. **IoT Integration**:
   - Use IoT sensors to control real-world robotic vacuum cleaners.

---

## Installation and Usage

### 1. Clone the Repository
```bash
git clone <repository-url>
cd vacuum-simulator
```

### 2. Install Dependencies
```bash
pip install -r data/requirements.txt
```

### 3. Start the Backend Server
```bash
cd app
python backend.py
```

### 4. Start the Frontend Server
```bash
cd web
python -m http.server 8000
```

### 5. Run the Simulation
```bash
cd app
python simulation.py
```

### 6. Generate Video from Frames
```bash
cd frames
ffmpeg -framerate 30 -i simulation_frame_%d.png -vf "scale=trunc(iw/2)*2:trunc(ih/2)*2" -c:v libx264 -pix_fmt yuv420p simulation.mp4
```

### 7. View the Frontend
Open a browser and go to:
```
http://<VM-public-IP>:8000/
```

---

## Project Structure

```
vacuum-simulator/
├── app/                     # Backend and simulation logic
│   ├── backend.py           # Flask server for data storage
│   ├── simulation.py        # Simulation logic and RL agent training
│   ├── visualizer.py        # Pygame-based simulation visualization
│   ├── room_environment.py  # Environment setup
│   ├── dqn_agent.py         # RL agent logic
│   └── __init__.py
├── data/                    # Data-related resources
│   ├── README.md            # Documentation
│   ├── requirements.txt     # Python dependencies
│   └── room_maps/           # Saved room maps
├── web/                     # Frontend files
│   ├── index.html           # Frontend visualization
│   ├── style.css            # Optional CSS for styling
├── frames/                  # Saved frames from Pygame simulation
└── README.md                # Project documentation
```

---

## Acknowledgments

This project leverages:
- TensorFlow for reinforcement learning.
- Pygame for real-time visualization.
- Chart.js for data visualization.
- MongoDB for backend data storage.
- FFmpeg for video generation.

