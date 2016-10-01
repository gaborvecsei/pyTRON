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

player_one_pos = []

player_one_start_pos_x, player_one_start_pos_y = np.random.randint(1,COURT_WIDTH-2), np.random.randint(1,COURT_HEIGHT-2)
COURT[player_one_start_pos_y][player_one_start_pos_x] = 'Q'

# This is the starting position for player one
player_one_pos.append((player_one_start_pos_x, player_one_start_pos_y))

# Show player
showCourt(COURT)

