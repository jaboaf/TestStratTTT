import copy

#Takes in a 3x3 board and returns a list of (row,col) coordinates of spots not filled with 'X' or 'O'
def openSpots(board):
	spots = []
	for row in range( len(board) ):
		for col in range( len(board[row]) ):
			if board[row][col] == 0:
				spots.append( (row,col) )
	return spots

#Takes in a 3x3 board and returns True if there is 3 in a row, and false otherwise
def isGameOver(board):
	#checking Rows
	if board[0][0] == board[0][1] == board[0][2] != 0:
		return True, board[0][0]
	elif board[1][0] == board[1][1] == board[1][2] != 0:
		return True, board[1][0]
	elif board[2][0] == board[2][1] == board[2][2] != 0:
		return True, board[2][0]

	#Checking Cols
	elif board[0][0] == board[1][0] == board[2][0] != 0:
		return True, board[0][0]
	elif board[0][1] == board[1][1] == board[2][1] != 0:
		return True, board[0][1]
	elif board[0][2] == board[1][2] == board[2][2] != 0:
		return True, board[0][2]

	#Checking Diagnols
	elif board[0][0] == board[1][1] == board[2][2] != 0:
		return True, board[0][0]
	elif board[0][2] == board[1][1] == board[2][0] != 0:
		return True, board[0][2]

	#No 3-in-a-row
	else:
		return False, 0

#takes in a 3x3, rotates 90 degrees
def rot90(board):
	return [	[ board[2][0] , board[1][0] , board[0][0] ],
				[ board[2][1] , board[1][1] , board[0][1] ],
				[ board[2][2] , board[1][2] , board[0][2] ]		]

def rot180(board):
	return [	[ board[2][2] , board[2][1] , board[2][0] ],
				[ board[1][2] , board[1][1] , board[1][0] ],
				[ board[0][2] , board[0][1] , board[0][0] ]		]

def rot270(board):
	return [	[ board[0][2] , board[1][2] , board[2][2] ],
				[ board[0][1] , board[1][1] , board[2][1] ],
				[ board[0][0] , board[1][0] , board[2][0] ]		]

#takes in 3x3 board and reflects it over the line from 0,1 to 2,1
def flipOverVert(board):
	return [	[ board[0][2] , board[0][1] , board[0][0] ],
				[ board[1][2] , board[1][1] , board[1][0] ],
				[ board[2][2] , board[2][1] , board[2][0] ] ]

#takes in 3x3 board and reflects it over the line from 1,0 to 1,2
def flipOverHor(board):
	return [	board[2],
				board[1],
				board[0]	]

def flipOverUpRight(board):
	return [	[ board[2][2] , board[1][2] , board[0][2] ],
				[ board[2][1] , board[1][1] , board[0][1] ],
				[ board[2][0] , board[1][0] , board[0][0] ]		]

def flipOverDownLeft(board):
	return [	[ board[0][0] , board[1][0] , board[2][0] ],
				[ board[0][1] , board[1][1] , board[2][1] ],
				[ board[0][2] , board[1][2] , board[2][2] ]		]

def upDiag(board):
	d = []
	for i in range( len(board) ):
		d.append( board[len(board)-1 - i][i] )
	return d

def downDiag(board):
	d = []
	for i in range( len(board) ):
		d.append( board[i][i] )
	return d

def cols(board):
	cs = []
	for c in range(3):
		col = [ board[0][c] , board[1][c] , board[2][c] ]
		cs.append(col)
	return c

def rows(board):
	rs = [ board[0] , board[1] , board[2] ]
	return rs

def similar(check, memory):
	#check is the board that we want to "check" for similarity with boards in memory
	#memory is a list of boards that form a basis for a given number of moves
	for i in range(len(memory)):
		board = memory[i]
		if check[1][1] == board[1][1]:
			if board==flipOverVert(check) or board==flipOverHor(check) or board==flipOverUpRight(check) or board==flipOverDownLeft(check):
				return True, i
			elif board == rot180(check):
				return True, i
			elif board == rot90(check) or board == rot270(check):
				return True, i
			elif board == check:
				return True, i

	return False, len(memory)

