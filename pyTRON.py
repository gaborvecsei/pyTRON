import time
import os
import sys
import numpy as np
# Windows specific:
import msvcrt

COURT_WIDTH = 100
COURT_HEIGHT = 20

# Height, Width
COURT = []

# Build the court
for i in range(COURT_HEIGHT):
	COURT_ROW = []
	for k in range(COURT_WIDTH):
		if i == 0:
			COURT_ROW.append('-')
		elif i == COURT_HEIGHT-1:
			COURT_ROW.append('-')
		elif k == 0 and i != 0:
			COURT_ROW.append('|')
		elif k == COURT_WIDTH-1:
			COURT_ROW.append('|')
		else:
			COURT_ROW.append(' ') 
	if len(COURT_ROW) > 0:
		COURT.append(COURT_ROW)

def showCourt(court):
	cls()
	# Print the court
	for i in range(COURT_HEIGHT):
		# For the newline
		print ''
		for k in range(COURT_WIDTH):
			sys.stdout.write(court[i][k])
			sys.stdout.flush()


# Clears the console's screen
def cls():
	os.system('cls' if os.name=='nt' else 'clear')

# Show court for first time
# showCourt(COURT)

def generateRandomPosition():
	x, y = np.random.randint(1,COURT_WIDTH-2), np.random.randint(1,COURT_HEIGHT-2)
	return (x,y)

def buildOnCourt(x,y,char):
	COURT[y][x] = char


class Player():

	def __init__(self, currDir = 0):
		self.currDir = currDir
		self.positions = []

	# Stores the (x,y) positions in an array
	def storePosition(self, position):
		self.positions.append(position)

	def getPositions(self):
		return self.positions

	# Set the current direction
	def changeDirection(self, dir):
		self.currDir = dir

	def getcurrentDirection(self):
		return self.currDir

	def translateDirection(self, currDir):
		dirs = {'left':0, 'right':1, 'up':2, 'down':3}
		return dirs[currDir]

	# Move one step with player in the current direction
	def moveOneStep(self):
		lastPosition = self.positions[-1]
		newPosition = (0,0)
		if self.currDir == 0:
			newPosition = (lastPosition[0]-1, lastPosition[1])
		elif self.currDir == 1:
			newPosition = (lastPosition[0]+1, lastPosition[1])
		elif self.currDir == 2:
			newPosition = (lastPosition[0], lastPosition[1]-1)
		else:
			newPosition = (lastPosition[0], lastPosition[1]+1)

		if self.detectSelfCollision(newPosition) == True:
			return False
		else:
			self.storePosition(newPosition)
			return True

	def detectSelfCollision(self, nextPosition):
		if nextPosition in self.positions:
			return True
		else:
			return False



# asks whether a key has been acquired
def kbfunc():
	#this is boolean for whether the keyboard has bene hit
	x = msvcrt.kbhit()
	if x:
		#getch acquires the character encoded in binary ASCII
		ret = msvcrt.getch()
	else:
		ret = False
	return ret


def drawPlayersOnCourt(players, playerCharacters):
	# Check if we has the same number of players as characters
	if len(players) != len(playerCharacters):
		print "ERROR with drawPlayersOnCourt"
		sys.exit(1)
	else:
		# i is the index in the players array
		for i, player in enumerate(players):
			for pos in player.getPositions():
				buildOnCourt(pos[0], pos[1], playerCharacters[i])



player_one_start_pos = generateRandomPosition()
player_one = Player()
player_one.storePosition(player_one_start_pos)


fps = 30
time_delta = 1./fps

while True:
	t0 = time.clock()
	time.sleep(time_delta)
	t1 = time.clock()

	# Detect key hits
	keyPressed = kbfunc()

	# LEFT
	if keyPressed != False and keyPressed.decode() == 'a' and player_one.getcurrentDirection() != 1:
		player_one.changeDirection(0)
		# You can use:  player_one.changeDirection(player_one.translateDirection('left')) too
	# RIGHT
	elif keyPressed != False and keyPressed.decode() == 'd' and player_one.getcurrentDirection() != 0:
		player_one.changeDirection(1)
	# UP
	elif keyPressed != False and keyPressed.decode() == 'w' and player_one.getcurrentDirection() != 3:
		player_one.changeDirection(2)
	# DOWN
	elif keyPressed != False and keyPressed.decode() == 's' and player_one.getcurrentDirection() != 2:
		player_one.changeDirection(3)
	
	# Move the player in the given direction
	is_player_one_moved = player_one.moveOneStep()
	# If we couldn't move our player than that's the end of the game
	if is_player_one_moved == False:
		sys.exit(0)

	drawPlayersOnCourt([player_one], ['w'])

	showCourt(COURT)