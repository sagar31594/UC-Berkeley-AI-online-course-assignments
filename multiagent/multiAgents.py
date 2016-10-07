# multiAgents.py
# --------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

class ReflexAgent(Agent):
    """
      A reflex agent chooses an action at each choice point by examining
      its alternatives via a state evaluation function.

      The code below is provided as a guide.  You are welcome to change
      it in any way you see fit, so long as you don't touch our method
      headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {North, South, West, East, Stop}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        #print scores
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best
        #print chosenIndex
        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
        oldGhostStates = currentGameState.getGhostStates()
        oldScaredTimes = [ghostState.scaredTimer for ghostState in oldGhostStates]
        
        "*** YOUR CODE HERE ***"
        oldPos = currentGameState.getPacmanPosition()
##        print successorGameState
##        print newPos
##        print newFood
##        print newGhostStates
##        print newScaredTimes
        foodCoordinates = newFood.asList()
        #foodCoordinates = currentGameState.getFood().asList()
        newGhostCoordinates = successorGameState.getGhostPositions()
        oldGhostCoordinates = currentGameState.getGhostPositions()
        remainingFood = len(foodCoordinates)
        #ghostCoordinates = currentGameState.getGhostPositions()
##        total = 0.0
##        for i in foodCoordinates:
##            total += manhattanDistance(newPos, i)
##        if len(foodCoordinates) != 0:    
##            dist = total/len(foodCoordinates)

        d = []
        for i in foodCoordinates:
            d.append(manhattanDistance(newPos, i))
        #print d    
        if len(d) != 0:    
            dist = sum(d)
            #print 'Dist: ', dist

        c = currentGameState.getCapsules()
##        print 'capsules ', c
##        print newPos
##        if newPos in c:
##            print newPos in c

        g = []
        ghostDist = 0
        for i in oldGhostCoordinates:
            g.append(manhattanDistance(oldPos, i))
        if len(g) != 0:
            ghostDist = min(g)

##        if ghostDist != 0 and ghostDist < 3:
##            gd = []
##            for i in newGhostCoordinates:
##                gd.append(manhattanDistance(newPos, i))
##            if len(gd) != 0:
##                return min(gd)
##        elif currentGameState.hasFood(newPos[0], newPos[1]):
##            return 2
##        else:
##            return 1.0/dist

        if sum(oldScaredTimes) == 0:
            if ghostDist != 0 and ghostDist < 3:
                gd = []
                for i in newGhostCoordinates:
                    gd.append(manhattanDistance(newPos, i))
                if len(gd) != 0:
                    return min(gd)
            elif newPos in c:
                return 3
            elif currentGameState.hasFood(newPos[0], newPos[1]):
                return 2
            else:
                return 1.0/dist
        else:
            gd = []
            for i in newGhostCoordinates:
                gd.append(manhattanDistance(newPos, i))
            if len(gd) != 0:
                dist = min(gd)
            if newPos in newGhostCoordinates:
                return 2
            else:
                return 1.0/dist

            
##        if sum(oldScaredTimes) == 0:
##            if newPos in ghostCoordinates:
##                print '-1'
##                return -1
##            elif newPos in c:
##                print '3'
##                return 3
##            elif currentGameState.hasFood(newPos[0], newPos[1]):
##                #print '2'
##                return 2
##            else:
##                #print '1/dist ', 1.0/dist
##                return 1.0/dist
##                #return 1.0/remainingFood
##        else:
##            g = []
##            for i in ghostCoordinates:
##                g.append(manhattanDistance(newPos, i))
##            if len(g) != 0:
##                dist = min(g)
##            if newPos in ghostCoordinates:
##                return 2
##            else:
##                return 1.0/dist
        
        return successorGameState.getScore()

def scoreEvaluationFunction(currentGameState):
    """
      This default evaluation function just returns the score of the state.
      The score is the same one displayed in the Pacman GUI.

      This evaluation function is meant for use with adversarial search agents
      (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
      This class provides some common elements to all of your
      multi-agent searchers.  Any methods defined here will be available
      to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

      You *do not* need to make any changes here, but you can if you want to
      add functionality to all your adversarial search agents.  Please do not
      remove anything, however.

      Note: this is an abstract class: one that should not be instantiated.  It's
      only partially specified, and designed to be extended.  Agent (game.py)
      is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)
        
