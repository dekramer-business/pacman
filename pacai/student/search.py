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

    # print("Start: %s" % (str(problem.startingState())))
    # print("Is the start a goal?: %s" % (problem.isGoal(problem.startingState())))
    # print("Start's successors: %s" % (problem.successorStates(problem.startingState())))
    # print("succesor's directions type: ", type((problem.successorStates(problem.startingState()))[0][1]))

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

            # directions are in reverse, flip the list. This is faster than prepending every time in native python
            directions.reverse()
            return directions
        

        explored.add(current_node)
        # unpack neighbor, direction, and path weight for each neighboring node
        for (neighbor, direction, weight) in problem.successorStates(current_node):
            if (neighbor not in frontier) and (neighbor not in explored):
                frontier.append(neighbor)  # add neighbor to frontier, appends right by default
                # set neighbor's parent and parent->neighbor direction here
                # can also set path weight and use that to calculate the full path at the end
                parents[neighbor] = (current_node, direction)


def breadthFirstSearch(problem):
    """
    Search the shallowest nodes in the search tree first. [p 81]
    """
    print("Start: %s" % (str(problem.startingState())))
    print("Is the start a goal?: %s" % (problem.isGoal(problem.startingState())))
    print("Start's successors: %s" % (problem.successorStates(problem.startingState())))
    print("succesor's directions type: ", type((problem.successorStates(problem.startingState()))[0][1]))

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

            # directions are in reverse, flip the list. This is faster than prepending every time in native python
            directions.reverse()
            return directions
        

        explored.add(current_node)
        # unpack neighbor, direction, and path weight for each neighboring node
        for (neighbor, direction, weight) in problem.successorStates(current_node):
            if (neighbor not in frontier) and (neighbor not in explored):
                frontier.append(neighbor)  # add neighbor to frontier, appends right by default
                # set neighbor's parent and parent->neighbor direction here
                # can also set path weight and use that to calculate the full path at the end
                parents[neighbor] = (current_node, direction)

def uniformCostSearch(problem):
    """
    Search the node of least total cost first.
    """

    #! I may be doing path cost incorrect, currently nodes are added based on their edge weights.
    #! Should I instead add them based on their total path cost?

    # *** Your Code Here ***
    if problem.isGoal(problem.startingState()):
        return []
    
    frontier = PriorityQueue()  # priority queue for UCS
    frontier.put((0, problem.startingState()))  # starting state has a cost of 0

    explored = set()  # init empty set
    parents = {}

    while True:
        if frontier.qsize() == 0:  # if frontier empty, failure
            return

        # using priority queue for UCS
        frontier_get = frontier.get()
        (parent_weight, current_node) = frontier_get
        
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

            # directions are in reverse, flip the list. This is faster than prepending every time in native python
            directions.reverse()
            return directions
        

        explored.add(current_node)
        # unpack neighbor, direction, and path weight for each neighboring node
        for (neighbor, direction, weight) in problem.successorStates(current_node):
            if (neighbor not in frontier.queue) and (neighbor not in explored):
                #! Should i do parent weight to make decision based on total weight, or just which path is currently cheapest?
                frontier.put((weight + parent_weight, neighbor))  # add neighbor and (path weight + parent weight) to frontier
                # frontier.put((weight, neighbor))  # add neighbor and path weight to frontier
                # set neighbor's parent and parent->neighbor direction here
                # can also set path weight and use that to calculate the full path at the end
                parents[neighbor] = (current_node, direction)

def aStarSearch(problem, heuristic):
    """
    Search the node that has the lowest combined cost and heuristic first.
    """

    # *** Your Code Here ***
    if problem.isGoal(problem.startingState()):
        return []
    
    frontier = PriorityQueue()  # priority queue for UCS
    frontier.put((0, problem.startingState()))  # starting state has a cost of 0

    explored = set()  # init empty set
    parents = {}

    while True:
        if frontier.qsize() == 0:  # if frontier empty, failure
            return

        # using priority queue for UCS
        frontier_get = frontier.get()
        (parent_weight, current_node) = frontier_get
        
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

            # directions are in reverse, flip the list. This is faster than prepending every time in native python
            directions.reverse()
            return directions
        

        explored.add(current_node)
        # unpack neighbor, direction, and path weight for each neighboring node
        for (neighbor, direction, weight) in problem.successorStates(current_node):
            if (neighbor not in frontier.queue) and (neighbor not in explored):
                #! Should i do parent weight to make decision based on total weight, or just which path is currently cheapest?
                frontier.put((weight + parent_weight + heuristic(neighbor, problem), neighbor))  # add neighbor and (path weight + parent weight + hueristic) to frontier
                # frontier.put((weight, neighbor))  # add neighbor and path weight to frontier
                # set neighbor's parent and parent->neighbor direction here
                # can also set path weight and use that to calculate the full path at the end
                parents[neighbor] = (current_node, direction)
