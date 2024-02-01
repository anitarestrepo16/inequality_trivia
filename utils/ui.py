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

def make_round_counter(win, round_num, text_col = 'white', position = (3, 3)):
	'''
	Create instance of round counter.
	'''
	return visual.TextStim(win, text = "Round: " + str(round_num), color = text_col, pos = position)

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


def choose_difficulty(win, wait_time, round_num):
	'''
    Shows options (easy vs. medium vs. hard), waits for mouse click
	  and records choice. 
    '''
	round_counter = make_round_counter(win, round_num)
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
	
	round_counter.draw()
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
	
def present_question(win, question, wait_time, round_num):
	'''
	Present question, allow response entry as text and record.
	'''
	round_counter = make_round_counter(win, round_num)
	q_msg = visual.TextStim(win, text = question, color = 'white', pos = (0,0.5))
	box = visual.TextBox2(win, '', color = 'white', editable = True)
	round_counter.draw()
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
			round_counter.draw()
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

def determine_points_self(accuracy, difficulty):
	'''
	Determine points earned depending on accuracy and difficulty level.
	'''
	if difficulty == 'easy':
		# if got it right
		if accuracy == 1:
			points_self = 1
		# if got it wrong
		elif accuracy == 0:
			points_self = -1
	
	elif difficulty == 'medium':
		# if got it right
		if accuracy == 1:
			points_self = 3
		# if got it wrong
		elif accuracy == 0:
			points_self = -3
	
	elif difficulty == 'hard':
		# if got it right
		if accuracy == 1:
			points_self = 5
		# if got it wrong
		elif accuracy == 0:
			points_self = -5
	
	return points_self

def determine_confederates_alt(difficulty, conf1_points, conf2_points, condition):
	'''
	Determine the confederates' choices and points for the trial.
	'''
	# for unequal end state
	if condition != 'equality':
		if difficulty == 'easy':
			conf1_points = conf1_points + 3
			conf2_points = conf2_points + 3
		elif difficulty == 'medium':
			conf1_points = conf1_points + 3
			conf2_points = conf2_points + 5
		elif difficulty == 'hard':
			conf1_points = conf1_points + 5
			conf2_points = conf2_points + 5
	# for equal end state
	elif condition == 'equality':
		if difficulty == 'easy':
			conf1_points = conf1_points + 1
			conf2_points = conf2_points + 1
		elif difficulty == 'medium':
			conf1_points = conf1_points + 3
			conf2_points = conf2_points + 3
		elif difficulty == 'hard':
			conf1_points = conf1_points + 5
			conf2_points = conf2_points + 5
	
	return (conf1_points, conf2_points)
			
def determine_confederates(total_points_self, total_points_conf1, total_points_conf2, condition):
	'''
	Determine the confederates' choices and points for the trial.
	'''
	# for unequal end state
	if condition != 'equality':
		# confederate 1
		if total_points_conf1 <= total_points_self + 10:
			conf1_points = 5
		elif (total_points_conf1 > total_points_self + 10) & (total_points_conf1 < total_points_self + 15):
			conf1_points = 3
		else:
			conf1_points = 1
		# confederate 2
		if total_points_conf2 <= total_points_self + 20:
			conf2_points = 5
		elif (total_points_conf2 > total_points_self + 20) & (total_points_conf2 < total_points_self + 30):
			conf2_points = 3
		else:
			conf2_points = 1
		
	# for equal end state
	elif condition == 'equality':
		# confederate 1
		if total_points_conf1 <= total_points_self - 5:
			conf1_points = 5
		elif (total_points_conf1 > total_points_self - 5) & (total_points_conf1 < total_points_self + 2):
			conf1_points = 3
		else:
			conf1_points = 1
		# confederate 2
		if total_points_conf2 <= total_points_self - 3:
			conf2_points = 5
		elif (total_points_conf2 > total_points_self - 3) & (total_points_conf2 < total_points_self + 2):
			conf2_points = 3
		else:
			conf2_points = 1
	
	return (conf1_points, conf2_points)

def present_practice_feedback(win, accuracy, difficulty, display_time):
	'''
	Present text with difficulty level and points earned for participant only.
	'''
	# default
	acc_txt = 'nothing'
	# correct/incorrect
	if accuracy == 1:
		acc_txt = 'correctly'
	elif accuracy == 0:
		acc_txt = 'incorrectly'
	points_earned = determine_points_self(accuracy, difficulty)
	self_txt = visual.TextStim(win, text = "This was a(n) " + difficulty +
			    " question and you answered " + acc_txt + '\n points earned: ' + 
				str(points_earned), color = 'red', pos = (0, 0.3))	
	self_txt.draw()
	win.flip()
	core.wait(display_time)


def present_feedback(win, difficulty, accuracy, points_self, total_points, 
		     conf1_points, conf2_points, total_points_conf1, total_points_conf2, display_time, round_num):
	'''
	Present text with points lost or gained.
	'''
	round_counter = make_round_counter(win, round_num)
	### Subject
	# default
	acc_txt = 'nothing'
	# correct/incorrect
	if accuracy == 1:
		acc_txt = 'correctly'
	elif accuracy == 0:
		acc_txt = 'incorrectly'
	self_txt = visual.TextStim(win, text = "You chose a(n) " + difficulty +
			    " question and answered " + acc_txt + '\n points earned: ' + 
				str(points_self) + '\n total points: ' + str(total_points), color = 'red', pos = (0, 0.3))	

	### Confederate 1
	if conf1_points == 1:
		conf1_diff = 'easy'
	elif conf1_points == 3:
		conf1_diff = 'medium'
	elif conf1_points == 5:
		conf1_diff = 'hard'

	conf1_txt = visual.TextStim(win, text = "Player 2 chose a(n) " + conf1_diff + " question and answered correctly" +
			     '\n points earned: ' + str(conf1_points)  + 
				 '\n total points: ' + str(total_points_conf1), color = 'blue', pos = (0, 0.3))

	### Confederate 2
	if conf2_points == 1:
		conf2_diff = 'easy'
	elif conf2_points == 3:
		conf2_diff = 'medium'
	elif conf2_points == 5:
		conf2_diff = 'hard'

	conf2_txt = visual.TextStim(win, text = "Player 3 chose a(n) " + conf2_diff + " question and answered correctly" +
			     '\n points earned: ' + str(conf2_points)  + 
				 '\n total points: ' + str(total_points_conf2), color = 'green', pos = (0, 0.3))
	
	## present sequentially
	round_counter.draw()
	self_txt.draw()
	win.flip()
	core.wait(display_time)
	round_counter.draw()
	conf1_txt.draw()
	win.flip()
	core.wait(display_time)
	round_counter.draw()
	conf2_txt.draw()
	win.flip()
	core.wait(display_time)


	