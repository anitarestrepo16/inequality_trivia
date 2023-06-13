import numpy as np
from psychopy import visual, event
from time import time
import random

from utils.ui import (
    fixation_cross,
    present_text,
    wait_for_keypress,
    choose_difficulty,
    present_question,
    check_answer,
    present_feedback
)

from utils.write import (
    CSVWriter_trial,
	CSVWriter_block,
	CSVWriter_subj
) 

#from utils.triggerer import Triggerer

#### initialize some things

# parport triggers
#parport = Triggerer(0)
#parport.set_trigger_labels(['MVC_start', 'MVC_end',
#			     'baseline_start', 'baseline_end',
#			     'fatigue_start', 'fatigue_end',
#				   'show_offer', 'make_choice', 'work_rest', 'feedback'])

# data handling
subj_num = input("Enter subject number: ")
subj_num = int(subj_num)
trial_log = CSVWriter_trial(subj_num)
#block_log = CSVWriter_block(subj_num)
#subj_log = CSVWriter_subj(subj_num)
np.random.seed(subj_num)
total_points = 0
points_self = 0
trial_num = 1


# make question dictionaries with answers

easy_qs = ['easy1', 'easy2']
easy_answers = ['easy_answer1', 'easy_answer2']
medium_qs = ['medium1', 'medium2']
medium_answers = ['medium_answer1', 'medium_answer2']
hard_qs = ['hard1', 'hard2']
hard_answers = ['hard_answer1', 'hard_answer2']


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


BASELINE_TIME = 3 # 5 minutes (300s)
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
Task Instructions here. \n
Press the spacebar to continue.
'''
wait_for_keypress(win, txt)

# Run Trivia Task

# cycle through rounds
for round in range(N_ROUNDS):
    # choose difficulty
	difficulty = choose_difficulty(win, DIFFICULTY_WAIT_TIME)
    # present question and get response
	if difficulty == 'easy':
		question = easy_qs[round]
		response = present_question(win, question, ROUND_TIME)
		answer = easy_answers[round]
	elif difficulty == 'medium':
		question = medium_qs[round]
		response = present_question(win, question, ROUND_TIME)
		answer = medium_answers[round]
	elif difficulty == 'hard':
		question = hard_qs[round]
		response = present_question(win, question, ROUND_TIME)
		answer = hard_answers[round]
	else:
		present_text(win, 'No difficulty level chosen.', 'white', ROUND_TIME)
	# check answer
	accuracy = check_answer(response, answer)
	#  display points earned
	points_self = present_feedback(win, difficulty, accuracy)
	# fixation
	fixation_cross(win)

	# save data
	trial_log.write(
		trial_num,
		difficulty,
		question,
		answer,
		response, 
		accuracy,
		points_self
	)
	trial_num += 1
	total_points += points_self
	# trial end

t2 = time()
print('Task Complete.')
print('The task took %d minutes.'%((t2 - t1)/60))
print('Participant earned %d points for themselves.'%(total_points))
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
