# grid_game.py
import random


class GridHuntGame:
    """A small Pacman-style grid environment (4x4) where an agent collects food."""

    def __init__(self, width=4, height=4):
        self.width = width
        self.height = height
        self.agent_pos = [0, 0]  # Starting position (x, y)

        # Place a few random food pellets and obstacles (walls)
        self.food_positions = {[1, 2], [2, 3], [3, 0], [2, 1]}
        self.walls = {[1, 1], [2, 2]}

        self.score = 0
        self.steps = 0

    def get_percept(self) -> dict:
    x, y = self.agent_pos

    # Find the cell directly in front of the agent
    front_x, front_y = x, y

    if self.direction == "Up":
        front_y += 1
    elif self.direction == "Down":
        front_y -= 1
    elif self.direction == "Left":
        front_x -= 1
    elif self.direction == "Right":
        front_x += 1

    # Check whether the cell in front is outside the grid
    # or contains a wall
    wall_ahead = (
        front_x < 0 or
        front_x >= self.width or
        front_y < 0 or
        front_y >= self.height or
        (front_x, front_y) in self.walls
    )

    # Check food in the adjacent cell
    food_ahead = (front_x, front_y) in self.food_positions

    # Check toxic trap in the adjacent cell
    toxin_ahead = (front_x, front_y) in self.toxic_traps

    return {
        'wall_ahead': wall_ahead,
        'food_ahead': food_ahead,
        'toxin_ahead': toxin_ahead
    }

    def execute_action(self, agent, action: str):
        self.steps += 1
        new_pos = list(self.agent_pos)

        if action == 'Up':
            new_pos[1] = min(self.height - 1, new_pos[1] + 1)
        elif action == 'Down':
            new_pos[1] = max(0, new_pos[1] - 1)
        elif action == 'Left':
            new_pos[0] = max(0, new_pos[0] - 1)
        elif action == 'Right':
            new_pos[0] = min(self.width - 1, new_pos[0] + 1)

        # Check collision with walls
        if tuple(new_pos) in self.walls:
            self.score -= 5  # Penalty for hitting a wall
        else:
            self.agent_pos = new_pos

        # Check if eating food
        tuple_pos = tuple(self.agent_pos)
        if tuple_pos in self.food_positions:
            self.food_positions.remove(tuple_pos)
            self.score += 20  # Reward for eating food pellet

    def is_done(self) -> bool:
        return len(self.food_positions) == 0 or self.steps >= 20


class SimpleReflexAgent:
    def sense_and_act(self, percept):
        # IF food is ahead THEN move forward
        if percept['food_ahead']:
            return "Right"

        # IF there is a wall ahead THEN turn left
        if percept['wall_ahead']:
            return "Left"

        # ELSE move forward
        return "Right"    


class ModelBasedAgent:
    def __init__(self):
        self.visited_cells = set()
        self.last_action = None

    def sense_and_act(self, percept):
        # Update internal state
        current_state = (
            percept['wall_ahead'],
            percept['food_ahead'],
            percept['toxin_ahead']
        )

        self.visited_cells.add(current_state)

        # IF food is ahead THEN move forward
        if percept['food_ahead']:
            action = "Right"

        # IF wall is ahead AND this situation was already visited
        # THEN choose an alternative action
        elif percept['wall_ahead'] and current_state in self.visited_cells:
            action = "Left"

        # IF wall is ahead THEN turn left
        elif percept['wall_ahead']:
            action = "Left"

        # ELSE move forward
        else:
            action = "Right"

        # Remember the last action
        self.last_action = action

        return action       