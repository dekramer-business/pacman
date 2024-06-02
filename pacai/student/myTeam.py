from pacai.util import reflection
from pacai.agents.capture.reflex import ReflexCaptureAgent
from pacai.core.directions import Directions
from pacai.core import distance
from pacai.core.actions import Actions
from pacai.core.search import search
from pacai.student.searchAgents import AnyFoodSearchProblem


class BetterDefensiveReflexAgent(ReflexCaptureAgent):
    """
    A reflex agent that tries to keep its side Pacman-free.
    This is to give you an idea of what a defensive agent could be like.
    It is not the best or only way to make such an agent.
    """

    def __init__(self, index, **kwargs):
        super().__init__(index)

    def getFeatures(self, gameState, action):
        features = {}

        successor = self.getSuccessor(gameState, action)
        myState = successor.getAgentState(self.index)
        myPos = myState.getPosition()

        # Computes whether we're on defense (1) or offense (0).
        features['onDefense'] = 1
        if (myState.isPacman()):
            features['onDefense'] = 0

        # Computes distance to invaders we can see.
        enemies = [successor.getAgentState(i) for i in self.getOpponents(successor)]
        invaders = [a for a in enemies if a.isPacman() and a.getPosition() is not None]
        features['numInvaders'] = len(invaders)

        if (len(invaders) > 0):
            dists = [self.getMazeDistance(myPos, a.getPosition()) for a in invaders]
            features['invaderDistance'] = min(dists)
    
        enemyDists = [self.getMazeDistance(myPos, a.getPosition()) for a in enemies]
        features['enemyDistance'] = min(enemyDists)

        if (action == Directions.STOP):
            features['stop'] = 1

        rev = Directions.REVERSE[gameState.getAgentState(self.index).getDirection()]
        if (action == rev):
            features['reverse'] = 1
        
        return features

    def getWeights(self, gameState, action):
        return {
            'numInvaders': -1000,
            'onDefense': 100,
            'invaderDistance': -15,
            'stop': -100,
            'reverse': -2,
            'enemyDistance': -5
        }
    
class BetterOffensiveReflexAgent(ReflexCaptureAgent):
    """
    A reflex agent that seeks food.
    This agent will give you an idea of what an offensive agent might look like,
    but it is by no means the best or only way to build an offensive agent.
    """

    def __init__(self, index, **kwargs):
        super().__init__(index)

    def getFeatures(self, gameState, action):
        features = {}
        successor = self.getSuccessor(gameState, action)
        features['successorScore'] = self.getScore(successor)
        # print("succScore: ", features['successorScore'])
        myState = gameState.getAgentState(self.index)
        myPos = myState.getPosition()
        myNextState = successor.getAgentState(self.index)
        myNextPos = myNextState.getPosition()
        # Compute the location of pacman after he takes the action.
        x, y = myPos
        dx, dy = Actions.directionToVector(action)
        next_x, next_y = int(x + dx), int(y + dy)
        walls = gameState.getWalls()

        # Compute distance to the nearest food.
        food = self.getFood(gameState)
        foodList = food.asList()

        # This should always be True, but better safe than sorry.
        if (len(foodList) > 0):
            # myPos = successor.getAgentState(self.index).getPosition()
            minDistance = min([self.getMazeDistance(myNextPos, food) for food in foodList])
            minDistanceNormalized = float(minDistance) / (walls.getWidth() * walls.getHeight())
            features['distanceToFood'] = minDistanceNormalized
        
        # Farther is better, squares each maze distance to pre
        enemies = [successor.getAgentState(i) for i in self.getOpponents(successor)]
        enemyGhostsPos = [a.getNearestPosition() for a in enemies if not a.isPacman() and a.getPosition() is not None]

        # # Get distance to closest ghost
        # closestGhost = float('inf')
        # for newGhostPos in enemyGhostsPos:
        #     ghostDistanceToPac = self.getMazeDistance(
        #         myPos, newGhostPos)
        #     if closestGhost > ghostDistanceToPac:
        #         closestGhost = ghostDistanceToPac
        
        # closestGhostNormalized = float(closestGhost) / (walls.getWidth() * walls.getHeight())
        # features["closest-enemy-ghost"] = closestGhostNormalized

        # Count the number of ghosts 1-step away.
        features["#-of-ghosts-1-step-away"] = sum((next_x, next_y) in
                Actions.getLegalNeighbors(g, walls) for g in enemyGhostsPos)

        # If there is no danger of ghosts then add the food feature.
        if features["#-of-ghosts-1-step-away"] == 0 and food[next_x][next_y]:
            features['eats-food'] = 1

        
        # If there is no danger of ghosts then add the food feature.
        capsule = self.getCapsules(gameState)
        # print("capsule: ", capsule)
        # print("action: ", action)
        # print(" x and y: ", (x, y))
        # print(" next x and y: ", (next_x, next_y))
        for cap in capsule:
            if (next_x, next_y) == cap:
                features['eats-capsule'] = 1

        # features['bias'] = 1

        # Computes whether we're on Offense (1) or Defense (0).
        features['onOffense'] = -1
        if (myState.isPacman()):
            features['onOffense'] = 1

        # dont revers on our side!
        if features['onOffense'] == -1:
            rev = Directions.REVERSE[gameState.getAgentState(self.index).getDirection()]
            if (action == rev):
                features['reverse'] = 1
        
        if (action == Directions.STOP):
            features['stop'] = 1

        # print("features: ", features)
        return features

    def getWeights(self, gameState, action):
        return {
            'bias': 100,
            'successorScore': 20,  # may have to change this, 8 was based on losing a lot of score if you die
            'distanceToFood': -40,
            'closest-enemy-ghost': 2,
            # 'totalFoodCount': -10,
            'onOffense': 5,
            '#-of-ghosts-1-step-away': -300,
            'eats-food': 100,
            'eats-capsule': 150,
            'reverse': -1,
            'stop': -30
        }

def createTeam(firstIndex, secondIndex, isRed,
        first = BetterOffensiveReflexAgent,
        second = BetterDefensiveReflexAgent):
    """
    This function should return a list of two agents that will form the capture team,
    initialized using firstIndex and secondIndex as their agent indexed.
    isRed is True if the red team is being created,
    and will be False if the blue team is being created.
    """

    # firstAgent = reflection.qualifiedImport(first)
    # secondAgent = reflection.qualifiedImport(second)

    return [
        # firstAgent(firstIndex),
        # secondAgent(secondIndex),
        first(firstIndex),
        second(secondIndex)
    ]