def isTrap(board, justPlayed):
	n = -1

	XwinSpots = []
	OwinSpots = []

	#rows
	for i in range(3):
		row = board[i]
		if row.count('X') == 2 and row.count('O') == 0:
			spot = ( i , row.index(0) )
			if spot not in XwinSpots:
				XwinSpots.append( spot )
		elif row.count('O') == 2 and row.count('X') == 0:
			spot = ( i , row.index(0) )
			if spot not in OwinSpots:
				OwinSpots.append( spot )

		col = [ board[0][i], board[1][i], board[2][i] ]
		if col.count('X') == 2 and col.count('O') == 0:
			spot = ( col.index(0) , i )
			if spot not in XwinSpots:
				XwinSpots.append( spot )
		elif col.count('O') == 2 and col.count('X') == 0:
			spot = ( col.index(0) , i )
			if spot not in OwinSpots:
				OwinSpots.append( spot )

	#Diagnols
	d0 = [ board[0][0], board[1][1], board[2][2] ]
	d1 = [ board[0][2], board[1][1], board[2][0] ]
	if d0.count('X') == 2 and d0.count('O') == 0:
		n = d0.index(0)
		spot = (n,n)
		if spot not in XwinSpots:
			XwinSpots.append( spot )
	elif d0.count('O') == 2 and d0.count('X') == 0:
		n = d0.index(0)
		spot = (n,n)
		if spot not in OwinSpots:
			OwinSpots.append( spot )

	if n != 1:
		if d1.count('X') == 2 and d1.count('O') == 0:
			n = d1.index(0)
			spot = ( n , int(2-n) )
			if spot not in XwinSpots:
				XwinSpots.append( spot )
		elif d1.count('O') == 2 and d1.count('X') == 0:
			n = d1.index(0)
			spot = ( n , int(2-n) )
			if spot not in OwinSpots:
				OwinSpots.append( spot )

	if justPlayed == 'X':
		if len(OwinSpots) > 0:
			return False, len(XwinSpots),  len(OwinSpots)
		elif len(XwinSpots) < 2:
			return False, len(XwinSpots),  len(OwinSpots)
		else:
			return True, len(XwinSpots),  len(OwinSpots)

	elif justPlayed == 'O':
		if len(XwinSpots) > 0:
			return False, len(XwinSpots),  len(OwinSpots)
		elif len(OwinSpots) < 2:
			return False, len(XwinSpots),  len(OwinSpots)
		else:
			return True, len(XwinSpots),  len(OwinSpots)

	else:
		return -1

def needToBlock(board, toPlay):
	if toPlay == 'X':
		opp = 'O'
	elif toPlay == 'O':
		opp = 'X'
	else:
		return -1

	blockSpots = []
	blockReq = False

	for i in range(3):
		row = board[i]
		if row.count(opp) == 2 and row.count(toPLay) == 0:
			blockSpots.append( ( i , index(0) ) )
			blockReq = True

		col = [ board[0][i] , board[1][i] , board[2][i] ]
		if col.count(opp) == 2 and col.count(toPlay) == 0:
			blockSpots.append( (index(0) , i ))
			blockReq = True

	d0 = [ board[0][0], board[1][1], board[2][2] ]
	d1 = [ board[0][2], board[1][1], board[2][0] ]

	if d0.count(opp) == 2 and d0.count(toPLay) == 0:
		blockSpots.append( ( index(0) , index(0) ) )
		blockReq = True

	if d1.count(opp) == 2 and d1.count(toPLay) == 0:
		blockSpots.append( ( index(0) , int(2- index(0)) ) )
		blockReq = True

	return blockReq, blockSpots

