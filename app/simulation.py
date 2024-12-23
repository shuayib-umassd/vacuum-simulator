from app.room_environment import RoomEnvironment
from app.dqn_agent import DQNAgent
from app.visualizer import PygameVisualizer
from app.backend import save_simulation_data
import numpy as np
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

def train_agent(env, agent, visualizer, episodes=100):
    batch_size = 32
    for episode in range(episodes):
        state = env.reset()
        state = np.array(state)
        done = False
        total_reward = 0
        while not done:
            action = agent.act(state)
            next_state, reward, done = env.step(action)
            next_state = np.array(next_state)
            agent.remember(state, action, reward, next_state, done)
            state = next_state
            total_reward += reward
            visualizer.draw()

        if len(agent.memory) > batch_size:
            agent.replay(batch_size)

        save_simulation_data(env, episode, total_reward)
        print(f"Episode {episode + 1}: Total reward = {total_reward}")

if __name__ == '__main__':
    size = (10, 10)
    obstacles = [(1, 1), (3, 3)]
    dirt = [(0, 4), (4, 0), (2, 2)]
    furniture = [(5, 5), (6, 7)]
    
    env = RoomEnvironment(size, dirt, obstacles, furniture)
    state_size = len(env.get_state())
    action_size = 3
    agent = DQNAgent(state_size, action_size)
    visualizer = PygameVisualizer(env)

    try:
        train_agent(env, agent, visualizer)
    finally:
        visualizer.close()