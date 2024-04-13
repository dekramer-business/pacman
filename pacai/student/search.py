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

    print("Start: %s" % (str(problem.startingState())))
    print("Is the start a goal?: %s" % (problem.isGoal(problem.startingState())))
    print("Start's successors: %s" % (problem.successorStates(problem.startingState())))

    # *** Your Code Here ***
    if problem.isGoal(problem.startingState()):
        return []
    
    frontier = [problem.startingState()]  # stack for DFS
    explored = set()
    parents = {}
    solution = []

    while True:
        if len(frontier) == 0:  # if frontier empty, failure
            return

        current_node = frontier.pop()
        
        if problem.isGoal(current_node):
            print("Goal state: %s" % (str(current_node)))
            # print("Explored: %s" % (explored))
            print("Parents: %s" % (parents))

            list_thang = []
            curr = current_node
            while curr != None:
                list_thang.append(curr)
                curr = parents.get(curr)
            
            print("list_thang: %s" % (list_thang))

            return explored
        
        explored.add(current_node)

        # starts left, could be reversed
        for (neighbor, direction, weight) in problem.successorStates(current_node):
            # print("%s's Neighbor: %s" % (current_node, neighbor))
            if (neighbor not in frontier) and (neighbor not in explored):
                frontier.append(neighbor)
                parents[neighbor] = current_node
                # parents[neighbor] = direction



    # raise NotImplementedError()

def breadthFirstSearch(problem):
    """
    Search the shallowest nodes in the search tree first. [p 81]
    """

    # *** Your Code Here ***
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
