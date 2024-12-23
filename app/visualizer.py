import pygame
import os

# Constants for visualization
TILE_SIZE = 50  # Size of each grid square in pixels
MARGIN = 5      # Margin between grid squares in pixels

class PygameVisualizer:
    def __init__(self, env):
        pygame.init()
        self.env = env
        self.window = pygame.display.set_mode(
            (env.size[1] * TILE_SIZE + MARGIN * (env.size[1] + 1),
             env.size[0] * TILE_SIZE + MARGIN * (env.size[0] + 1))
        )
        pygame.display.set_caption("Robot Vacuum Simulation")
        self.clock = pygame.time.Clock()
        self.step_number = 0  # Track the simulation step

        # Create a directory to save frames if it doesn't exist
        if not os.path.exists('frames'):
            os.makedirs('frames')

    def draw(self):
        self.window.fill((255, 255, 255))
        for row in range(self.env.size[0]):
            for col in range(self.env.size[1]):
                color = (200, 200, 200)  # Empty space
                if self.env.grid[row, col] == -1:
                    color = (0, 0, 0)  # Obstacle
                elif self.env.grid[row, col] == 1:
                    color = (0, 255, 0)  # Dirt
                elif self.env.grid[row, col] == 2:
                    color = (139, 69, 19)  # Furniture (brown)

                pygame.draw.rect(
                    self.window,
                    color,
                    [(MARGIN + TILE_SIZE) * col + MARGIN,
                     (MARGIN + TILE_SIZE) * row + MARGIN,
                     TILE_SIZE,
                     TILE_SIZE]
                )

                # Draw room map
                if self.env.room_map[row, col] == 1:
                    pygame.draw.rect(
                        self.window,
                        (100, 100, 255, 100),  # Light blue, semi-transparent
                        [(MARGIN + TILE_SIZE) * col + MARGIN,
                         (MARGIN + TILE_SIZE) * row + MARGIN,
                         TILE_SIZE,
                         TILE_SIZE]
                    )

        # Draw robot
        x, y = self.env.robot_position
        robot_center = [(MARGIN + TILE_SIZE) * y + MARGIN + TILE_SIZE // 2,
                        (MARGIN + TILE_SIZE) * x + MARGIN + TILE_SIZE // 2]
        pygame.draw.circle(self.window, (255, 0, 0), robot_center, TILE_SIZE // 4)

        # Draw direction indicator
        direction_end = [
            robot_center[0] + int(TILE_SIZE * 0.4 * [0, 1, 0, -1][self.env.robot_direction]),
            robot_center[1] + int(TILE_SIZE * 0.4 * [-1, 0, 1, 0][self.env.robot_direction])
        ]
        pygame.draw.line(self.window, (0, 0, 255), robot_center, direction_end, 3)

        # Draw trajectory
        for pos in self.env.trajectory:
            pygame.draw.circle(
                self.window,
                (255, 0, 0, 100),  # Red, semi-transparent
                [(MARGIN + TILE_SIZE) * pos[1] + MARGIN + TILE_SIZE // 2,
                 (MARGIN + TILE_SIZE) * pos[0] + MARGIN + TILE_SIZE // 2],
                2
            )

        pygame.display.flip()

        # Save the current frame as an image
        frame_path = f"frames/simulation_frame_{self.step_number}.png"
        pygame.image.save(self.window, frame_path)
        self.step_number += 1

    def close(self):
        pygame.quit()