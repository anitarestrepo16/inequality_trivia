from psychopy import visual, core, event
from psychopy.tools.filetools import fromFile, toFile
import numpy as np
from time import time
import re

def fixation_cross(win):
	'''
	Displays a fixation cross for a random amount of time between
	200 and 400 milliseconds.
	'''
	fixation = visual.TextStim(win, text = '+', color = "white", pos = (0,0))
	fixation.draw()
	win.flip()
	core.wait(np.random.uniform(.2, .4))

def present_text(win, text_block, text_col = 'white', display_time = 1):
	'''
	Displays a block of text on the screen.
	'''
	msg = visual.TextStim(win, text = text_block, color = text_col, pos = (0,0))
	msg.draw()
	win.flip()
	core.wait(display_time)

def wait_for_keypress(win, message = ''):
	'''
	Wait until subject presses spacebar.
	'''
	if message:
		present_text(win, message)
	event.waitKeys(keyList = ["space"]) # wait until subject responds

def determine_start(condition):
	'''
	Determine the starting points for all players
	depending on experimental condition.
	'''
	if condition == 'inequality':
		self_start = 10
		conf1_start = 15
		conf2_start = 30
	elif condition == 'meritocracy':
		self_start = 10
		conf1_start = 10
		conf2_start = 10
	elif condition == 'equality':
		self_start = 10
		conf1_start = 10
		conf2_start = 10
	else:
		return "ERROR - NO VALID CONDITION ENTERED"
	
	return (self_start, conf1_start, conf2_start)

def present_start_points(win, self_pts, conf1_pts, conf2_pts, display_time):
	'''
	Display start point state on screen.
	'''
	self_txt = visual.TextStim(win, text = "You are starting with " + str(self_pts) + " points", color = 'red', pos = (0, 0.3))
	conf1_txt = visual.TextStim(win, text = "Player 2 is starting with " + str(conf1_pts) + " points", color = 'blue', pos = (0, 0))
	conf2_txt = visual.TextStim(win, text = "Player 3 is starting with  " + str(conf2_pts) + " points", color = 'green', pos = (0, -0.3))
	self_txt.draw()
	conf1_txt.draw()
	conf2_txt.draw()
	win.flip()
	core.wait(display_time)

def determine_end(condition, subj_total_points):
	'''
	Determine ending points for confederates
	based on condition and points earned by participant.
	'''
	if condition == 'inequality':
		conf1_end = subj_total_points + 10
		conf2_end = subj_total_points + 30
	elif condition == 'meritocracy':
		conf1_end = subj_total_points + 10
		conf2_end = subj_total_points + 30
	elif condition == 'equality':
		conf1_end = subj_total_points + 2
		conf2_end = subj_total_points + 4
	
	return (conf1_end, conf2_end)

def present_end_points(win, self_pts, conf1_pts, conf2_pts, display_time):
	'''
	Display end point state on screen.
	'''
	self_txt = visual.TextStim(win, text = "You won " + str(self_pts) + " points", color = 'red', pos = (0, 0.3))
	conf1_txt = visual.TextStim(win, text = "Player 2 won " + str(conf1_pts) + " points", color = 'blue', pos = (0, 0))
	conf2_txt = visual.TextStim(win, text = "Player 3 won " + str(conf2_pts) + " points", color = 'green', pos = (0, -0.3))
	self_txt.draw()
	conf1_txt.draw()
	conf2_txt.draw()
	win.flip()
	core.wait(display_time)


