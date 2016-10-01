import time
import os
import sys
import numpy as np

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
		print ''
		for k in range(COURT_WIDTH):
			sys.stdout.write(court[i][k])
			sys.stdout.flush()


# Clears the console's screen
def cls():
	os.system('cls' if os.name=='nt' else 'clear')

# Show court for first time
showCourt(COURT)

def generateRandomPosition():
	x, y = np.random.randint(1,COURT_WIDTH-2), np.random.randint(1,COURT_HEIGHT-2)
	return (x,y)

def buildOnCourt(x,y,char):
	COURT[y][x] = char

class Player():

	def __init__(self):
		self.currDir = 0
		self.positions = []

	# Stores the (x,y) positions in an array
	def storePosition(self, position):
		self.positions.append(position)

	def getPositions(self):
		return self.positions

	# Set the current direction
	def setCurrentDirection(self, dir):
		self.currDir = dir

	def getcurrentDirection(self):
		return self.currDir


player_one_start_pos = generateRandomPosition()
player_one = Player()
player_one.storePosition(player_one_start_pos)

for pos in player_one.getPositions():
	buildOnCourt(pos[0], pos[1], 'o')

# Show player
showCourt(COURT)

# fps = 5
# time_delta = 1./fps

# while True:
#     t0 = time.clock()
#     time.sleep(time_delta)
#     t1 = time.clock()
#     print 1. / (t1 - t0)