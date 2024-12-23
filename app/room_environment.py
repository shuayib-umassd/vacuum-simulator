import numpy as np

class RoomEnvironment:
    def __init__(self, size, dirt_locations, obstacle_locations, furniture_locations):
        self.size = size
        self.initial_dirt = dirt_locations
        self.initial_obstacles = obstacle_locations
        self.initial_furniture = furniture_locations
        self.reset()

    def reset(self):
        self.robot_position = [0, 0]
        self.robot_direction = 0  # 0: up, 1: right, 2: down, 3: left
        self.grid = np.zeros(self.size)
        self.trajectory = []
        self.room_map = np.zeros(self.size)

        for dirt in self.initial_dirt:
            self.grid[dirt[0], dirt[1]] = 1  # Dirt
        for obs in self.initial_obstacles:
            self.grid[obs[0], obs[1]] = -1  # Obstacle
        for furniture in self.initial_furniture:
            self.grid[furniture[0], furniture[1]] = 2  # Furniture

        return self.get_state()

    def step(self, action):
        x, y = self.robot_position
        reward = -1
        done = False

        if action == 0:
            new_x, new_y = x, y
            if self.robot_direction == 0 and x > 0:
                new_x -= 1
            elif self.robot_direction == 1 and y < self.size[1] - 1:
                new_y += 1
            elif self.robot_direction == 2 and x < self.size[0] - 1:
                new_x += 1
            elif self.robot_direction == 3 and y > 0:
                new_y -= 1

            if self.grid[new_x, new_y] not in [-1, 2]:  # Avoid obstacles and furniture
                self.robot_position = [new_x, new_y]
                if self.grid[new_x, new_y] == 1:  # Collect dirt
                    reward = 10
                    self.grid[new_x, new_y] = 0
            else:
                reward = -10  # Penalty for hitting obstacle or furniture

        elif action == 1:
            self.robot_direction = (self.robot_direction - 1) % 4
        elif action == 2:
            self.robot_direction = (self.robot_direction + 1) % 4

        self.trajectory.append(tuple(self.robot_position))
        self.update_room_map()

        if not np.any(self.grid == 1):
            done = True
            reward += 50  # Bonus for completing the task

        return self.get_state(), reward, done

    def get_state(self):
        return self.robot_position + [self.robot_direction] + self.get_sensor_data()

    def get_sensor_data(self):
        sensors = []
        for direction in range(4):
            x, y = self.robot_position
            distance = 0
            while True:
                if direction == 0:
                    x -= 1
                elif direction == 1:
                    y += 1
                elif direction == 2:
                    x += 1
                elif direction == 3:
                    y -= 1
                if x < 0 or x >= self.size[0] or y < 0 or y >= self.size[1] or self.grid[x, y] in [-1, 2]:
                    break
                distance += 1
            sensors.append(distance)
        return sensors

    def update_room_map(self):
        x, y = self.robot_position
        self.room_map[x, y] = 1  # Mark as visited