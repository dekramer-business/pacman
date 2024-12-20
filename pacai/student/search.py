"""
In this file, you will implement generic search algorithms which are called by Pacman agents.
"""
from collections import deque
from queue import PriorityQueue


def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first [p 85].

    Your search algorithm needs to return a list of actions that reaches the goal.
    Make sure to implement a graph search algorithm [Fig. 3.7].

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:
    ```
    print("Start: %s" % (str(problem.startingState())))
    print("Is the start a goal?: %s" % (problem.isGoal(problem.startingState())))
    print("Start's successors: %s" % (problem.successorStates(problem.startingState())))
    ```
    """

    # *** Your Code Here ***
    if problem.isGoal(problem.startingState()):
        return []

    frontier = deque([problem.startingState()])  # stack for DFS
    explored = set()  # init empty set
    parents = {}

    while True:
        if len(frontier) == 0:  # if frontier empty, failure
            return

        # using stack for DFS, pop's right by default
        current_node = frontier.pop()

        # if this is the goal state, generate a path from goal to start via parents dictionary
        if problem.isGoal(current_node):
            directions = []
            while True:
                parent = parents.get(current_node)
                if parent is None:  # when get returns None, we found the full path
                    break
                else:  # otherwise unpack the next node and the direction it took
                    (current_node, direction) = parent

                directions.append(direction)

            # directions are in reverse, flip the list
            # This is faster than prepending every time in native python
            directions.reverse()
            return directions

        explored.add(current_node)
        # unpack neighbor, direction, and path weight for each neighboring node
        for (neighbor, direction, weight) in problem.successorStates(current_node):
            if (neighbor not in frontier) and (neighbor not in explored):
                # add neighbor to frontier, appends right by default
                frontier.append(neighbor)
                # set neighbor's parent and parent->neighbor direction here
                # can also set path weight and use that to calculate the full path at the end
                parents[neighbor] = (current_node, direction)


def breadthFirstSearch(problem):
    """
    Search the shallowest nodes in the search tree first. [p 81]
    # """
    # print("Start: %s" % (str(problem.startingState())))
    # print("Is the start a goal?: %s" %
    #       (problem.isGoal(problem.startingState())))
    # print("Start's successors: %s" %
    #       (problem.successorStates(problem.startingState())))
    # print("succesor's directions type: ", type(
    #     (problem.successorStates(problem.startingState()))[0][1]))

    # *** Your Code Here ***
    if problem.isGoal(problem.startingState()):
        return []

    frontier = deque([problem.startingState()])  # queue for BFS
    explored = set()  # init empty set
    parents = {}

    while True:
        if len(frontier) == 0:  # if frontier empty, failure
            return

        # using queue for BFS, pop left needed for FIFO
        current_node = frontier.popleft()

        # if this is the goal state, generate a path from goal to start via parents dictionary
        if problem.isGoal(current_node):
            directions = []
            while True:
                parent = parents.get(current_node)
                if parent is None:  # when get returns None, we found the full path
                    break
                else:  # otherwise unpack the next node and the direction it took
                    (current_node, direction) = parent

                directions.append(direction)

            # directions are in reverse, flip the list
            # This is faster than prepending every time in native python
            directions.reverse()
            return directions

        explored.add(current_node)
        # unpack neighbor, direction, and path weight for each neighboring node
        for (neighbor, direction, weight) in problem.successorStates(current_node):
            if (neighbor not in frontier) and (neighbor not in explored):
                # add neighbor to frontier, appends right by default
                frontier.append(neighbor)
                # set neighbor's parent and parent->neighbor direction here
                # can also set path weight and use that to calculate the full path at the end
                parents[neighbor] = (current_node, direction)