def P2W(board, player):
	if player == 'X':
		opp = 'O'
	elif player == 'O':
		opp = 'X'
	else:
		return -1

	lines = 0
	intersectPoints = 0
	points = dict.fromkeys(openSpots(board), 0)

	for c in range(len(board)):
		col = [ board[i][c] for i in range(len(board)) ]
		if opp not in col:
			if player in col:
				w = col.count(player)
				lines += 1
				for r in range(len(board)):
					if (r,c) in points:
						points[(r,c)] += (w+1)**2
			else:
				for r in range(len(board)):
					if (r,c) in points:
						points[(r,c)] += 1

	for r in range(len(board)):
		row = board[r]
		if opp not in row:
			if player in row:
				w = row.count(player)
				lines += 1
				for c in range(len(board)):
					if (r,c) in points:
						points[(r,c)] += (w+1)**2
			else:
				for c in range(len(board)):
					if (r,c) in points:
						points[(r,c)] += 1

	if opp not in upDiag(board):
		if player in upDiag(board):
			w = upDiag(board).count(player)
			lines += 1
			for i in range(len(board)):
				r = len(board) -1 -i
				c = i
				if (r,c) in points:
					points[(r,c)] += (w+1)**2
		else:
			for i in range(len(board)):
				r = len(board) -1 -i
				c = i
				if (r,c) in points:
					points[(r,c)] += 1

	if opp not in downDiag(board):
		if player in downDiag(board):
			w = downDiag(board).count(player)
			lines += 1
			for i in range(len(board)):
				if (i,i) in points:
					points[(i,i)] += (w+1)**2
		else:
			for i in range(len(board)):
				if (i,i) in points:
					points[(i,i)] += 1

	for v in points.values():
		if v >= 4:
			intersectPoints += 1

	return lines, intersectPoints, points

def strat(board, player):

	val = {}
	v = {}
	v['X'] = P2W(board, 'X')[2]
	v['O'] = P2W(board, 'O')[2]
	maxs = {}

	for point in openSpots(board):
		val[point] = v['X'][point] + v['O'][point]
		if val[point] in maxs:
			maxs[val[point]] += [point]
		else:
			maxs[val[point]] = [point]

	pref = 0
	goHere = (-1,-1)
	for point in maxs[max(maxs)]:
		if v[player][point] >= pref:
			pref = v[player][point]
			goHere = point

	return goHere


#uniq is a dictionary of unique boards
#	keys are number of moves
#	values are a list of unique boards formed the given number of moves
uniq = {}
terminalBasis = {}
nonTerminalBasis = {}

uniq[0] =  [	[	[0, 0, 0],
					[0, 0, 0],
					[0, 0, 0]	]	]

terminalBasis[0] = []
nonTerminalBasis[0] = [	[	[0, 0, 0],
							[0, 0, 0],
							[0, 0, 0]	]	]

#dict of valid games after being played;
#	key1 = # of Xs and Os
#	value= dict of distinct games
#		key2 = last board played (from 0 to len(nonTerminalBasis[key1]) )
#		value = set of games with nonTerminalBasis[key1][key2] board played last
gamesContinued = { 0: { 0: [ [0] ] } , 1:{} , 2:{} , 3:{} , 4:{} , 5:{} , 6:{} , 7:{} , 8:{} , 9:{} , 10:{}  }
gamesFinished = { 0:{} , 1:{} , 2:{} , 3:{} , 4:{} , 5:{} , 6:{} , 7:{} , 8:{} , 9:{} , 10:{}  }
gamesIwon = {0:{} , 1:{} , 2:{} , 3:{} , 4:{} , 5:{} , 6:{} , 7:{} , 8:{} , 9:{} , 10:{}}
gamesIlost =  {0:{} , 1:{} , 2:{} , 3:{} , 4:{} , 5:{} , 6:{} , 7:{} , 8:{} , 9:{} , 10:{}}

gameCount = {	'nonTerminal'	: { 'duplicates': {} ,
									'nonDuplicates' : {} },

				'terminal'		: { 'duplicates': {} ,
									'nonDuplicates' : { 'X' : {},
														'O' : {} }	}	}

gameCount['nonTerminal']['nonDuplicates'] = {0:0, 1:0, 2:0, 3:0, 4:0, 5:0, 6:0, 7:0, 8:0, 9:0, 10:0}
gameCount['nonTerminal']['duplicates'] = {0:0, 1:0, 2:0, 3:0, 4:0, 5:0, 6:0, 7:0, 8:0, 9:0, 10:0}

gameCount['terminal']['nonDuplicates']['X'] = {0:0, 1:0, 2:0, 3:0, 4:0, 5:0, 6:0, 7:0, 8:0, 9:0, 10:0}
gameCount['terminal']['nonDuplicates']['O'] = {0:0, 1:0, 2:0, 3:0, 4:0, 5:0, 6:0, 7:0, 8:0, 9:0, 10:0}
gameCount['terminal']['duplicates'] = {0:0, 1:0, 2:0, 3:0, 4:0, 5:0, 6:0, 7:0, 8:0, 9:0, 10:0}


