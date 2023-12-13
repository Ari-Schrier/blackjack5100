def chooseAction(state):
	p = state.player
	d = state.dealer
	a = state.playerAce
	if p >= 21:
		return 0
	if a: 
		if p <= 17:
			return 1
		if p == 18 and d >= 9:
			return 1
		return 0
	if p >= 17:
		return 0
	if p >= 13:
		if d >= 7:
			return 1
		else:
			return 0
	if p == 12:
		if d <= 3 or d >=7:
			return 1
		return 0
	return 1
