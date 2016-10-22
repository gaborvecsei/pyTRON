"""
*****************************************************
*
*              Gabor Vecsei
* Email:       vecseigabor.x@gmail.com
* Blog:        https://gaborvecsei.wordpress.com/
* LinkedIn:    www.linkedin.com/in/vecsei-gabor
* Github:      https://github.com/gaborvecsei
*
*****************************************************
"""

import time
import os
import sys
import numpy as np
# Windows OS specific:
import msvcrt

# This is a class that represents the game's court
class Court():

	def __init__(self, width, height):
		self.court_width = width
		self.court_height = height
		self.court = []
		# Prepare court
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
		#sys.stdout.flush()

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

	def clearCourt(self):
		self.court = []
		self.build()



# This is a class for the players
class Player():

	# inputCharacters: you have to give in this order: (left, right, up, down)
	# you can control the player with these characters
	# playerCharacter: This is the character we will draw on the court to display the player
	def __init__(self, startPosition, inputCharacters, currDir = 0, playerCharacter = 'o'):
		self.currDir = currDir
		self.positions = []
		self.playerCharacter = playerCharacter
		self.inputCharacters = inputCharacters
		if len(self.inputCharacters) != 4:
			print "Error with player input characters!"
			sys.exit(1)
		self.storePosition(startPosition)

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

		self.storePosition(newPosition)


	# Detects if the player collided with itself
	def detectSelfCollision(self):
		lastPosition = self.positions[-1]
		if lastPosition in self.positions[0:-1]:
			return True
		else:
			return False

	# Detect if we collided to the wall
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

	# Detect collision with other players
	def detectPlayerCollision(self, otherPlayers):
		lastPosition = self.positions[-1]
		for otherPlayer in otherPlayers:
			if lastPosition in otherPlayer.getPositions():
				# Return the collision position too (we can draw it etc..., it's more user friendly)
				return True, lastPosition
			else:
				return False, (0,0)
		return False, (0,0)


	# Change the player's direction based on the user input
	def controllPlayerWithInput(self, keyPressed):
		left, right, up, down = self.inputCharacters

		# LEFT
		if keyPressed != False and keyPressed.decode() == left and self.getcurrentDirection() != 1:
			self.changeDirection(0)
			# You can use:  player_one.changeDirection(player_one.translateDirection('left')) too
		# RIGHT
		elif keyPressed != False and keyPressed.decode() == right and self.getcurrentDirection() != 0:
			self.changeDirection(1)
		# UP
		elif keyPressed != False and keyPressed.decode() == up and self.getcurrentDirection() != 3:
			self.changeDirection(2)
		# DOWN
		elif keyPressed != False and keyPressed.decode() == down and self.getcurrentDirection() != 2:
			self.changeDirection(3)


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

# Goes to the main menu if the user presses x
def gotoMainMenu():
	print '\nPress (x) to go back to the main menu'
	pressedKey = raw_input('')
	if pressedKey == 'x' or pressedKey == 'X':
		cls()
		mainScreen()
	else:
		gotoMainMenu()

# We start the game with this screen where we can choose what to do
def mainScreen():
	cls()
	print "Welcome to pyTRON!"
	print "\nTron game written in python by Gabor Vecsei\n"
	print "Press (1) to play a game"
	print "Press (2) to see who made it"
	print "Press (3) to show some help"
	print "Press (4) to exit from the game"
	
	selectedMenuPoint = raw_input("Enter the selected menu point and press ENTER: ")
	print "\n\n"

	if eval(selectedMenuPoint) == 1:
		gamePlayScreen()
	elif eval(selectedMenuPoint) == 2:
		aboutScreen()
	elif eval(selectedMenuPoint) == 3:
		helpScreen()
	elif eval(selectedMenuPoint) == 4:
		exit()
	else:
		mainScreen()

def aboutScreen():
	cls()
	print "		Tron game made by Gabor Vecsei"
	print "		2016 October"
	print """
		/*****************************************************
		*
		*              Gabor Vecsei
		* Email:       vecseigabor.x@gmail.com
		* Blog:        https://gaborvecsei.wordpress.com/
		* LinkedIn:    www.linkedin.com/in/vecsei-gabor
		* Github:      https://github.com/gaborvecsei
		*
		*****************************************************
		"""
	gotoMainMenu()

def helpScreen():
	cls()
	print "Help menu, so you can play pyTRON\n"
	print "Okay, okay...I will help you, just read this:"
	print "Avoid collisions with the wall, other players and even with yourself."
	print "Controls:\nplayer 1: W, A, S, D,\nplayer 2: I, J, K, L"
	print "That's it...Start playing! :P"
	gotoMainMenu()

def exit():
	print "\nThank you for playing!\n"
	sys.exit(0)


# We can say that fps here is the speed of the game
# newPlayers is a list. This contains newly added players from the settings, we concatenate this list with the existing one (players)
# The higher the number the lower we wait in the while
def gamePlayScreen(fps = 10):

	# Create a new court
	court = Court(100, 20)
	
	# Create a player
	player_one_start_pos = court.generateRandomPositionOnCourt()
	player_one = Player(player_one_start_pos, ('a', 'd', 'w', 's'), playerCharacter='x')
	# Move in a random direction at first
	player_one.changeDirection(np.random.randint(0,4))
	
	# Create a player
	player_two_start_pos = court.generateRandomPositionOnCourt()
	player_two = Player(player_two_start_pos, ('j', 'l', 'i', 'k'), playerCharacter='o')
	# Move in a random direction at first
	player_two.changeDirection(np.random.randint(0,4))

	players = [player_one, player_two]

	time_delta = 1./fps
	
	while True:
		t0 = time.clock()
		time.sleep(time_delta)
		t1 = time.clock()

		# Detect user input
		keyPressed = kbfunc()
	
		# Move the players and detect collisions
		for player in players:
			# For inputs change the players direction
			if keyPressed != False:
				player.controllPlayerWithInput(keyPressed)

			# Move the player
			player.moveOneStep()
	
			# Copy the players array
			otherPlayers = players[:]
			# Remove the "active" player and check if the active player collided it with someone
			otherPlayers.remove(player)
			isPlayerCollision, collisionPosition = player.detectPlayerCollision(otherPlayers)
			if isPlayerCollision:
				# Put a character where the collision happened
				court.buildOnCourt(collisionPosition[0], collisionPosition[1], '#')
				# Draw the court one last time to show the collision
				court.printCourt()
				print "\nPlayers Collision for player: " + player.getCharacter()
				gotoMainMenu()

			if player.detectSelfCollision():
				print "\nSELF COLLISION for player: " + player.getCharacter()
				gotoMainMenu()
	
			if player.detectCourtCollision(court):
				print "\nWALL COLLISION for player: " + player.getCharacter()
				gotoMainMenu()

			# Show the court and players in the console
			court.drawPlayers(players)
			court.printCourt()


############ GAME STARTS HERE ################ 

# Show the main screen
mainScreen()