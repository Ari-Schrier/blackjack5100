import numpy as np
import random
import reflexAgent
import copy

"""
Contains various classes needed to run monte carlo tree search
I took a lot of inspiration for my implementation from this tutorial:
https://ai-boson.github.io/mcts/
"""

#Set hyperparams here
CVALUE = 0.25
SIMULATIONSTORUN = 150

class MonteCarloTreeSearchNode():
	def __init__(self, state, parent=None, parentAction=None):
		self.state = state
		self.parent = parent
		self.parentAction = parentAction
		self.children = []
		self.timesVisited = 0
		self.wins = 0
		self.losses = 0
		self.untriedActions = [0, 1] #0 = stay, 1 = hit
		
	"""
	Expand explores an action that hasn't been tried yet, and uses it
	to generate a new node which is appended to our children.
	"""
	def expand(self):
		action = self.untriedActions.pop()
		nextState = self.state.move(action)
		childNode = MonteCarloTreeSearchNode(
			nextState, parent=self, parentAction=action)
		self.children.append(childNode)
		return childNode

	"""
	rollout plays out a game based off of the rollout policy until the
	game is over.
	"""
	def rollout(self):
		currentState = self.state
		while not currentState.isGameOver():
			possibleMoves = currentState.getLegalActions()
			action = self.rolloutPolicy(possibleMoves)
			currentState = currentState.move(action)
		return currentState.gameResult()

	"""
	backpropagate goes back up the tree, applying the result of the sim
	to all parents of a node 
	"""
	def backpropagate(self, result):
		self.timesVisited += 1.
		if result > 0:
			self.wins += 1
		elif result < 0:
			self.losses += 1
		if self.parent:
			self.parent.backpropagate(result)
	
	"""
	getBestChild finds the child of the current node with the highest weighted value
	"""
	def getBestChild(self, cValue):
		bestValue = float("-inf")
		bestNode = 2
		for each in self.children:
			childValue = (each.wins - each.losses / each.timesVisited) + (cValue * np.sqrt((np.log(self.timesVisited) / each.timesVisited)))
			if childValue > bestValue:
				bestValue = childValue
				bestNode = each
				
		#if cValue == 0:    
			#print("Selected", each.parentAction, "with value", bestValue)
		return each
			
		
		#choicesWeights is propagated using UCB formula
		choicesWeights = [(c.wins-c.losses / c.timesVisited) + 
		cValue * np.sqrt((2 * np.log(self.timesVisited) / c.timesVisited)
		) for c in self.children]
		if len(choicesWeights) == 2 and choicesWeights[0] == choicesWeights[1]:
			#To avoid argmax always making the same choice when both weights are equal
			return random.choice(self.children)
		"""
		if cValue == 0:
			print(choicesWeights[1])
			best = np.argmax(choicesWeights)
			print("Best child identified as", best)
		"""
		return self.children[np.argmax(choicesWeights)]
	
	"""
	alwaysExploreRandom foregoes UCB entirely and just picks a random child note to look at
	"""
	def alwaysExploreRandom(self):
		return random.choice(self.children)
	
	"""
	rolloutPolicy decides a move when we don't have information on our
	options from a node. Commenting out the first line changes the policy
	to be based on our reflex agent
	"""
	def rolloutPolicy(self, possibleMoves):
		return random.choice(possibleMoves)
		#Keeping this second version for posterity, but it doesn't
		#perform as well as a completely random choice
		if len(possibleMoves) < 2:
			return 0
		return reflexAgent.chooseAction(self.state)
		
	
	"""
	treePolicy tries to expand first, then prefers higher-value nodes
	"""
	def treePolicy(self):
		currentNode = self
		while not currentNode.state.isGameOver():
			if not currentNode.untriedActions == []:
				return currentNode.expand()
			else:
				#currentNode = currentNode.alwaysExploreRandom()
				#Always explore random didn't lead to any better results, if slightly worse results, than getBestChild
				currentNode = currentNode.getBestChild(CVALUE)
		return currentNode

	"""
	bestAction can be called on a node to find the action with the
	best expected value
	"""
	def bestAction(self):
		for i in range(SIMULATIONSTORUN):
			v = self.treePolicy()
			reward = v.rollout()
			v.backpropagate(reward)
		#Debugging block
		"""
		print("\nFinding best action")
		for each in self.children:
			print("Found a child from action: ", each.parentAction)
			print("Child's value was", (each.wins-each.losses) / each.timesVisited)
			print(f"Out of {each.timesVisited} tests")
		"""
		return self.getBestChild(0)
		
	"""
	fullMonte should be called on a gamestate to get back the best action
	"""
def fullMonte(initial_state):
	root = MonteCarloTreeSearchNode(initial_state)
	selected_node = root.bestAction()
	return selected_node.parentAction




