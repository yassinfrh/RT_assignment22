from __future__ import print_function

import time
from sr.robot import *

a_th = 2.0
""" float: Threshold for the control of the orientation"""

s_d_th = 0.4
g_d_th = 0.6
""" float: Threshold for the control of the linear distance (s for silver tokens and g for golden tokens)"""

R = Robot()
""" instance of the class Robot"""

def drive(speed, seconds):
	"""
	Function for setting a linear velocity
    
	Args: speed (int): the speed of the wheels seconds (int): the time interval
	"""
	R.motors[0].m0.power = speed
	R.motors[0].m1.power = speed
	time.sleep(seconds)
	R.motors[0].m0.power = 0
	R.motors[0].m1.power = 0

def turn(speed, seconds):
	"""
	Function for setting an angular velocity
    
	Args: speed (int): the speed of the wheels seconds (int): the time interval
	"""
	R.motors[0].m0.power = speed
	R.motors[0].m1.power = -speed
	time.sleep(seconds)
	R.motors[0].m0.power = 0
	R.motors[0].m1.power = 0

def find_token(token_type, tokens_list):
	"""
	Function to find the closest token
	
	Args: 
		token_type : the type of token found (MARKER_TOKEN_GOLD for gold and MARKER_TOKEN_SILVER for silver)
		tokens_list: list of tokens of type token_type that have been already arranged

	Returns:
		dist (float): distance of the closest token (-1 if no token is detected)
		rot_y (float): angle between the robot and the token (-1 if no token is detected)
	"""
	dist=100
	for token in R.see():
		if token.dist < dist and token.info.marker_type == token_type and token.info.code not in tokens_list:
			dist=token.dist
			rot_y=token.rot_y
			code = token.info.code
	if dist==100:
		return -1, -1, -1
	else:
		return dist, rot_y, code

def approach_token(token_type, tokens_list):
	"""
	Function to approach the closest token of type token_type and grab it if it's silver or release the silver token if it's golden
	
	Args: 
		token_type: the type of token found (MARKER_TOKEN_GOLD for gold and MARKER_TOKEN_SILVER for silver)
		tokens_list: list of tokens of type token_type that have been already arranged
	"""
	while 1:
		dist, rot_y, code = find_token(token_type, tokens_list)  # we look for markers
		if dist==-1:
			turn(10, 0.1)  # if no markers are detected
		elif token_type == MARKER_TOKEN_SILVER and dist <s_d_th: 
			R.grab() # if we are close to the silver token, we grab it.
			tokens_list.append(code) # we add the grabbed silver token to the list
			return
		elif token_type == MARKER_TOKEN_GOLD and dist < g_d_th:
			R.release() # if we are close to the golden token, we release the silver token.
			tokens_list.append(code) #we add the paired golden token to the list
			drive(-100, 1)
			return
		elif -a_th<= rot_y <= a_th: # if the robot is well aligned with the token, we go forward
			drive(200, 0.1)
		elif rot_y < -a_th: # if the robot is not well aligned with the token, we move it on the left or on the right
			turn(-10, 0.1)
		elif rot_y > a_th:
			turn(+10, 0.1)
			
silver_tokens = [] # list of already grabbed silver tokens
golden_tokens = [] # list of already paired golden tokens
NUM_TOKENS = 6 # number of tokens to arrange/grab

while 1:

	approach_token(MARKER_TOKEN_SILVER, silver_tokens) # approach a silver token and grab it
	approach_token(MARKER_TOKEN_GOLD, golden_tokens) # approach a golden token and release the silver token next to it
	if len(silver_tokens) == 6: # if all the tokens have been arranged, exit
		exit()
