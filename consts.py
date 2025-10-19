from enum import Enum


class Direction(int, Enum):
    NORTH = 0
    NORTHEAST = 1
    EAST = 2
    SOUTHEAST = 3
    SOUTH = 4
    SOUTHWEST = 5
    WEST = 6
    NORTHWEST = 7
    SKIP = 8

    def __int__(self):
        return self.value

    @staticmethod
    def rotation_cost(direction1, direction2):
        difference = abs(direction1 - direction2)
        return min(difference, 8 - difference)


MOVE_DIRECTIONS = [
    (0, 1, Direction.NORTH),
    (1, 1, Direction.NORTHEAST),
    (1, 0, Direction.EAST),
    (1, -1, Direction.SOUTHEAST),
    (0, -1, Direction.SOUTH),
    (-1, -1, Direction.SOUTHWEST),
    (-1, 0, Direction.WEST),
    (-1, 1, Direction.NORTHWEST),
]

TURN_FACTOR = 1
EXPANDED_CELL = 1

GRID_WIDTH = 20
GRID_HEIGHT = 20

MAX_ITERATIONS = 2000
TURN_RADIUS = 1

SAFE_TURN_COST = 1000
SNAPSHOT_COST = 50
