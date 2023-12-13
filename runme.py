import monteCarlo
import blackjack
import random
import reflexAgent

def runGame():
	env = blackjack.BlackJack()
	terminated = False
	while not terminated:
		action = monteCarlo.fullMonte(env)
		#action = random.choice([0, 1])
		#action = reflexAgent.chooseAction(env)
		env = env.move(action)
		terminated = env.isGameOver()
	#env.analyzeGame()
	return env.reward

def runGames(gamesToPlay):
	wins = 0
	ties = 0
	losses = 0
	for i in range(gamesToPlay):
		env = blackjack.BlackJack()
		if i % 1000 == 0:
			print(f"{i}/{gamesToPlay}")
		reward = runGame()
		if reward > 0:
			wins += 1
		if reward == 0:
			ties += 1
		if reward < 0:
			losses += 1
	print(f"Played {gamesToPlay} rounds of blackjack.\nTotal wins: {wins}\nTotal ties: {ties}\nTotal losses: {losses}")
	
runGames(10000)