#count = list()

class MinimaxAgent(MultiAgentSearchAgent):
    """
      Your minimax agent (question 2)
    """
    #count = list()

    def value(self, gameState, depth, n):
##        print 'depth ', depth
##        if depth == 0:
##            print '\nself.count: ', count, '\n'
        #depth %= gameState.getNumAgents()
##        if depth == 0:#gameState.getNumAgents() - 1:
##            self.count += 1
        actions = gameState.getLegalActions(depth % n)
##        print 'Actions: ', actions
##        print 'Count: ', count
        if len(actions) == 0 or depth == self.depth * n:
            return self.evaluationFunction(gameState)
        if depth % n == 0:
            return self.maxValue(gameState, depth, n)
        else:
            return self.minValue(gameState, depth, n)

    def maxValue(self, gameState, depth, n):
        v = -float('inf')
        actions = gameState.getLegalActions(depth % n)
        depth += 1
        vPrev = v
        chosenAction = None
        for action in actions:
            v = max(v, self.value(gameState.generateSuccessor((depth-1) % n, action), depth, n))
            if v != vPrev:
                chosenAction = action
                vPrev = v
        if depth - 1 == 0:
            return chosenAction
        return v

    def minValue(self, gameState, depth, n):
        v = float('inf')
##        global count
        actions = gameState.getLegalActions(depth % n)
##        if depth % n == gameState.getNumAgents() - 1 and depth not in count:
##            count.append(depth)
        depth += 1
        for action in actions:
            v = min(v, self.value(gameState.generateSuccessor((depth-1) % n, action), depth, n))
        return v
    
    def getAction(self, gameState):
        """
          Returns the minimax action from the current gameState using self.depth
          and self.evaluationFunction.

          Here are some method calls that might be useful when implementing minimax.

          gameState.getLegalActions(agentIndex):
            Returns a list of legal actions for an agent
            agentIndex=0 means Pacman, ghosts are >= 1

          gameState.generateSuccessor(agentIndex, action):
            Returns the successor game state after an agent takes an action

          gameState.getNumAgents():
            Returns the total number of agents in the game
        """
        "*** YOUR CODE HERE ***"
##        global count
##        print 'self.depth ', self.depth
##        print 'no of agents ', gameState.getNumAgents()
        action = self.value(gameState, 0, gameState.getNumAgents())
##        count = list()
##        print '\nself.count: ', count, '\n'
        return action
        
        util.raiseNotDefined()

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """
    def value(self, gameState, depth, n, alpha, beta):
##        print 'depth ', depth
##        if depth == 0:
##            print '\nself.count: ', count, '\n'
        #depth %= gameState.getNumAgents()
##        if depth == 0:#gameState.getNumAgents() - 1:
##            self.count += 1
        actions = gameState.getLegalActions(depth % n)
##        print 'Actions: ', actions
##        print 'Count: ', count
        if len(actions) == 0 or depth == self.depth * n:
            return self.evaluationFunction(gameState)
        if depth % n == 0:
            return self.maxValue(gameState, depth, n, alpha, beta)
        else:
            return self.minValue(gameState, depth, n, alpha, beta)

    def maxValue(self, gameState, depth, n, alpha, beta):
        v = -float('inf')
        actions = gameState.getLegalActions(depth % n)
        depth += 1
        vPrev = v
        chosenAction = None
        for action in actions:
            v = max(v, self.value(gameState.generateSuccessor((depth-1) % n, action), depth, n, alpha, beta))
            if v != vPrev:
                chosenAction = action
                vPrev = v
            if v > beta:
                return v
            alpha = max(alpha, v)
        if depth - 1 == 0:
            return chosenAction
        return v

    def minValue(self, gameState, depth, n, alpha, beta):
        v = float('inf')
##        global count
        actions = gameState.getLegalActions(depth % n)
##        if depth % n == gameState.getNumAgents() - 1 and depth not in count:
##            count.append(depth)
        depth += 1
        for action in actions:
            v = min(v, self.value(gameState.generateSuccessor((depth-1) % n, action), depth, n, alpha, beta))
            if v < alpha:
                return v
            beta = min(beta, v)
        return v

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
##        global count
##        print 'self.depth ', self.depth
##        print 'no of agents ', gameState.getNumAgents()
        action = self.value(gameState, 0, gameState.getNumAgents(), -float('inf'), float('inf'))
##        count = list()
##        print '\nself.count: ', count, '\n'
        return action

        util.raiseNotDefined()

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """
    
    def value(self, gameState, depth, n):
