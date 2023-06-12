from psychopy import visual, core, event
from psychopy.tools.filetools import fromFile, toFile
import numpy as np
from time import time

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
	mouse = event.Mouse()
	q_msg = visual.TextStim(win, text = question, color = 'white', pos = (0,0.5))
	box = visual.TextBox2(win, '', color = 'white', editable = True)
	#box.clear()
	#box.setAutoDraw(False)
	q_msg.draw()
	box.draw()
	win.flip()
	t0 = time()
	t = time()
	end_txt = False
	while not end_txt:
		if mouse.getPressed() != [0, 0, 0]:
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
	
	return resp

def work_rest_segment(win, choice, gdx_obj, MVC, y_anchor):
	'''
	If chose to work, presents grip strength segment,
	otherwise presents "Rest".

	Returns tuple:
		avg_grip (float): mean grip strength for that trial
		success (Boolean): whether work trial succeeded
	'''
	# if choose to work
	if ('left' in choice):
		# Countdown to Grip
		present_text(win, '3')
		present_text(win, '3, 2')
		present_text(win, '3, 2, 1')

		# Grip
		present_text(win, 'SQUEEZE', 'white', 0.1)
		avg_grip, success = grip_segment(gdx_obj, 3, MVC, win, y_anchor) # sample 3s
		return (avg_grip, success)

	# if choose to rest
	elif ('right' in choice):
		# rest segment
		present_text(win, 'You may rest.')
		return (-99, False)

	# Anything else
	else:
		# catch all
		present_text(win, 'Please make a choice.')

def present_feedback(win, trial, choice, success):
	'''
	Present text with points lost or gained and return
		number of points.
	'''
	# default
	outcome = 'nothing'
	
	# if chose rest
	if ('right' in choice):
		# if self reward trial
		if (trial == 'self_reward'):
			outcome = "+1 point for you"
			points_self = 1
			points_other = 0
		# if other reward trial
		elif (trial == 'other_reward'):
			outcome = "+1 point for the next participant"
			points_self = 0
			points_other = 1
		# if self punishment trial
		elif (trial == 'self_punishment'):
			outcome = "-1 point for you"
			points_self = -1
			points_other = 0
		# if other punishment trial
		elif (trial == 'other_punishment'):
			outcome = "-1 point for the next participant"
			points_self = 0
			points_other = -1
		else:
			outcome = 'Warning, wrong input'
			points_self = 0
			points_other = 0
	
	# if worked and succeeded
	elif ('left' in choice) & (success):
		if trial == 'self_reward':
			outcome = "Success! \n +10 points for you"
			points_self = 10
			points_other = 0
		elif trial == 'self_punishment':
			outcome = "Success! \n -0 points for you"
			points_self = 0
			points_other = 0
		elif trial == 'other_reward':
			outcome = 'Success! \n +10 points for the next participant'
			points_self = 0
			points_other = 10
		elif trial == 'other_punishment':
			outcome = 'Success! \n -0 points for the next participant'
			points_self = 0
			points_other = 0
		else:
			outcome = 'Warning, wrong input'
			points_self = 0
			points_other = 0

	# if worked and failed
	elif ('left' in choice) & (not success):
		if trial == 'self_reward':
			outcome = "Failed. \n +0 points for you"
			points_self = 0
			points_other = 0
		elif trial == 'self_punishment':
			outcome = "Failed. \n -10 points for you"
			points_self = -10
			points_other = 0
		elif trial == 'other_reward':
			outcome = 'Failed. \n +0 points for the next participant'
			points_self = 0
			points_other = 0
		elif trial == 'other_punishment':
			outcome = 'Failed. \n -10 points for the next participant'
			points_self = 0
			points_other = -10
		else:
			outcome = 'Warning, wrong input'
			points_self = 0
			points_other = 0
	
	# sanity check
	if points_self != 0:
		assert points_other == 0
	if points_other != 0:
		assert points_self == 0
	
	present_text(win, outcome)
	return (points_self, points_other)
	