def uniformCostSearch(problem):
    """
    Search the node of least total cost first.
    """

    # *** Your Code Here ***
    if problem.isGoal(problem.startingState()):
        return []

    frontier = PriorityQueue()  # priority queue for UCS
    frontier.put((0, problem.startingState()))  # start state cost of 0

    explored = set()  # init empty set
    parents = {}  # dictionary to hold parents
    goal_node = None

    while frontier.qsize() > 0:
        # using priority queue for UCS
        frontier_get = frontier.get()
        (parent_path_weight, current_node) = frontier_get

        # if this is the goal state, youre done
        if problem.isGoal(current_node):
            goal_node = current_node
            break

        explored.add(current_node)
        current_frontier = {ndwt[1]: ndwt[0] for ndwt in frontier.queue}
        # unpack neighbor, direction, and path weight for each neighboring node
        for (neighbor, direction, weight) in problem.successorStates(current_node):
            if (neighbor not in current_frontier) and (neighbor not in explored):
                # add neighbor and (path weight + parent weight) to frontier
                frontier.put((weight + parent_path_weight, neighbor))
                parents[neighbor] = (current_node, direction)
            elif (neighbor in current_frontier
                    and current_frontier[neighbor] > weight + parent_path_weight):
                # update current_frontier dictionary, repush everything to frontier
                current_frontier[neighbor] = weight + parent_path_weight
                frontier = PriorityQueue()

                for nd, wt in current_frontier.items():
                    frontier.put((wt, nd))
                parents[neighbor] = (current_node, direction)

    # frontier is empty, if no node found return, else generate path
    if goal_node is not None:
        # Below code uses the dictionary to generate a path from any node to initial
        directions = []
        current_node = goal_node
        while True:
            parent = parents.get(current_node)
            if parent is None:  # when get returns None, we found the full path
                break
            else:  # otherwise unpack the next node and the direction it took
                (current_node, direction) = parent

            directions.append(direction)

        # directions are in reverse, flip the list
        # This is faster than prepending every time in native python
        directions.reverse()
        return directions
    else:
        return
        

def aStarSearch(problem, heuristic):
    """
    Search the node that has the lowest combined cost and heuristic first.
    """

    # *** Your Code Here ***
    if problem.isGoal(problem.startingState()):
        return []

    frontier = PriorityQueue()  # priority queue for UCS
    frontier.put((0, problem.startingState()))  # start state cost of 0

    explored = set()  # init empty set
    parents = {}  # dictionary to hold parents
    path_cost_to_node = {}
    path_cost_to_node[problem.startingState()] = 0
    goal_node = None

    while frontier.qsize() > 0:
        # using priority queue for UCS
        frontier_get = frontier.get()
        (heuristic_weight, current_node) = frontier_get
        parent_path_weight = path_cost_to_node[current_node]

        # set goal if this is the goal state
        if problem.isGoal(current_node):
            goal_node = current_node
            break

        explored.add(current_node)
        # Priority queues are not searchable by element in python, this is a workaround
        searchable_frontier = {ndwt[1]: ndwt[0] for ndwt in frontier.queue}
        # unpack neighbor, direction, and path weight for each neighboring node
        for (neighbor, direction, weight) in problem.successorStates(current_node):
            cost = weight + parent_path_weight
            heuristic_cost = heuristic(neighbor, problem)

            if (neighbor not in searchable_frontier) and (neighbor not in explored):
                # add neighbor and (path weight + parent weight) to frontier
                frontier.put((cost + heuristic_cost, neighbor))
                parents[neighbor] = (current_node, direction)
                path_cost_to_node[neighbor] = cost
            elif (neighbor in searchable_frontier
                    and searchable_frontier[neighbor] > cost + heuristic_cost):
                # update searchable_frontier dictionary, repush everything to frontier
                searchable_frontier[neighbor] = cost + heuristic_cost
                frontier = PriorityQueue()

                for nd, wt in searchable_frontier.items():
                    frontier.put((wt, nd))
                
                # update path cost to this node if this cost is cheaper than it
                # was previously, also update parent
                if path_cost_to_node[neighbor] < cost:
                    path_cost_to_node[neighbor] = cost
                    parents[neighbor] = (current_node, direction)

    # frontier is empty, if no node found return, else generate path
    if goal_node is not None:
        # Below code uses the dictionary to generate a path from any node to initial
        directions = []
        current_node = goal_node
        while True:
            parent = parents.get(current_node)
            if parent is None:  # when get returns None, we found the full path
                break
            else:  # otherwise unpack the next node and the direction it took
                (current_node, direction) = parent

            directions.append(direction)

        # directions are in reverse, flip the list
        # This is faster than prepending every time in native python
        directions.reverse()
        return directions
    else:
        return