##        print 'depth ', depth
##        if depth == 0:
##            print '\nself.count: ', count, '\n'
        #depth %= gameState.getNumAgents()
##        if depth == 0:#gameState.getNumAgents() - 1:
##            self.count += 1
        actions = gameState.getLegalActions(depth % n)
##        print 'Actions: ', actions
##        print 'Count: ', count
        if len(actions) == 0 or depth == self.depth * n:
            return self.evaluationFunction(gameState)
        if depth % n == 0:
            return self.maxValue(gameState, depth, n)
        else:
            return self.expValue(gameState, depth, n)

    def maxValue(self, gameState, depth, n):
        v = -float('inf')
        actions = gameState.getLegalActions(depth % n)
        depth += 1
        vPrev = v
        chosenAction = None
        for action in actions:
            v = max(v, self.value(gameState.generateSuccessor((depth-1) % n, action), depth, n))
            if v != vPrev:
                chosenAction = action
                vPrev = v
        if depth - 1 == 0:
            return chosenAction
        return v

    def expValue(self, gameState, depth, n):
        #v = float('inf')
##        global count
        v = 0
        actions = gameState.getLegalActions(depth % n)
        probability = 1.0/len(actions)
##        if depth % n == gameState.getNumAgents() - 1 and depth not in count:
##            count.append(depth)
        depth += 1
        for action in actions:
            #v = min(v, self.value(gameState.generateSuccessor((depth-1) % n, action), depth, n))
            v += probability * self.value(gameState.generateSuccessor((depth-1) % n, action), depth, n)
        return v

    def getAction(self, gameState):
        """
          Returns the expectimax action using self.depth and self.evaluationFunction

          All ghosts should be modeled as choosing uniformly at random from their
          legal moves.
        """
        "*** YOUR CODE HERE ***"
##        global count
##        print 'self.depth ', self.depth
##        print 'no of agents ', gameState.getNumAgents()
        action = self.value(gameState, 0, gameState.getNumAgents())
##        count = list()
##        print '\nself.count: ', count, '\n'
        return action

        util.raiseNotDefined()

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    ghostStates = currentGameState.getGhostStates()
    food = currentGameState.getFood()
    pos = currentGameState.getPacmanPosition()
    scaredTimes = [ghostState.scaredTimer for ghostState in ghostStates]
    foodCoordinates = food.asList()
    ghostCoordinates = currentGameState.getGhostPositions()
    foodCount = len(foodCoordinates)

    d = []
    dist = 0
    for i in foodCoordinates:
        d.append(manhattanDistance(pos, i))
    if len(d) != 0:
        dist = sum(d)

    g = []
    ghostDist = 0
    for i in ghostCoordinates:
        g.append(manhattanDistance(pos, i))
    if len(g) != 0:
        ghostDist = min(g)

##    if sum(scaredTimes) == 0:
##        if ghostDist != 0 and ghostDist < 3:
##            #print '-1'
##            return ghostDist/10.0 + 20.0/foodCount
##        elif dist == 0:
##            return 1000
##        else:
##            #print 'Dist: ', dist
##            return 1.0/foodCount
##    else:
##        if ghostDist == 0:
##            return 1000
##        else:
##            return 100 + 1.0/ghostDist
    if sum(scaredTimes) == 0:
        if dist == 0:
            return 100
        else:
            return ghostDist/10.0 + 20.0/foodCount + 1.0/dist
            #return ghostDist/100.0 + 1.0/dist
    else:
        if ghostDist == 0:
            return 1000
        else:
            return 100 + 1.0/ghostDist
##    return 1.0/foodCount + 1.0/dist
##    if ghostDist > 3:
##        return 1.0/foodCount + 1.0/dist
##    else:
##        return -5 - ghostDist + 1.0/dist
    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction

