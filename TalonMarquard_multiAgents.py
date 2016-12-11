# multiAgents.py
# --------------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# For more info, see http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html

from util import manhattanDistance
from game import Directions
import random, util
from game import Agent
from util import Stack
from util import Queue

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
    to the MinimaxPacmanAgent and AlphaBetaPacmanAgent.

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
    "*** YOUR CODE HERE IF YOU WANT TO ***"
    "*** RELEVANT FOR QUESTIONS 3 AND 4***"


class MinimaxAgent(MultiAgentSearchAgent):
  """
    Your minimax agent (question 1)
  """

  def getAction(self, gameState):
    
    """
      Returns the minimax action from the current gameState using self.depth
      and self.evaluationFunction.

      Here are some method calls that might be useful when implementing minimax.

      gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1

      Directions.STOP:
        The stop direction, which is always legal, unless the game has ended

      gameState.generateSuccessor(agentIndex, action):
        Returns the successor game state after an agent takes an action

      gameState.getNumAgents():
        Returns the total number of agents in the game
    """
    "*** YOUR CODE HERE ***"
    #print "depth", self.depth
    #print "eval func: ", self.evaluationFunction
    #print "Actions: ", gameState.getLegalActions(0)
    #print "Successor: ", gameState.generateSuccessor(0, Directions.STOP)
    #print "number: ", gameState.getNumAgents()

    bestMove = []
    successors = []
    player = 0
    hScore = -100000
    actions = gameState.getLegalActions(player)
    
    for action in actions:
      successors.append([action, gameState.generateSuccessor(player, action)])
    for successor in successors:
      score = MinValue(player + 1, self.depth, self, successor[1])
      if (score > hScore):
        hScore = score
        
        bestMove = successor[0]
    return bestMove
    
  


def MaxValue(player, depth, self, gameState):

  if depth <= 0 or gameState.isWin() == True or gameState.isLose() == True:
    return self.evaluationFunction(gameState)
  
  
  hScore = -1000000
  
  actions = gameState.getLegalActions(0)
  successors = []

  for action in actions:
    successors.append(gameState.generateSuccessor(0, action))
  for successor in successors:
    score = MinValue(player + 1,depth, self, successor)
    if (score > hScore):
      hScore = score
    
      
  return hScore            

def MinValue(player, depth, self, gameState):
  "min"
  lScore = 1000000
  successors = []
  actions = gameState.getLegalActions(player)
  i = 1
  
  for action in actions:
    successors.append(gameState.generateSuccessor(player, action))
  for successor in successors:
      
    if player == gameState.getNumAgents() - 1:
      score = MaxValue(0,(depth - 1), self, successor)
      if score < lScore:
        lScore = score
        
    else:
      score = MinValue(player + 1, depth, self, successor)
      if score < lScore:
        lScore = score
  if lScore == 1000000:
    lScore = self.evaluationFunction(gameState)
      
  return lScore


      
  


class AlphaBetaAgent(MultiAgentSearchAgent):
  """
    Your minimax agent with alpha-beta pruning (question 2)
  """

  def getAction(self, gameState):
    """
      Returns the minimax action using self.depth and self.evaluationFunction
    """
    "*** YOUR CODE HERE ***"
    bestMove = []
    successors = []
    player = 0
    hScore = float("-inf")
    alpha = float("-inf")
    beta = float("inf")
    actions = gameState.getLegalActions(player)
    for action in actions:
      successor = gameState.generateSuccessor(player,action)
      score = MinValueAB(player + 1, self.depth, self, successor, alpha, beta)
      if (score > hScore):
        hScore = score
        bestMove = action
      if hScore > beta:
        return bestMove
      alpha = max(hScore, alpha)
      
    return bestMove
    
  


def MaxValueAB(player, depth, self, gameState, alpha, beta):

  if depth <= 0 or gameState.isWin() == True or gameState.isLose() == True:
    return self.evaluationFunction(gameState)
  
  
  hScore = float("-inf")
  
  actions = gameState.getLegalActions(0)
  successors = []

  for action in actions:
    successor = gameState.generateSuccessor(0, action)
    score = MinValueAB(player + 1,depth, self, successor, alpha, beta)
    hScore = max(hScore, score)
    if hScore >= beta:
      return hScore
    alpha = max(alpha, hScore)
  return hScore            

def MinValueAB(player, depth, self, gameState, alpha, beta):
  "min"
  lScore = float("inf")
  successors = []
  actions = gameState.getLegalActions(player)
  i = 1
  
  for action in actions:
    successor = gameState.generateSuccessor(player, action)
      
    if player == gameState.getNumAgents() - 1:
      score = MaxValueAB(0,(depth - 1), self, successor, alpha, beta)
      lScore = min(score, lScore)
      if lScore <= alpha:
        return lScore
      beta = min(beta, lScore)
        
    else:
      score = MinValueAB(player + 1, depth, self, successor, alpha, beta)
      lScore = min(score, lScore)
      if lScore <= alpha:
        return lScore
      beta = min(beta, lScore)
      
      
  if lScore == float("inf"):
    lScore = self.evaluationFunction(gameState)
      
  return lScore


previousPlaces = []
def betterEvaluationFunction(currentGameState):
  """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 3).

    You can store some additional information in a game-state using the 
    customData dictionairy. You can store this information in the getAction
    function and retrieve it here. Note that all data will be reset
    the next time getAction is called, so if your data has to be persistent
    between calls to getAction you will have to store the data in your
    search agent and then initialize the dictionairy for every call of
    getAction.

    Also note that a deep copy of the dictionairy is created for every
    call to getSuccessor, meaning that stroring large data structures in
    the dictionairy might make you code really slow. For data that should
    be initialized once and never be altered you might want to consider 
    storing in it a global variable and setting it only the first time
    getAction gets called.

    To store data in the customData dictionairy:
    currentGameState.customData['myData'] = thisIsMyData

    To get data from the customData dictionairy:
    retreivedData = currentGameState.customData['myData']

    Also, do not forget you can set some variables in the __init__ function
    of the MultiAgentSearchAgent and that your agents should still work
    on the problems provided by the autograder.
  """
  "*** YOUR CODE HERE ***"
  win = 0
  lose = 0
  still = 0
  foodDist = float("inf")
  foodVal = 0
  capsuleDist = 0
  GhostVal = float("inf")
  foods = currentGameState.getFood()
  foodList = foods.asList()
  attack = False
  pacPos = currentGameState.getPacmanPosition()
  num = currentGameState.getNumAgents()
  ghostPos = currentGameState.getGhostPositions()

  
  foodVal = len(foodList)
  for food in foodList:
    temp = abs(food[0] - pacPos[0]) + abs(food[1] - pacPos[1])
    
    if temp < foodDist:
      foodDist = temp
      #print foodDist
  for ghost in ghostPos:
    temp = abs(ghost[0] - pacPos[0]) + abs(ghost[1] - pacPos[1])
    if GhostVal > temp:
      GhostVal = temp
    if temp == 0:
      lose = -10000

  if GhostVal > 2:
    GhostVal = 0
    

  if len(previousPlaces) != 0:
    if pacPos == previousPlaces[len(previousPlaces) - 1]:
      still = 1000
  
  previousPlaces.append(pacPos)
  score = currentGameState.getScore() 
    
  if len(foodList) == 0:
    win = 10000
    foodDist = 0
  return -10 * foodDist - 1000 * foodVal + 100*GhostVal + win + lose - still + score
  
 

# Abbreviation
better = betterEvaluationFunction

class UltimateAgent(MultiAgentSearchAgent):
  """
    The best agent you can think of (question 4).
  """

  def getAction(self, gameState):
    """
      Returns an action.  You can use any method you want and search to any depth you want.
      Just remember that the excercise is timed, so you have to trade off speed and computation.

      Ghosts don't behave randomly anymore, but they aren't perfect either -- they'll usually
      just make a beeline straight towards Pacman (or away from him if they're scared!)
    """
    "*** YOUR CODE HERE ***"
    pass


