from collections import deque
import heapq
import math
import random


class GreedyGridAgent:
    """A simple agent that tries to move around systematically to clear the grid."""

    def __init__(self):
        self.actions_pool = ['Up', 'Down', 'Left', 'Right']

    def sense_and_act(self, percept: dict) -> str:
        pos = percept['agent_pos']
        return random.choice(self.actions_pool)


class SearchAgent:

    def bfs_search(self, start, goal, grid_size, walls):

        queue = deque()
        queue.append((start, []))

        reached = {start}

        while queue:

            current, path = queue.popleft()

            if current == goal:
                return path

            for next_state, action in self.get_neighbors(current, grid_size, walls):

                if next_state not in reached:
                    reached.add(next_state)
                    queue.append((next_state, path + [action]))

        return []

    def dfs_search(self, start, goal, grid_size, walls):

        stack = []
        stack.append((start, []))

        reached = {start}

        while stack:

            current, path = stack.pop()

            if current == goal:
                return path

            for next_state, action in self.get_neighbors(current, grid_size, walls):

                if next_state not in reached:
                    reached.add(next_state)
                    stack.append((next_state, path + [action]))

        return []

    def ucs_search(self, start, goal, grid_size, walls):

        priority_queue = []
        heapq.heappush(priority_queue, (0, start, []))

        reached = {start: 0}

        while priority_queue:

            cost, current, path = heapq.heappop(priority_queue)

            if current == goal:
                return path

            for next_state, action in self.get_neighbors(current, grid_size, walls):

                new_cost = cost + 1

                if next_state not in reached or new_cost < reached[next_state]:
                    reached[next_state] = new_cost

                    heapq.heappush(
                        priority_queue,
                        (new_cost, next_state, path + [action])
                    )

        return []

    def manhattan_distance(self, pos, goal):
        x1, y1 = pos
        x2, y2 = goal

        return abs(x1 - x2) + abs(y1 - y2)

    def euclidean_distance(self, pos, goal):
        x1, y1 = pos
        x2, y2 = goal

        return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)


# Testing
agent = SearchAgent()

start = (0, 0)
goal = (3, 4)

print("Manhattan Distance:", agent.manhattan_distance(start, goal))
print("Euclidean Distance:", agent.euclidean_distance(start, goal))