#Iterates over 'board statuses' ie. when there are x number of Xs or Os, where play = x
for play in range(0,10):
	#Determining whose turn it is
	if play % 2 == 0:
		player = 'X'
	else:
		player = 'O'

	print('Play = ' + str(play) + ' , and player = ' + player)
	print('Uniqs = ' + str(len(uniq[play])))
	print('nonTerminalBasis = ' + str(len(nonTerminalBasis[play])))
	print('terminalBasis = ' + str(len(terminalBasis[play])))

	nonTbasis = []
	Tbasis = []
	basis = []
	dealWithAfter = {}
	#iterates over the unique boards
	#	Thought: should I only iterate over non-winning boards in the basis...
	for i in range(len(gamesContinued[play])):
		dealWithAfter[i] = []

		U = nonTerminalBasis[play][i]
		if player == 'X':
			spotsToPLay = [strat(U,'X')]
		else:
			spotsToPLay = openSpots(U)

		for spot in spotsToPLay:
			row = spot[0]
			col = spot[1]

			board = copy.deepcopy(U)
			board[row][col] = player

			#Thought: when I append gamesAfter, should Is append a 'relevantAfter' dict
			#so we don't have to iterate at the begining
			if play < 4 or isGameOver(board)[0] == False:
				sim = similar(board, nonTbasis)

				if sim[0] == False:
					nonTbasis.append(board)

				for seq in gamesContinued[play][i]:
					if sim[1] in gamesContinued[play+1].keys():
						newSeq = seq + [sim[1]]
						if newSeq in gamesContinued[play+1][ sim[1] ]:
							gameCount['nonTerminal']['duplicates'][play+1] += 1
						else:
							gameCount['nonTerminal']['nonDuplicates'][play+1] += 1
							gamesContinued[play+1][ sim[1] ] += [ seq + [sim[1]] ]
					else:
						gamesContinued[play+1][ sim[1] ] = [ seq + [sim[1]] ]
						gameCount['nonTerminal']['nonDuplicates'][play+1] += 1
			else:
				dealWithAfter[i] += [ board ]

	for i in dealWithAfter:
		for board in dealWithAfter[i]:
			sim = similar(board, Tbasis)

			if sim[0] == False:
				Tbasis.append(board)

			basisIndex = len(nonTbasis) + sim[1]

			winner = isGameOver(board)[1]

			for seq in gamesContinued[play][i]:
				if basisIndex in gamesFinished[play+1].keys():
					newSeq = seq + [basisIndex]

					if newSeq in gamesFinished[play+1][ basisIndex ]:
						gameCount['terminal']['duplicates'][play+1] += 1

					else:
						gameCount['terminal']['nonDuplicates'][winner][play+1] += 1
						gamesFinished[play+1][ basisIndex ] += [ seq + [basisIndex] ]

				else:
					gameCount['terminal']['nonDuplicates'][winner][play+1] += 1
					gamesFinished[play+1][ basisIndex ] = [ seq + [basisIndex] ]


	print('Number of games to be played next round')
	print(gameCount['nonTerminal']['nonDuplicates'][play+1])

	print('Number of games ended this round with X win')
	print(gameCount['terminal']['nonDuplicates']['X'][play+1])

	print('Number of games ended this round with O win')
	print(gameCount['terminal']['nonDuplicates']['O'][play+1])

	nonTerminalBasis[play+1] = nonTbasis
	terminalBasis[play+1] = Tbasis
	uniq[play+1] = nonTbasis + Tbasis


for k in uniq:
	print('******** Basis for ' + str(k) + ' plays ****')
	if len(uniq[k]) < 16:
		print('     *** nonTerminalBasis ***')
		for line in range(3):
			statment = ''
			for j in nonTerminalBasis[k]:
				statment += str(j[line][0]) + ',' + str(j[line][1]) + ',' + str(j[line][2])+  '  |  '
			print('     ' + statment)
		print('     *** terminalBasis ***')
		for line in range(3):
			statment = ''
			for j in terminalBasis[k]:
				statment += str(j[line][0]) + ',' + str(j[line][1]) + ',' + str(j[line][2])+  '  |  '
			print('     ' + statment)
	else:
		print('     *** nonTerminalBasis ***')
		for line in range(3):
			statment = ''
			for j in nonTerminalBasis[k][:12]:
				statment += str(j[line][0]) + ',' + str(j[line][1]) + ',' + str(j[line][2])+  '  |  '
			print('     ' + statment)
		print('     *** terminalBasis ***')
		for line in range(3):
			statment = ''
			for j in terminalBasis[k][:12]:
				statment += str(j[line][0]) + ',' + str(j[line][1]) + ',' + str(j[line][2])+  '  |  '
			print('     ' + statment)



