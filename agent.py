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

    def __init__(self):
        self.plan = []
        self.active_algo = 'AStar'

    # ---------------- BFS ----------------
    def bfs_search(self, start, goal, grid_size, walls):

        queue = deque()
        queue.append((start, []))

        reached = {start}

        while queue:

            current, path = queue.popleft()

            if current == goal:
                return path

            for next_state, action in self.get_neighbors(
                current, grid_size, walls
            ):

                if next_state not in reached:
                    reached.add(next_state)
                    queue.append(
                        (next_state, path + [action])
                    )

        return []

    # ---------------- DFS ----------------
    def dfs_search(self, start, goal, grid_size, walls):

        stack = []
        stack.append((start, []))

        reached = {start}

        while stack:

            current, path = stack.pop()

            if current == goal:
                return path

            for next_state, action in self.get_neighbors(
                current, grid_size, walls
            ):

                if next_state not in reached:
                    reached.add(next_state)
                    stack.append(
                        (next_state, path + [action])
                    )

        return []

    # ---------------- UCS ----------------
    def ucs_search(self, start, goal, grid_size, walls):

        priority_queue = []

        heapq.heappush(
            priority_queue,
            (0, start, [])
        )

        reached = {start: 0}

        while priority_queue:

            cost, current, path = heapq.heappop(
                priority_queue
            )

            if current == goal:
                return path

            for next_state, action in self.get_neighbors(
                current, grid_size, walls
            ):

                new_cost = cost + 1

                if (
                    next_state not in reached
                    or new_cost < reached[next_state]
                ):

                    reached[next_state] = new_cost

                    heapq.heappush(
                        priority_queue,
                        (
                            new_cost,
                            next_state,
                            path + [action]
                        )
                    )

        return []

    # ---------------- Manhattan Distance ----------------
    def manhattan_distance(self, pos, goal):

        x1, y1 = pos
        x2, y2 = goal

        return abs(x1 - x2) + abs(y1 - y2)

    # ---------------- Euclidean Distance ----------------
    def euclidean_distance(self, pos, goal):

        x1, y1 = pos
        x2, y2 = goal

        return math.sqrt(
            (x1 - x2) ** 2 +
            (y1 - y2) ** 2
        )

    # ---------------- A* Search ----------------
    def astar_search(
        self,
        start_pos,
        goal_pos,
        walls,
        grid_size,
        heuristic_type='manhattan'
    ):

        priority_queue = []
        reached_states = set()

        # Starting node
        g_cost = 0

        if heuristic_type == 'manhattan':
            h_cost = self.manhattan_distance(
                start_pos,
                goal_pos
            )
        else:
            h_cost = self.euclidean_distance(
                start_pos,
                goal_pos
            )

        f_cost = g_cost + h_cost

        heapq.heappush(
            priority_queue,
            (
                f_cost,
                g_cost,
                start_pos,
                []
            )
        )

        while priority_queue:

            f_cost, g_cost, current_pos, path_taken = (
                heapq.heappop(priority_queue)
            )

            if current_pos == goal_pos:
                return path_taken

            reached_states.add(current_pos)

            # Expand neighbors
            for next_pos, action in self.get_neighbors(
                current_pos,
                grid_size,
                walls
            ):

                if next_pos not in reached_states:

                    g_new = g_cost + 1

                    if heuristic_type == 'manhattan':
                        h_new = self.manhattan_distance(
                            next_pos,
                            goal_pos
                        )
                    else:
                        h_new = self.euclidean_distance(
                            next_pos,
                            goal_pos
                        )

                    f_new = g_new + h_new

                    heapq.heappush(
                        priority_queue,
                        (
                            f_new,
                            g_new,
                            next_pos,
                            path_taken + [action]
                        )
                    )

        return []

    # ---------------- Neighbors ----------------
    def get_neighbors(
        self,
        current,
        grid_size,
        walls
    ):

        width, height = grid_size

        x, y = current

        moves = [
            ((x, y + 1), 'Up'),
            ((x, y - 1), 'Down'),
            ((x - 1, y), 'Left'),
            ((x + 1, y), 'Right')
        ]

        for (nx, ny), action in moves:

            if (
                0 <= nx < width
                and 0 <= ny < height
                and (nx, ny) not in walls
            ):

                yield (nx, ny), action

    # ---------------- Sense and Act ----------------
    def sense_and_act(self, percept: dict) -> str:

        pos = percept['agent_pos']

        # If there is no current plan,
        # calculate a new path
        if not self.plan:

            # Get remaining food
            foods = percept.get(
                'remaining_food',
                percept.get('all_food', [])
            )

            if foods:

                # Find closest food
                goal_pos = min(
                    foods,
                    key=lambda food:
                    abs(food[0] - pos[0]) +
                    abs(food[1] - pos[1])
                )

                grid_size = percept['grid_size']
                walls = percept['walls']

                # BFS
                if self.active_algo == 'BFS':

                    self.plan = self.bfs_search(
                        pos,
                        goal_pos,
                        grid_size,
                        walls
                    )

                # DFS
                elif self.active_algo == 'DFS':

                    self.plan = self.dfs_search(
                        pos,
                        goal_pos,
                        grid_size,
                        walls
                    )

                # UCS
                elif self.active_algo == 'UCS':

                    self.plan = self.ucs_search(
                        pos,
                        goal_pos,
                        grid_size,
                        walls
                    )

                # A*
                elif self.active_algo == 'AStar':

                    self.plan = self.astar_search(
                        pos,
                        goal_pos,
                        walls,
                        grid_size,
                        heuristic_type='manhattan'
                    )

        # Execute next action
        if self.plan:
            return self.plan.pop(0)

        # Fallback
        return 'Up'


# ---------------- Testing Heuristics ----------------
if __name__ == "__main__":

    agent = SearchAgent()

    start = (0, 0)
    goal = (3, 4)

    print(
        "Manhattan Distance:",
        agent.manhattan_distance(start, goal)
    )

    print(
        "Euclidean Distance:",
        agent.euclidean_distance(start, goal)
    )