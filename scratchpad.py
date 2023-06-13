import numpy as np
from psychopy import visual, event, core
from time import time
import random

from utils.ui import (
    choose_difficulty, 
    present_text, 
    #present_question,
    fixation_cross
)

def present_question(win, question, wait_time):
	'''
	Present question, allow response entry as text and record.
	'''
	#mouse = event.Mouse()
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


win = visual.Window(
	size = (800, 600),
	color = (0, 0, 0),
	colorSpace = 'rgb255',
	screen = -1,
	units = "norm",
	fullscr = False,
	pos = (0, 0),
	allowGUI = False
	)

present_text(win, "press enter")
event.waitKeys(keyList = ['return'])

resp1 = present_question(win, 'blah1', 30)
print(resp1)
fixation_cross(win)
resp2 = present_question(win, 'blah2', 30)
print(resp2)
fixation_cross(win)
resp3 = present_question(win, 'blah3', 30)
print(resp3)