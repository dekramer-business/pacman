"""
This file contains incomplete versions of some agents that can be selected to control Pacman.
You will complete their implementations.

Good luck and happy searching!
"""

import logging

from pacai.core.actions import Actions
from pacai.core.directions import Directions
from pacai.core.search.position import PositionSearchProblem
from pacai.core.search.problem import SearchProblem
from pacai.agents.base import BaseAgent
from pacai.agents.search.base import SearchAgent
from pacai.student.search import breadthFirstSearch
from pacai.core import distance


class CornersProblem(SearchProblem):
    """
    This search problem finds paths through all four corners of a layout.

    You must select a suitable state space and successor function.
    See the `pacai.core.search.position.PositionSearchProblem` class for an example of
    a working SearchProblem.

    Additional methods to implement:

    `pacai.core.search.problem.SearchProblem.startingState`:
    Returns the start state (in your search space,
    NOT a `pacai.core.gamestate.AbstractGameState`).

    `pacai.core.search.problem.SearchProblem.isGoal`:
    Returns whether this search state is a goal state of the problem.
    list len 4 is all corners visited

    `pacai.core.search.problem.SearchProblem.successorStates`:
    Returns successor states, the actions they require, and a cost of 1.
    The following code snippet may prove useful:
    ```
        # returns (successor state, action, cost of taking the action).
        successors = []

        for action in Directions.CARDINAL:
            x, y = currentPosition
            dx, dy = Actions.directionToVector(action)
            nextx, nexty = int(x + dx), int(y + dy)
            hitsWall = self.walls[nextx][nexty]

            if (not hitsWall):
                # Construct the successor.
                successor_cord = (nextx, netxy)
                successor_cost = 1
                #
                corners_seen = list(corner)

        return successors
    ```
    """

    def __init__(self, startingGameState):
        super().__init__()

        self.walls = startingGameState.getWalls()
        self.startingPosition = startingGameState.getPacmanPosition()
        top = self.walls.getHeight() - 2
        right = self.walls.getWidth() - 2

        self.corners = ((1, 1), (1, top), (right, 1), (right, top))
        visited = (False, False, False, False)
        for corner in self.corners:
            if not startingGameState.hasFood(*corner):
                logging.warning('Warning: no food in corner ' + str(corner))

        # *** Your Code Here ***
        # start state has position and list of corners
        self.startingGameState = startingGameState
        self.start = (startingGameState.getPacmanPosition(), visited)

    def startingState(self):
        return self.start

    def isGoal(self, state):
        return state[1].count(True) == 4

    def successorStates(self, state):
        successors = []
        self._numExpanded += 1
        for action in Directions.CARDINAL:
            # print("state[0]: ", state[0])
            x, y = state[0]
            dx, dy = Actions.directionToVector(action)
            nextx, nexty = int(x + dx), int(y + dy)
            hitsWall = self.walls[nextx][nexty]
            next_succ = (nextx, nexty)

            if (not hitsWall):
                visited_corners = list(state[1])
                # Construct the successor.
                if (next_succ in self.corners):
                    visited_corners[self.corners.index(next_succ)] = True

                visited_corners = tuple(visited_corners)
                successor_state = (next_succ, visited_corners)
                successors.append((successor_state, action, 1))

        return successors

    def actionsCost(self, actions):
        """
        Returns the cost of a particular sequence of actions.
        If those actions include an illegal move, return 999999.
        This is implemented for you.
        """

        if (actions is None):
            return 999999

        x, y = self.startingPosition
        for action in actions:
            dx, dy = Actions.directionToVector(action)
            x, y = int(x + dx), int(y + dy)
            if self.walls[x][y]:
                return 999999

        return len(actions)


def cornersHeuristic(state, problem):
    """
    A heuristic for the CornersProblem that you defined.

    This function should always return a number that is a lower bound
    on the shortest path from the state to a goal of the problem;
    i.e. it should be admissible.
    (You need not worry about consistency for this heuristic to receive full credit.)
    """

    # *** Your Code Here ***
    # Get all corners we need
    start_coords = state[0]
    visited_corners_bools = list(state[1])
    points_of_interest = []

    # get corners we havent visited
    for i in range(len(visited_corners_bools)):
        if visited_corners_bools[i] is False:
            points_of_interest.append(problem.corners[i])

    # add start to point of interest
    points_of_interest.append(start_coords)

    # call helper function
    min_dist = open_traveling_salesman(
        points_of_interest, len(points_of_interest) - 1)
    return min_dist


# returns 2d array with distances between all points in a list
def man_distance_between_all_points(points_of_interest):
    dists = []

    # for state and all corners, get distances between
    for x in range(len(points_of_interest)):
        dists.append([])
        for y in range(len(points_of_interest)):
            dists[x].append(distance.manhattan(
                points_of_interest[x], points_of_interest[y]))

    return dists


