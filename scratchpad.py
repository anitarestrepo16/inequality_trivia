import numpy as np
from psychopy import visual, event, core
from time import time
import random

from utils.ui import choose_difficulty, present_text, present_question


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

print(present_question(win, 'blah', 30))

print(present_question(win, 'blah', 30))
print(present_question(win, 'blah', 30))