for k in uniq:
	print(str(k) + '     ' + str(len(uniq[k])) + '     ' + str(len(nonTerminalBasis[k])) + '     ' +  str(len(terminalBasis[k])))

'''
for line in range(3):
	statment = ''
	for j in uniq[9][:15]:
		statment += str(j[line][0]) + ',' + str(j[line][1]) + ',' + str(j[line][2])+  '  |  '
	print(statment)
'''

print('-----------------------------------------------------------------------------------------------------')
for k in range(11):
	print('terminal nonDuplicates: X wins:' + str(gameCount['terminal']['nonDuplicates']['X'][k])  + ' O Wins: ' + str(gameCount['terminal']['nonDuplicates']['O'][k]))

print('-----------------------------------------------------------------------------------------------------')
for k in range(11):
	print('nonTerminal: nonDuplicates: ' + str(gameCount['nonTerminal']['nonDuplicates'][k])  + ' duplicates: ' + str(gameCount['nonTerminal']['duplicates'][k]))

print('-----------------------------------------------------------------------------------------------------')

leverBal = {}
trapBoardBasis = {}
trapFormBasis = {}

trapBoards = []
trapForms = []

for i in range(0,10):
	trapBoards = []
	trapForms = []
	leverBal[i] = { (0,0):0, (0,1):0, (0,2):0, (0,3):0,
					(1,0):0, (1,1):0, (1,2):0, (1,3):0,
					(2,0):0, (2,1):0, (2,2):0,
					(3,0):0, (3,1):0					}


	if i % 2 == 1:
		justPlayed = 'X'
		toPlay = 'O'
	else:
		justPlayed = 'O'
		toPlay = 'X'

	for board in nonTerminalBasis[i]:
		isTr = isTrap(board, justPlayed)

		if isTr[0] == True:
			trapBoards.append(board)
			leverBal[i][ (isTr[1], isTr[2])] += 1

			form = copy.deepcopy(board)

			for r in range(3):
				for c in range(3):
					if form[r][c] == toPlay:
						form[r][c] = 0

			sim = similar(form, trapForms)

			if sim[0] == False:
				trapForms.append(form)

		else:
			leverBal[i][ (isTr[1], isTr[2])] += 1

	trapBoardBasis[i] = trapBoards
	trapFormBasis[i] = trapForms

for k in range(0,10):
	print('   --------------------------------------------------------------------------------------------------')

	print('*** trapBoards for ' + str(k) + ' plays *** # of boards = ' + str(len(trapBoardBasis[k])) )
	for line in range(3):
		statment = ''
		for j in trapBoardBasis[k][:15]:
			statment += str(j[line][0]) + ',' + str(j[line][1]) + ',' + str(j[line][2])+  '  |  '
		print('   ' + statment)

	print('*** trapForms for ' + str(k) + ' plays *** # of forms = ' + str(len(trapFormBasis[k])) )
	for line in range(3):
		statment = ''
		for j in trapFormBasis[k][:15]:
			statment += str(j[line][0]) + ',' + str(j[line][1]) + ',' + str(j[line][2])+  '  |  '
		print('   ' + statment)

	print('** leverBal dict ***')
	print(leverBal[k])

def printBoard(board):
	for line in range(3):
 		print( str(board[line][0]) + ',' + str(board[line][1]) + ',' + str(board[line][2]) )



if len(uniq[3]) < 12:
	print('     *** nonTerminal Boards ***')
	for B in uniq[3]:
		printBoard(B)
		print(' PW2 for X: ' + str(P2W(B,'X')))
		print(' PW2 for O: ' + str(P2W(B,'O')))
else:
	print('     *** nonTerminal Boards ***')
	for B in uniq[3][:12]:
		printBoard(B)
		print(' PW2 for X: ' + str(P2W(B,'X')))
		print(' PW2 for O: ' + str(P2W(B,'O')))
