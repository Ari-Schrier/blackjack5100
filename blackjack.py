import random

"""
Contains functions needed for blackjack
"""
class BlackJack:
	def __init__(self, observations = None, deck = None, action = None):
		if deck == None:
			oneDeck = [2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10, 11, 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10, 11, 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10, 11, 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10, 11]
			self.deck = oneDeck + oneDeck + oneDeck + oneDeck #Hacky way of putting together a shoe of cards
			for i in range(0, random.randint(0, 155)):
				#To simulate a game in progress
				self.deck.pop()
		else:
			self.deck = deck
		random.shuffle(self.deck)
		self.reward = 0
		if observations:
			self.player = observations[0]
			self.dealer = observations[1]
			self.playerAce = observations[2]
			self.dealerAce = observations[3]
		else:
			self.playerAce = False
			self.dealerAce = False
			self.player = self.dealCard() + self.dealCard()
			self.dealer = self.dealCard(False)
			self.dealerAce = False
		self.terminal = False	

	def analyzeGame(self):
		if self.player > 21:
			print("Busted!")
		elif self.player == 21:
			print("Blackjack!")
		elif self.player > self.dealer:
			print("Player won!")
		elif self.dealer > self.player:
			print("House wins.")
		elif self.dealer == self.player:
			print("Tie")
		else:
			print("Something odd happened")
		
	def defineState(self):
		print(f"Time for a game of blackjack! I have {self.player} in my hand. The dealer has {self.dealer}.")
		if self.terminal:
			print("Also, I'm terminal!")
		print(self.deck)
			
	def dealCard(self, isPlayer = True):
		if len(self.deck) < 52:
			#Standard casino rules. Once we're down to about a deck's worth of cards, everything gets shuffled together
			oneDeck = [2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10, 11, 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10, 11, 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10, 11, 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10, 11]
			self.deck = oneDeck + oneDeck + oneDeck + oneDeck
			random.shuffle(self.deck)
		dealt = self.deck[0]
		self.deck = self.deck[1:]
		if dealt == 11:
			if isPlayer:
				self.playerAced = True
			else:
				self.dealerAced = True
		return dealt
	
	def getLegalActions(self):
		if self.player < 21:
			return[0, 1]
		return[0]
		
	def isGameOver(self):
		return self.terminal
		
	def gameResult(self):
		return self.reward
	
	def move(self, action):
		observations = [self.player, self.dealer, self.playerAce, self.dealerAce]
		newDeck = self.deck[:]
		newState = BlackJack(observations, newDeck , action)
		newState.handle(action)
		return newState
		
	def handle(self, action):
		if action == 0:
			self.terminal = True
			if self.player > 21:
				self.reward = -1
			elif self.player == self.dealer:
				self.reward = 0
			elif self.player == 21:
				self.reward = 1
			else:
				while self.dealer < 17:
					self.dealer += self.dealCard(False)
					if self.dealer > 21 and self.dealerAce:
						self.dealer -= 10
						self.dealerAce = False
				if self.dealer > 21:
					self.reward = 1
				elif self.player > self.dealer:
					self.reward = 1
				elif self.dealer > self.player:
					self.reward = -1
				else:
					self.reward = 0
		if action == 1:
			self.terminal = False
			self.player += self.dealCard()
			if self.player > 21 and self.playerAce:
				self.playerAce = False
				self.player -= 10
			
				
			