def choose_difficulty(win, wait_time):
	'''
    Shows options (easy vs. medium vs. hard), waits for mouse click
	  and records choice. 
    '''
	mouse = event.Mouse()
	easy_rect = visual.rect.Rect(win, pos = (-0.6, 0))
	medium_rect = visual.rect.Rect(win, pos = (0, 0))
	hard_rect = visual.rect.Rect(win, pos = (0.6, 0))
	easy_txt = visual.TextStim(win, color = "SteelBlue", pos = (-0.6, 0),
                                  text = 'Easy')
	medium_txt = visual.TextStim(win, color = "SteelBlue", pos = (0, 0),
                                  text = 'Medium')
	hard_txt = visual.TextStim(win, color = "SteelBlue", pos = (0.6, 0),
                                  text = 'Hard')
	
	print(mouse.getPressed())
	
	easy_rect.draw()
	medium_rect.draw()
	hard_rect.draw()
	easy_txt.draw()
	medium_txt.draw()
	hard_txt.draw()
	win.flip()
	
	clicks = mouse.getPressed()
	print(clicks)
	t0 = time()
	t = time()

	while clicks == [0, 0, 0]:
		if mouse.isPressedIn(easy_rect):
			return 'easy'
		elif mouse.isPressedIn(medium_rect):
			return 'medium'
		elif mouse.isPressedIn(hard_rect):
			return 'hard'
		else:
			t = time()
			if t > t0 + wait_time:
				return 'no_response'
	
def present_question(win, question, wait_time):
	'''
	Present question, allow response entry as text and record.
	'''
	q_msg = visual.TextStim(win, text = question, color = 'white', pos = (0,0.5))
	box = visual.TextBox2(win, '', color = 'white', editable = True)
	q_msg.draw()
	box.draw()
	win.flip()
	t0 = time()
	t = time()
	end_txt = False
	while not end_txt:
		keys = event.getKeys()
		if 'return' in keys:
			resp = box.getText()
			box.clear()
			box.setAutoDraw(False)
			win.flip()
			end_txt = True
		else:
			box.setAutoDraw(True)
			q_msg.draw()
			win.flip()
			t = time()
			if t > t0 + wait_time:
				resp = box.getText()
				box.clear()
				box.setAutoDraw(False)
				win.flip()
				end_txt = True
			else:
				continue
	
	return resp

def check_answer(response, answer):
	'''
	Compare participant's response (a string)
	  to correct answer (a list of strings) and 
	return accuracy (1 or 0). 
	'''
	# lower case
	response = str.lower(response)
	answer = [str.lower(item) for item in answer]
	# remove non-alphanumeric
	response = re.sub(r'\W+', '', response)
	answer = [re.sub(r'\W+', '', item) for item in answer]

	# check if response is in list of possible answers
	if response in answer:
		return 1
	else:
		return 0


def present_feedback(win, difficulty, accuracy, total_points, display_time):
	'''
	Present text with points lost or gained and return
		number of points.
	'''
	# default
	outcome = 'nothing'
	acc_txt = 'nothing'

	# correct/incorrect
	if accuracy == 1:
		acc_txt = 'correctly'
	elif accuracy == 0:
		acc_txt = 'incorrectly'
	
	# if difficulty is easy
	if difficulty == 'easy':
		# if got it right
		if accuracy == 1:
			outcome = "+$1.00 for you"
			points_self = 1
		# if got it wrong
		elif accuracy == 0:
			outcome = "-$1.00 for you"
			points_self = -1
	# if difficulty is medium
	elif difficulty == 'medium':
		# if got it right
		if accuracy == 1:
			outcome = "+$3.00 for you"
			points_self = 3
		# if got it wrong
		elif accuracy == 0:
			outcome = "-$3.00 for you"
			points_self = -3
	# if difficulty is hard
	elif difficulty == 'hard':
		# if got it right
		if accuracy == 1:
			outcome = "+$5.00 for you"
			points_self = 5
		# if got it wrong
		elif accuracy == 0:
			outcome = "-$5.00 for you"
			points_self = -5
	
	#present_text(win, outcome)
	self_txt = visual.TextStim(win, text = "You chose a(n) " + difficulty +
			     " question and answered " + acc_txt + '\n' + 'points earned: ' + 
				 outcome + '\n' + 'total points: ' + str(total_points), color = 'red', pos = (0, 0.3))
	#conf1_txt = visual.TextStim(win, text = "Player 2 is starting with " + str(conf1_pts) + " points", color = 'blue', pos = (0, 0))
	#conf2_txt = visual.TextStim(win, text = "Player 3 is starting with  " + str(conf2_pts) + " points", color = 'green', pos = (0, -0.3))
	self_txt.draw()
	#conf1_txt.draw()
	#conf2_txt.draw()
	win.flip()
	core.wait(display_time)
	
	return points_self


	