# returns min dist between points of interest (list) and starting pt index
# min dist represents optimal path between all points via manhattan distance
def open_traveling_salesman(points_of_interest, start_index):
    point_count = len(points_of_interest)
    min_dist = float('inf')  # infinity!

    dists = man_distance_between_all_points(points_of_interest)

    for start_point in range(point_count):
        unvisited_points = set(range(point_count))  # set of unvisited points
        current_point = start_point
        total_distance = 0

        while len(unvisited_points) != 0:
            # find shortest distance to next point
            nearest_point = None
            min_dist_to_unvisited = float('inf')
            for unvisited_point in unvisited_points:
                distance_to_point = dists[current_point][unvisited_point]
                if distance_to_point < min_dist_to_unvisited:
                    min_dist_to_unvisited = distance_to_point
                    nearest_point = unvisited_point

            # calc total and remove from unvisited
            total_distance += dists[current_point][nearest_point]
            unvisited_points.remove(nearest_point)
            current_point = nearest_point

        min_dist = min(min_dist, total_distance)  # get shortest dist

    return min_dist


def foodHeuristic(state, problem):
    """
    Your heuristic for the FoodSearchProblem goes here.

    This heuristic must be consistent to ensure correctness.
    First, try to come up with an admissible heuristic;
    almost all admissible heuristics will be consistent as well.

    If using A* ever finds a solution that is worse than what uniform cost search finds,
    your heuristic is *not* consistent, and probably not admissible!
    On the other hand, inadmissible or inconsistent heuristics may find optimal solutions,
    so be careful.

    The state is a tuple (pacmanPosition, foodGrid) where foodGrid is a
    `pacai.core.grid.Grid` of either True or False.
    You can call `foodGrid.asList()` to get a list of food coordinates instead.

    If you want access to info like walls, capsules, etc., you can query the problem.
    For example, `problem.walls` gives you a Grid of where the walls are.

    If you want to *store* information to be reused in other calls to the heuristic,
    there is a dictionary called problem.heuristicInfo that you can use.
    For example, if you only want to count the walls once and store that value, try:
    ```
    problem.heuristicInfo['wallCount'] = problem.walls.count()
    ```
    Subsequent calls to this heuristic can access problem.heuristicInfo['wallCount'].
    """

    position, foodGrid = state

    # *** Your Code Here ***
    foodGridList = foodGrid.asList()

    # If no food, goal!
    if len(foodGridList) == 0:
        return 0

    min_dist = 0

    for point in foodGridList:
        maze_dist = distance.maze(position, point, problem.startingGameState)
        if maze_dist > min_dist:
            min_dist = maze_dist
    
    return min_dist


class ClosestDotSearchAgent(SearchAgent):
    """
    Search for all food using a sequence of searches.
    """

    def __init__(self, index, **kwargs):
        super().__init__(index, **kwargs)

    def registerInitialState(self, state):
        self._actions = []
        self._actionIndex = 0

        currentState = state

        while (currentState.getFood().count() > 0):
            nextPathSegment = self.findPathToClosestDot(
                currentState)  # The missing piece
            self._actions += nextPathSegment

            for action in nextPathSegment:
                legal = currentState.getLegalActions()
                if action not in legal:
                    raise Exception('findPathToClosestDot returned an illegal move: %s!\n%s' %
                                    (str(action), str(currentState)))

                currentState = currentState.generateSuccessor(0, action)

        logging.info('Path found with cost %d.' % len(self._actions))

    def findPathToClosestDot(self, gameState):
        """
        Returns a path (a list of actions) to the closest dot, starting from gameState.
        """

        # Here are some useful elements of the startState
        # startPosition = gameState.getPacmanPosition()
        # food = gameState.getFood()
        # walls = gameState.getWalls()
        # problem = AnyFoodSearchProblem(gameState)

        # *** Your Code Here ***
        problem = AnyFoodSearchProblem(gameState, gameState.getPacmanPosition())
        return breadthFirstSearch(problem)


class AnyFoodSearchProblem(PositionSearchProblem):
    """
    A search problem for finding a path to any food.

    This search problem is just like the PositionSearchProblem,
    but has a different goal test, which you need to fill in below.
    The state space and successor function do not need to be changed.

    The class definition above, `AnyFoodSearchProblem(PositionSearchProblem)`,
    inherits the methods of `pacai.core.search.position.PositionSearchProblem`.

    You can use this search problem to help you fill in
    the `ClosestDotSearchAgent.findPathToClosestDot` method.

    Additional methods to implement:

    `pacai.core.search.position.PositionSearchProblem.isGoal`:
    The state is Pacman's position.
    Fill this in with a goal test that will complete the problem definition.
    """

    def __init__(self, gameState, start=None):
        super().__init__(gameState, goal=None, start=start)

        # Store the food for later reference.
        self.food = gameState.getFood()
    
    def isGoal(self, state):
        # print("self.food: ", self.food)
        (x, y) = state
        if (self.food[x][y] is True):
            return True
        
        return False


class ApproximateSearchAgent(BaseAgent):
    """
    Implement your contest entry here.

    Additional methods to implement:

    `pacai.agents.base.BaseAgent.getAction`:
    Get a `pacai.bin.pacman.PacmanGameState`
    and return a `pacai.core.directions.Directions`.

    `pacai.agents.base.BaseAgent.registerInitialState`:
    This method is called before any moves are made.
    """

    def __init__(self, index, **kwargs):
        super().__init__(index, **kwargs)
