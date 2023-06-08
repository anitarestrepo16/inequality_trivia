import numpy as np
from psychopy import visual, event
from time import time
import random

from utils.ui import (
    fixation_cross,
    present_text,
    wait_for_keypress,
    choose_difficulty,
    present_question
)


#### initialize some things

# make questions lists

easy_qs = ['easy1', 'easy2']
medium_qs = ['medium1', 'medium2']
hard_qs = ['hard1', 'hard2']


# psychopy viz
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


BASELINE_TIME = 3
DIFFICULTY_WAIT_TIME = 30 # 30s to choose difficulty
ROUND_TIME = 30 # 30s to answer question
N_ROUNDS = 2 # 8 rounds total


########################
# Baseline Physio
########################

# Instructions
txt = '''
Now we are going to collect a 5-minute baseline measurement for the ECG. 
Sit comfortably, relax and breathe normally. \n
Press the spacebar when you're ready to begin.
'''
wait_for_keypress(win, txt)

# Get Baseline Physio
#parport.send_trigger('baseline_start')
present_text(win, 'Relax', BASELINE_TIME)
#parport.send_trigger('baseline_end')

########################
# Trivia Task
########################

t1 = time()

# Instructions
txt = '''
We are now going to begin the main part of the experiment. 
For each trial in this task you will be given an offer to work to 
either earn points or avoid losing points. You will then be given 
the choice to either "work" or "rest". \n
Press the spacebar to continue.
'''
wait_for_keypress(win, txt)

txt = '''
If you choose to work, you'll be asked to squeeze the hand dynamometer
to a target level for 3 seconds. If you succeed, you will successfully
obtain the offer. For some offers, the points earned or lost will be applied 
to you while for other offers the points will go to the next participant. You'll
be told who the target of the offer is at the beginning of each trial. \n
Press the spacebar to continue.
'''
wait_for_keypress(win, txt)

txt = '''
After each trial, you will receive feedback as to whether you succeeded
or failed (if you decided to work) and the number of points earned or lost
for the trial's target. \n
Press the spacebar to continue.
'''
wait_for_keypress(win, txt)

txt = '''
Let's do a practice run. Grip the hand dynamometer in your dominant 
hand. \n
Press the spacebar when you're ready for the practice round.
'''
wait_for_keypress(win, txt)

txt = '''
Now you're ready for the real task. You will complete a total of 100 trials. 
After every 25 trials you'll be asked to rate your fatigue levels and will 
be able to take a short break. Make sure to hold the hand dynamometer
exclusively in your dominant hand throughout the task. We'll start
with a fatigue rating. \n
Press the spacebar when you're ready to begin.
'''
wait_for_keypress(win, txt)

# Run Trivia Task

# cycle through rounds


for round in range(N_ROUNDS):
    # choose difficulty
	difficulty = choose_difficulty(win, DIFFICULTY_WAIT_TIME)
    # present question and get answer
	if difficulty == 'easy':
		response = present_question(win, easy_qs[round], ROUND_TIME)
	elif difficulty == 'medium':
		response = present_question(win, medium_qs[round], ROUND_TIME)
	elif difficulty == 'hard':
		response = present_question(win, hard_qs[round], ROUND_TIME)
	else:
		present_text(win, 'No difficulty level chosen.', 'white', ROUND_TIME)

t2 = time()
print('Task Complete.')
print('The task took %d minutes.'%((t2 - t1)/60))
#print('Participant earned %d points for themselves.'%(points_self))
#print('Participant earned %d points for the next participant.'%(points_other))

##########################
# and we're done!
##########################
txt = '''
That's all! You can press the spacebar to end the experiment.
If the experimenter doesn't come get you immediately, let them
know you're done using the button on your desk.
'''
wait_for_keypress(win, txt)
