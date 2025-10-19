import heapq
import math
from typing import List
import numpy as np
from entities.Robot import Robot
from entities.Entity import Obstacle, CellState, Grid
from consts import Direction, MOVE_DIRECTIONS, TURN_FACTOR, MAX_ITERATIONS, TURN_RADIUS, SAFE_TURN_COST
from python_tsp.exact import solve_tsp_dynamic_programming

turn_adjustments = [
    [3 * TURN_RADIUS, TURN_RADIUS],
    [4 * TURN_RADIUS, 2 * TURN_RADIUS]
]


class MazeSolver:
    def __init__(self, width: int, height: int, robot_x: int, robot_y: int, robot_dir: Direction, big_turn=None, allow_45=True):
        self.grid = Grid(width, height)
        self.robot = Robot(robot_x, robot_y, robot_dir)
        self.path_map = {}
        self.cost_map = {}
        self.big_turn = 0 if big_turn is None else int(big_turn)
        self.allow_45 = allow_45

    def add_obstacle(self, x: int, y: int, direction: Direction, obstacle_id: int):
        obstacle = Obstacle(x, y, direction, obstacle_id)
        self.grid.add_obstacle(obstacle)

    def reset_obstacles(self):
        self.grid.reset_obstacles()

    @staticmethod
    def compute_coord_distance(x1: int, y1: int, x2: int, y2: int, level=1):
        dx = x1 - x2
        dy = y1 - y2
        if level == 2:
            return math.sqrt(dx ** 2 + dy ** 2)
        return abs(dx) + abs(dy)

    @staticmethod
    def compute_state_distance(start: CellState, end: CellState, level=1):
        return MazeSolver.compute_coord_distance(start.x, start.y, end.x, end.y, level)

    @staticmethod
    def get_visit_options(count):
        options = []
        bits = bin(2 ** count - 1).count('1')
        for i in range(2 ** count):
            options.append(bin(i)[2:].zfill(bits))
        options.sort(key=lambda val: val.count('1'), reverse=True)
        return options

    def get_optimal_order_dp(self, retry_flag) -> List[CellState]:
        best_distance = 1e9
        best_path = []

        view_positions = self.grid.get_view_obstacle_positions(retry_flag)

        for option in self.get_visit_options(len(view_positions)):
            items = [self.robot.get_start_state()]
            current_views = []

            for idx, bit in enumerate(option):
                if bit == '1':
                    items += view_positions[idx]
                    current_views.append(view_positions[idx])

            self.generate_path_costs(items)

            combinations = []
            self.generate_combinations(current_views, 0, [], combinations, [MAX_ITERATIONS])

            for combination in combinations:
                visited_nodes = [0]
                index_offset = 1
                fixed_cost = 0

                for i, view_set in enumerate(current_views):
                    visited_nodes.append(index_offset + combination[i])
                    fixed_cost += view_set[combination[i]].penalty
                    index_offset += len(view_set)

                cost_matrix = np.zeros((len(visited_nodes), len(visited_nodes)))

                for start_idx in range(len(visited_nodes) - 1):
                    for end_idx in range(start_idx + 1, len(visited_nodes)):
                        start_state = items[visited_nodes[start_idx]]
                        end_state = items[visited_nodes[end_idx]]
                        if (start_state, end_state) in self.cost_map:
                            cost_matrix[start_idx][end_idx] = self.cost_map[(start_state, end_state)]
                        else:
                            cost_matrix[start_idx][end_idx] = 1e9
                        cost_matrix[end_idx][start_idx] = cost_matrix[start_idx][end_idx]

                cost_matrix[:, 0] = 0
                permutation, total_cost = solve_tsp_dynamic_programming(cost_matrix)

                if total_cost + fixed_cost >= best_distance:
                    continue

                best_path = [items[0]]
                best_distance = total_cost + fixed_cost

                for i in range(len(permutation) - 1):
                    start_state = items[visited_nodes[permutation[i]]]
                    end_state = items[visited_nodes[permutation[i + 1]]]
                    path_segment = self.path_map[(start_state, end_state)]
                    for j in range(1, len(path_segment)):
                        best_path.append(CellState(path_segment[j][0], path_segment[j][1], path_segment[j][2]))
                    best_path[-1].set_screenshot(end_state.screenshot_id)

            if best_path:
                break

        return best_path, best_distance

    @staticmethod
    def generate_combinations(view_positions, index, current, result, iterations):
        if index == len(view_positions):
            result.append(current[:])
            return
        if iterations[0] == 0:
            return
        iterations[0] -= 1
        for j in range(len(view_positions[index])):
            current.append(j)
            MazeSolver.generate_combinations(view_positions, index + 1, current, result, iterations)
            current.pop()

    def get_safe_cost(self, x, y):
        for obstacle in self.grid.obstacles:
            if abs(obstacle.x - x) == 2 and abs(obstacle.y - y) == 2:
                return SAFE_TURN_COST
            if abs(obstacle.x - x) == 1 and abs(obstacle.y - y) == 2:
                return SAFE_TURN_COST
            if abs(obstacle.x - x) == 2 and abs(obstacle.y - y) == 1:
                return SAFE_TURN_COST
            if abs(obstacle.x - x) <= 1 and abs(obstacle.y - y) <= 1:
                return SAFE_TURN_COST
        return 0

    def get_neighbors(self, x, y, direction):
        neighbors = []

        # Forward / backward
        for dx, dy, new_dir in MOVE_DIRECTIONS:
            if new_dir == direction:
                if self.grid.reachable(x + dx, y + dy):
                    cost = self.get_safe_cost(x + dx, y + dy)
                    neighbors.append((x + dx, y + dy, new_dir, cost))
                if self.grid.reachable(x - dx, y - dy):
                    cost = self.get_safe_cost(x - dx, y - dy)
                    neighbors.append((x - dx, y - dy, new_dir, cost))

        # 45° diagonals
        if self.allow_45:
            for dx, dy, new_dir in MOVE_DIRECTIONS:
                diff = (int(new_dir) - int(direction)) % 8
                if diff in [1, 7]:
                    if self.grid.reachable(x + dx, y + dy, turn=True) and self.grid.reachable(x, y, preTurn=True):
                        cost = self.get_safe_cost(x + dx, y + dy)
                        neighbors.append((x + dx, y + dy, new_dir, cost + 5))

        # 90° arcs
        large_shift, small_shift = turn_adjustments[self.big_turn]

        if direction == Direction.NORTH:
            for dx, dy, new_dir in [(large_shift, small_shift, Direction.EAST), (-small_shift, -large_shift, Direction.EAST)]:
                if self.grid.reachable(x + dx, y + dy, turn=True) and self.grid.reachable(x, y, preTurn=True):
                    cost = self.get_safe_cost(x + dx, y + dy)
                    neighbors.append((x + dx, y + dy, new_dir, cost + 10))

        elif direction == Direction.EAST:
            for dx, dy, new_dir in [
                (small_shift, large_shift, Direction.NORTH),
                (-large_shift, -small_shift, Direction.NORTH),
                (small_shift, -large_shift, Direction.SOUTH),
                (-large_shift, small_shift, Direction.SOUTH),
            ]:
                if self.grid.reachable(x + dx, y + dy, turn=True) and self.grid.reachable(x, y, preTurn=True):
                    cost = self.get_safe_cost(x + dx, y + dy)
                    neighbors.append((x + dx, y + dy, new_dir, cost + 10))

        elif direction == Direction.SOUTH:
            for dx, dy, new_dir in [
                (large_shift, -small_shift, Direction.EAST),
                (-small_shift, large_shift, Direction.EAST),
                (-large_shift, -small_shift, Direction.WEST),
                (small_shift, large_shift, Direction.WEST),
            ]:
                if self.grid.reachable(x + dx, y + dy, turn=True) and self.grid.reachable(x, y, preTurn=True):
                    cost = self.get_safe_cost(x + dx, y + dy)
                    neighbors.append((x + dx, y + dy, new_dir, cost + 10))

        elif direction == Direction.WEST:
            for dx, dy, new_dir in [
                (-small_shift, -large_shift, Direction.SOUTH),
                (large_shift, small_shift, Direction.SOUTH),
                (-small_shift, large_shift, Direction.NORTH),
                (large_shift, -small_shift, Direction.NORTH),
            ]:
                if self.grid.reachable(x + dx, y + dy, turn=True) and self.grid.reachable(x, y, preTurn=True):
                    cost = self.get_safe_cost(x + dx, y + dy)
                    neighbors.append((x + dx, y + dy, new_dir, cost + 10))

        return neighbors

    def generate_path_costs(self, states: List[CellState]):
        def record_path(start, end, parents, total_cost):
            self.cost_map[(start, end)] = total_cost
            self.cost_map[(end, start)] = total_cost

            path = []
            node = (end.x, end.y, end.direction)

            while node in parents:
                path.append(node)
                node = parents[node]
            path.append(node)

            self.path_map[(start, end)] = path[::-1]
            self.path_map[(end, start)] = path

        def astar(start: CellState, end: CellState):
            if (start, end) in self.path_map:
                return

            g_costs = {(start.x, start.y, start.direction): 0}
            open_set = [(self.compute_state_distance(start, end), start.x, start.y, start.direction)]
            parents = {}
            visited = set()

            while open_set:
                _, x, y, direction = heapq.heappop(open_set)
                if (x, y, direction) in visited:
                    continue
                if end.is_eq(x, y, direction):
                    record_path(start, end, parents, g_costs[(x, y, direction)])
                    return

                visited.add((x, y, direction))
                current_cost = g_costs[(x, y, direction)]

                for nx, ny, nd, safety_cost in self.get_neighbors(x, y, direction):
                    if (nx, ny, nd) in visited:
                        continue

                    step_cost = math.sqrt((nx - x) ** 2 + (ny - y) ** 2)
                    move_cost = Direction.rotation_cost(nd, direction) * TURN_FACTOR + step_cost + safety_cost

                    if (nx, ny, nd) not in g_costs or g_costs[(nx, ny, nd)] > current_cost + move_cost:
                        g_costs[(nx, ny, nd)] = current_cost + move_cost
                        parents[(nx, ny, nd)] = (x, y, direction)

                        heuristic = self.compute_coord_distance(nx, ny, end.x, end.y, level=2)
                        total_cost = g_costs[(nx, ny, nd)] + move_cost + heuristic
                        heapq.heappush(open_set, (total_cost, nx, ny, nd))

        for i in range(len(states) - 1):
            for j in range(i + 1, len(states)):
                astar(states[i], states[j])


if __name__ == "__main__":
    pass
