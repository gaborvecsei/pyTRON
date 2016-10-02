import time
import os
import sys
import numpy as np
# Windows OS specific:
import msvcrt

# Clears the console's screen
def cls():
	os.system('cls' if os.name=='nt' else 'clear')

# Asks whether a key has been acquired
def kbfunc():
	x = msvcrt.kbhit()
	if x:
		ret = msvcrt.getch()
	else:
		ret = False
	return ret


class Court():

	def __init__(self, width, height):
		self.court_width = width
		self.court_height = height
		self.court = []
		# Prepare court for usage
		self.build()

	# Prepare the court (draw the edges etc...)
	def build(self):
		# Build the court
		for i in range(self.court_height):
			court_row = []
			for k in range(self.court_width):
				if i == 0:
					court_row.append('-')
				elif i == self.court_height-1:
					court_row.append('-')
				elif k == 0 and i != 0:
					court_row.append('|')
				elif k == self.court_width-1:
					court_row.append('|')
				else:
					court_row.append(' ') 
			if len(court_row) > 0:
				self.court.append(court_row)


	# Print the court on the console
	def printCourt(self):
		cls()
		# Prepare a string that represents the court
		screen = "\n".join(''.join(line) for line in self.court)
		# Print the court
		sys.stdout.write(screen)
		sys.stdout.flush()

	# Put a character somewhere in the court
	def buildOnCourt(self, x, y, char):
		self.court[y][x] = char

	# Draw the players with their given character
	def drawPlayers(self, players):
		# i is the index in the players array
		for i, player in enumerate(players):
			playerCharacter = player.getCharacter()
			for pos in player.getPositions():
				self.buildOnCourt(pos[0], pos[1], playerCharacter)

	# Generate a random position within the court
	def generateRandomPositionOnCourt(self):
		x, y = np.random.randint(1,self.court_width-2), np.random.randint(1,self.court_height-2)
		return (x,y)

	def getCourtArray(self):
		return self.court

	def getWidthHeight(self):
		return (self.court_width, self.court_height)


class Player():

	def __init__(self, currDir = 0, playerCharacter = 'o'):
		self.currDir = currDir
		self.positions = []
		self.playerCharacter = playerCharacter

	# Stores the given (x,y) positions in an array
	def storePosition(self, position):
		self.positions.append(position)

	def getCharacter(self):
		return self.playerCharacter

	# Returns the position array where we can see the players positions
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

	# Detects if the player collided with itself
	def detectSelfCollision(self, nextPosition):
		if nextPosition in self.positions:
			return True
		else:
			return False

	def detectCourtCollision(self, court):
		# (x,y)
		lastPosition = self.positions[-1]
		# (width,height)
		(w,h) = court.getWidthHeight()

		if (lastPosition[0] >= w-1) or (lastPosition[0] <= 0):
			return True
		elif (lastPosition[1] >= h-1) or (lastPosition[1] <= 0):
			return True
		else:
			return False



def ControllPlayer(keyPressed, player, inputChars):
	left, right, up, down = inputChars
	# LEFT
	if keyPressed != False and keyPressed.decode() == left and player.getcurrentDirection() != 1:
		player.changeDirection(0)
		# You can use:  player_one.changeDirection(player_one.translateDirection('left')) too
	# RIGHT
	elif keyPressed != False and keyPressed.decode() == right and player.getcurrentDirection() != 0:
		player.changeDirection(1)
	# UP
	elif keyPressed != False and keyPressed.decode() == up and player.getcurrentDirection() != 3:
		player.changeDirection(2)
	# DOWN
	elif keyPressed != False and keyPressed.decode() == down and player.getcurrentDirection() != 2:
		player.changeDirection(3)


# Create a new court
court = Court(100, 20)

# Create a player
player_one_start_pos = court.generateRandomPositionOnCourt()
player_one = Player(playerCharacter='x')
player_one.storePosition(player_one_start_pos)

# Create a player
player_two_start_pos = court.generateRandomPositionOnCourt()
player_two = Player(playerCharacter='o')
player_two.storePosition(player_two_start_pos)

fps = 30
time_delta = 1./fps

while True:
	t0 = time.clock()
	time.sleep(time_delta)
	t1 = time.clock()

	# Detect key hits
	keyPressed = kbfunc()
	if keyPressed != False:
		# Change player directions if necessary
		ControllPlayer(keyPressed, player_one, ('a', 'd', 'w', 's'))
		ControllPlayer(keyPressed, player_two, ('j', 'l', 'i', 'k'))

	####### Player One ########

	# Move the player in the given direction
	is_player_one_moved = player_one.moveOneStep()
	# If we couldn't move our player than that's the end of the game
	if is_player_one_moved == False:
		print "\nSELF COLLISION"
		sys.exit(0)

	if player_one.detectCourtCollision(court):
		print "\nWALL COLLISION"
		sys.exit()


	####### Player Two ########

	is_player_two_moved = player_two.moveOneStep()

	if is_player_two_moved == False:
		print "\nSELF COLLISION"
		sys.exit(0)

	if player_two.detectCourtCollision(court):
		print "\nWALL COLLISION"
		sys.exit()



	# Show the court and players
	court.drawPlayers([player_one, player_two])
	court.printCourt()