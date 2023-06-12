import numpy as np
from psychopy import visual, event, core
from time import time
import random

from utils.ui import (
    choose_difficulty, 
    present_text, 
    present_question,
    fixation_cross
)


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



resp1 = present_question(win, 'blah1', 30)
print(resp1)
fixation_cross(win)
resp2 = present_question(win, 'blah2', 30)
print(resp2)
fixation_cross(win)
resp3 = present_question(win, 'blah3', 30)
print(resp3)