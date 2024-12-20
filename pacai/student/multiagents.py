import random

from pacai.agents.base import BaseAgent
from pacai.agents.search.multiagent import MultiAgentSearchAgent
from pacai.core import distance


class ReflexAgent(BaseAgent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.
    You are welcome to change it in any way you see fit,
    so long as you don't touch the method headers.
    """

    def __init__(self, index, **kwargs):
        super().__init__(index, **kwargs)

    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        `ReflexAgent.getAction` chooses among the best options according to the evaluation function.

        Just like in the previous project, this method takes a
        `pacai.core.gamestate.AbstractGameState` and returns some value from
        `pacai.core.directions.Directions`.
        """

        # Collect legal moves.
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions.
        scores = [self.evaluationFunction(
            gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(
            len(scores)) if scores[index] == bestScore]
        # Pick randomly among the best.
        chosenIndex = random.choice(bestIndices)

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current `pacai.bin.pacman.PacmanGameState`
        and an action, and returns a number, where higher numbers are better.
        Make sure to understand the range of different values before you combine them
        in your evaluation function.
        """

        successorGameState = currentGameState.generatePacmanSuccessor(action)

        # Useful information you can extract.
        newPosition = successorGameState.getPacmanPosition()
        newScore = successorGameState.getScore()
        oldScore = currentGameState.getScore()
        # newFood = successorGameState.getFood()
        newFoodList = successorGameState.getFood().asList()
        newGhostStates = successorGameState.getGhostStates()

        # print("newFood: ", newFood)

        # Get the shorest distance to a ghost, bigger is better
        # Farther is better, squares each maze distance to pre
        closestGhost = float('inf')
        for newGhostState in newGhostStates:
            newGhostStatePos = newGhostState.getNearestPosition()
            ghostDistanceToPac = distance.manhattan(
                newPosition, newGhostStatePos)
            if closestGhost > ghostDistanceToPac:
                closestGhost = ghostDistanceToPac

        # # Get total squares on grid
        # totalSquares = 0
        # for row in newFood:
        #     for col in row:
        #         totalSquares += 1

        # Get total food amounts, less is better
        totalFoodCount = 0
        foodDistToPac = 0
        closestFoodDist = float('inf')
        for foodCoord in newFoodList:
            totalFoodCount += 1
            # foodDistToPac = distance.maze(
            #     newPosition, foodCoord, currentGameState)
            foodDistToPac = distance.manhattan(
                newPosition, foodCoord)
            if closestFoodDist > foodDistToPac:
                closestFoodDist = foodDistToPac

        if totalFoodCount == 0:
            totalFoodCount = 1
            closestFoodDist = -float('inf')

        # Takes ~80 seconds to play, ~8/10 wins
        # eval = 5*(newScore-oldScore) - 50*(totalFoodCount) - 3 * closestFoodDist

        # Takes ~70 seconds to play 10/10 wins
        eval = 4 * (newScore - oldScore) + int(closestGhost / 2) - \
            5 * (totalFoodCount) - closestFoodDist

        # Takes ~65 seconds, 9/10 wins
        # eval = int(closestGhost/3) - 4*(totalFoodCount) - 6*closestFoodDist

        # print("totalFoodCount: ", totalFoodCount)
        # print("foodDistToPac: ", foodDistToPac)
        # print("eval: ", eval)
        # print("newScore: ", newScore)
        # print("newPosition: ", newPosition)
        # print("totalSquares: ", totalSquares)
        # print("totalFoodCount: ", totalFoodCount)
        # print("closestGhost: ", closestGhost)

        return eval


class MinimaxAgent(MultiAgentSearchAgent):
    """
    A minimax agent.

    Here are some method calls that might be useful when implementing minimax.

    `pacai.core.gamestate.AbstractGameState.getNumAgents()`:
    Get the total number of agents in the game

    `pacai.core.gamestate.AbstractGameState.getLegalActions`:
    Returns a list of legal actions for an agent.
    Pacman is always at index 0, and ghosts are >= 1.

    `pacai.core.gamestate.AbstractGameState.generateSuccessor`:
    Get the successor game state after an agent takes an action.

    `pacai.core.directions.Directions.STOP`:
    The stop direction, which is always legal, but you may not want to include in your search.

    Method to Implement:

    `pacai.agents.base.BaseAgent.getAction`:
    Returns the minimax action from the current gameState using
    `pacai.agents.search.multiagent.MultiAgentSearchAgent.getTreeDepth`
    and `pacai.agents.search.multiagent.MultiAgentSearchAgent.getEvaluationFunction`.
    """

    def __init__(self, index, **kwargs):
        super().__init__(index, **kwargs)

    def getAction(self, state):
        (action, cost) = self._minimax(0, 0, state)
        return action

    def _minimax(self, agentNum, currDepth, state):
        # We hit max depth!
        if currDepth == self.getTreeDepth() or state.isLose() or state.isWin():
            return ('Stop', self.getEvaluationFunction()(state))

        bestActionMMValue = None
        bestAction = None
        nextAgentNum = agentNum + 1
        agentsLegalActions = state.getLegalActions(agentNum)
        if agentNum == 0:  # max, pac!
            bestActionMMValue = -float('inf')
            for action in agentsLegalActions:
                if action == 'Stop':
                    continue
                actionMMValue = self._minimax(nextAgentNum, currDepth,
                                        state.generateSuccessor(agentNum, action))[1]
                # print("action, actionMMValue: ", (action, actionMMValue))
                if actionMMValue > bestActionMMValue:
                    bestActionMMValue = actionMMValue
                    bestAction = action
        else:  # min, not pacman
            if nextAgentNum == state.getNumAgents():
                nextAgentNum = 0  # maxs turn
                currDepth += 1  # all agents have gone, increment depth

            bestActionMMValue = float('inf')
            for action in agentsLegalActions:
                if action == 'Stop':
                    continue
                actionMMValue = self._minimax(nextAgentNum, currDepth,
                                        state.generateSuccessor(agentNum, action))[1]
                if actionMMValue < bestActionMMValue:
                    bestActionMMValue = actionMMValue
                    bestAction = action

        return (bestAction, bestActionMMValue)


class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    A minimax agent with alpha-beta pruning.

    Method to Implement:

    `pacai.agents.base.BaseAgent.getAction`:
    Returns the minimax action from the current gameState using
    `pacai.agents.search.multiagent.MultiAgentSearchAgent.getTreeDepth`
    and `pacai.agents.search.multiagent.MultiAgentSearchAgent.getEvaluationFunction`.
    """

    def __init__(self, index, **kwargs):
        super().__init__(index, **kwargs)
    
    def getAction(self, state):
        (action, cost) = self._minimax(0, 0, state, -float('inf'), float('inf'))
        return action

    def _minimax(self, agentNum, currDepth, state, alpha, beta):
        # We hit max depth!
        if currDepth == self.getTreeDepth() or state.isLose() or state.isWin():
            return ('Stop', self.getEvaluationFunction()(state))

        bestActionMMValue = None
        bestAction = None
        nextAgentNum = agentNum + 1
        agentsLegalActions = state.getLegalActions(agentNum)
        if agentNum == 0:  # max, pac!
            bestActionMMValue = -float('inf')
            for action in agentsLegalActions:
                if action == 'Stop':
                    continue
                actionMMValue = self._minimax(nextAgentNum, currDepth,
                                        state.generateSuccessor(agentNum, action), alpha, beta)[1]
                # print("action, actionMMValue: ", (action, actionMMValue))
                if actionMMValue > bestActionMMValue:
                    bestActionMMValue = actionMMValue
                    bestAction = action
                
                # alpha-beta pruning!
                if bestActionMMValue >= beta:
                    return (bestAction, bestActionMMValue)
                alpha = max(alpha, bestActionMMValue)
                
        else:  # min, not pacman
            if nextAgentNum == state.getNumAgents():
                nextAgentNum = 0  # max's turn
                currDepth += 1  # all agents have gone, increment depth

            bestActionMMValue = float('inf')
            for action in agentsLegalActions:
                if action == 'Stop':
                    continue
                actionMMValue = self._minimax(nextAgentNum, currDepth,
                                        state.generateSuccessor(agentNum, action), alpha, beta)[1]
                if actionMMValue < bestActionMMValue:
                    bestActionMMValue = actionMMValue
                    bestAction = action
                
                # alpha-beta pruning!
                if bestActionMMValue <= alpha:
                    return (bestAction, bestActionMMValue)
                beta = max(beta, bestActionMMValue)

        return (bestAction, bestActionMMValue)


class ExpectimaxAgent(MultiAgentSearchAgent):
    """
    An expectimax agent.

    All ghosts should be modeled as choosing uniformly at random from their legal moves.

    Method to Implement:

    `pacai.agents.base.BaseAgent.getAction`:
    Returns the expectimax action from the current gameState using
    `pacai.agents.search.multiagent.MultiAgentSearchAgent.getTreeDepth`
    and `pacai.agents.search.multiagent.MultiAgentSearchAgent.getEvaluationFunction`.
    """

    def __init__(self, index, **kwargs):
        super().__init__(index, **kwargs)
    
    def getAction(self, state):
        (action, cost) = self._minimax(0, 0, state)
        return action

    def _minimax(self, agentNum, currDepth, state):
        # We hit max depth!
        if currDepth == self.getTreeDepth() or state.isLose() or state.isWin():
            return ('Stop', self.getEvaluationFunction()(state))

        bestActionMMValue = None
        bestAction = None
        nextAgentNum = agentNum + 1
        agentsLegalActions = state.getLegalActions(agentNum)
        if agentNum == 0:  # max, pac!
            bestActionMMValue = -float('inf')
            for action in agentsLegalActions:
                if action == 'Stop':
                    continue
                actionMMValue = self._minimax(nextAgentNum, currDepth,
                                        state.generateSuccessor(agentNum, action))[1]
                if actionMMValue > bestActionMMValue:
                    bestActionMMValue = actionMMValue
                    bestAction = action
        else:  # chance, not pacman
            if nextAgentNum == state.getNumAgents():
                nextAgentNum = 0  # maxs turn
                currDepth += 1  # all agents have gone, increment depth

            bestActionMMValue = 0
            numActions = 0
            for action in agentsLegalActions:
                if action == 'Stop':
                    continue
                numActions += 1
                actionMMValue = self._minimax(nextAgentNum, currDepth,
                                        state.generateSuccessor(agentNum, action))[1]
                bestActionMMValue += actionMMValue
            # get average
            bestActionMMValue /= numActions

        return (bestAction, bestActionMMValue)


def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable evaluation function.

    DESCRIPTION: <write something here so we know what you did>
    """
    position = currentGameState.getPacmanPosition()
    score = currentGameState.getScore()
    foodList = currentGameState.getFood().asList()
    ghostStates = currentGameState.getGhostStates()

    # Get the shorest distance to a ghost, bigger is better
    # Farther is better, squares each maze distance to pre
    closestGhost = float('inf')
    for newGhostState in ghostStates:
        newGhostStatePos = newGhostState.getNearestPosition()
        # ghostDistanceToPac = distance.maze(
        #     position, newGhostStatePos, currentGameState)
        ghostDistanceToPac = distance.manhattan(
            position, newGhostStatePos)
        if closestGhost > ghostDistanceToPac:
            closestGhost = ghostDistanceToPac

    # Get total food amounts, less is better
    totalFoodCount = 0
    foodDistToPac = 0
    closestFoodDist = float('inf')
    for foodCoord in foodList:
        totalFoodCount += 1
        # foodDistToPac = distance.maze(
        #     position, foodCoord, currentGameState)
        foodDistToPac = distance.manhattan(
            position, foodCoord)
        if closestFoodDist > foodDistToPac:
            closestFoodDist = foodDistToPac

    if totalFoodCount == 0:
        totalFoodCount = 1
        closestFoodDist = -float('inf')

    # Takes ~70 seconds to play 10/10 wins
    eval = 4 * score + int(closestGhost / 2) - 5 * (totalFoodCount) - closestFoodDist
    # eval = 4 * score - 5 * (totalFoodCount) - closestFoodDist
    return eval


class ContestAgent(MultiAgentSearchAgent):
    """
    Your agent for the mini-contest.

    You can use any method you want and search to any depth you want.
    Just remember that the mini-contest is timed, so you have to trade off speed and computation.

    Ghosts don't behave randomly anymore, but they aren't perfect either -- they'll usually
    just make a beeline straight towards Pacman (or away if they're scared!)

    Method to Implement:

    `pacai.agents.base.BaseAgent.getAction`
    """

    def __init__(self, index, **kwargs):
        super().__init__(index, **kwargs)
