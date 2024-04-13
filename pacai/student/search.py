"""
In this file, you will implement generic search algorithms which are called by Pacman agents.
"""

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
    
    frontier = [problem.startingState()]  # stack for DFS
    explored = set()  # init empty set
    parents = {}

    while True:
        if len(frontier) == 0:  # if frontier empty, failure
            return

        # using stack for DFS
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
                frontier.append(neighbor)  # add neighbor to frontier
                # set neighbor's parent and parent->neighbor direction here
                # can also set path weight and use that to calculate the full path at the end
                parents[neighbor] = (current_node, direction)


def breadthFirstSearch(problem):
    """
    Search the shallowest nodes in the search tree first. [p 81]
    """

    # *** Your Code Here ***
    if problem.isGoal(problem.startingState()):
        return []
    
    frontier = [problem.startingState()]  # queue for BFS
    explored = set()  # init empty set
    parents = {}

    while True:
        if len(frontier) == 0:  # if frontier empty, failure
            return

        # using queue for BFS
        current_node = frontier.pop(0)
        
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
                frontier.append(neighbor)  # add neighbor to frontier
                # set neighbor's parent and parent->neighbor direction here
                # can also set path weight and use that to calculate the full path at the end
                parents[neighbor] = (current_node, direction)
    raise NotImplementedError()

def uniformCostSearch(problem):
    """
    Search the node of least total cost first.
    """

    # *** Your Code Here ***
    raise NotImplementedError()

def aStarSearch(problem, heuristic):
    """
    Search the node that has the lowest combined cost and heuristic first.
    """

    # *** Your Code Here ***
    raise NotImplementedError()
