import numpy as np
import json
from psychopy import visual, event
from time import time
import random

from utils.ui import (
    fixation_cross,
    present_text,
    wait_for_keypress,
    determine_start,
    present_start_points,
    choose_difficulty,
    present_question,
    check_answer,
    determine_points_self,
    #determine_confederates,
	present_practice_feedback,
    present_feedback,
    present_end_points
)

def determine_confederates(total_points_self, total_points_conf1, total_points_conf2, condition, round_num):
	'''
	Determine the confederates' choices and points for the trial.
	'''
	# rounds when both confederates succeed
	if round_num in [0, 1, 4, 5, 8]:
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
	
	# rounds when confederate 1 fails
	elif round_num in [2, 6]:
		conf1_points = -1
		# for unequal end state
		if condition != 'equality':
			# confederate 2
			if total_points_conf2 <= total_points_self + 20:
				conf2_points = 5
			elif (total_points_conf2 > total_points_self + 20) & (total_points_conf2 < total_points_self + 30):
				conf2_points = 3
			else:
				conf2_points = 1
		# for equal end state
		elif condition == 'equality':
			# confederate 2
			if total_points_conf2 <= total_points_self - 3:
				conf2_points = 5
			elif (total_points_conf2 > total_points_self - 3) & (total_points_conf2 < total_points_self + 2):
				conf2_points = 3
			else:
				conf2_points = 1
	
	# round when confederate 2 fails
	elif round_num in [3, 7]:
		conf2_points = -1
		# for unequal end state
		if condition != 'equality':
			# confederate 1
			if total_points_conf1 <= total_points_self + 10:
				conf1_points = 5
			elif (total_points_conf1 > total_points_self + 10) & (total_points_conf1 < total_points_self + 15):
				conf1_points = 3
			else:
				conf1_points = 1
		# for equal end state
		elif condition == 'equality':
			# confederate 1
			if total_points_conf1 <= total_points_self - 5:
				conf1_points = 5
			elif (total_points_conf1 > total_points_self - 5) & (total_points_conf1 < total_points_self + 2):
				conf1_points = 3
			else:
				conf1_points = 1
	
	return (conf1_points, conf2_points)




from utils.write import (
    CSVWriter_trial,
	CSVWriter_subj
) 

from utils.triggerer import Triggerer

#### initialize some things

# parport triggers
parport = Triggerer(0)
parport.set_trigger_labels(['baseline_start', 'baseline_end',
			     'choose_difficulty', 'answer_question',
				   'start_feedback', 'end_feedback', 
 					'initial_points', 'final_points'])

# data handling
subj_num = input("Enter subject number: ")
subj_num = int(subj_num)
trial_log = CSVWriter_trial(subj_num)
subj_log = CSVWriter_subj(subj_num)
subj_cond = input("Enter subject condition: ")
subj_cond = str(subj_cond)
subj_log.write(subj_num, subj_cond)
np.random.seed(subj_num)

# starting points
points_self, points_conf1, points_conf2 = determine_start(subj_cond)
total_points_self = points_self
total_points_conf1 = points_conf1
total_points_conf2 = points_conf2
trial_num = 1
n_wrong = 0
n_correct = 0

# read in question and answer lists
with open('trivia_questions.json') as f:
    all_qs = json.load(f)

super_easy_qs = all_qs['super_easy_qs']
easy_qs = all_qs['easy_qs']
medium_qs = all_qs['medium_qs']
hard_qs = all_qs['hard_qs']
super_hard_qs = all_qs['super_hard_qs']

random.shuffle(easy_qs)
random.shuffle(medium_qs)
random.shuffle(hard_qs)

# psychopy viz
win = visual.Window(
	size = (1920, 1080),
	color = (0, 0, 0),
	colorSpace = 'rgb255',
	units = "norm",
	fullscr = False,
	pos = (0, 0),
	allowGUI = False
	)



BASELINE_TIME = 3 # 5 minutes (300s)
DIFFICULTY_WAIT_TIME = 30 # 30s to choose difficulty
ROUND_TIME = 10 # 30s to answer question
N_ROUNDS = 5 # 8 rounds total
START_DISPLAY_TIME = 3
END_DISPLAY_TIME = 3
FEEDBACK_DISPLAY_TIME = 5


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
parport.send_trigger('baseline_start')
present_text(win, 'Relax', BASELINE_TIME)
parport.send_trigger('baseline_end')

########################
# Trivia Task
########################

t1 = time()

# Run Trivia Task

# present starting state
parport.send_trigger('initial_points')
present_start_points(win, total_points_self, total_points_conf1, total_points_conf2, START_DISPLAY_TIME)

# cycle through rounds
for round in range(1, N_ROUNDS+1, 1):
    # choose difficulty
	parport.send_trigger('choose_difficulty')
	difficulty = choose_difficulty(win, DIFFICULTY_WAIT_TIME, round)
    # present question and get response
	if difficulty == 'easy':
		# if got 4 easy questions wrong in a row show super easy q
		if n_wrong < 4:
			q_chosen = easy_qs.pop()
			question = q_chosen['question']
			answer = q_chosen['answers']
			parport.send_trigger('answer_question')
			response = present_question(win, question, ROUND_TIME, round)
		else:
			q_chosen = super_easy_qs.pop()
			question = q_chosen['question']
			answer = q_chosen['answers']
			parport.send_trigger('answer_question')
			response = present_question(win, question, ROUND_TIME, round)
	elif difficulty == 'medium':
		q_chosen = medium_qs.pop()
		question = q_chosen['question']
		answer = q_chosen['answers']
		parport.send_trigger('answer_question')
		response = present_question(win, question, ROUND_TIME, round)
	elif difficulty == 'hard':
		# if got 4 hard questions correct in a row show super hard q
		if n_correct < 4:
			q_chosen = hard_qs.pop()
			question = q_chosen['question']
			answer = q_chosen['answers']
			parport.send_trigger('answer_question')
			response = present_question(win, question, ROUND_TIME, round)
		else:
			q_chosen = super_hard_qs.pop()
			question = q_chosen['question']
			answer = q_chosen['answers']
			parport.send_trigger('answer_question')
			response = present_question(win, question, ROUND_TIME, round)
	else:
		present_text(win, 'No difficulty level chosen.', 'white', ROUND_TIME)
	# check answer and determine point changes
	accuracy = check_answer(response, answer)
	# decide to conditionally present super easy/super hard qs
	if (difficulty == 'easy') & (accuracy == 1):
		n_wrong = 0
	elif (difficulty == 'easy') & (accuracy == 0):
		n_wrong += 1
	elif (difficulty == 'hard') & (accuracy == 0):
		n_correct = 0
	elif (difficulty == 'hard') & (accuracy == 1):
		n_correct += 1
	# determine point changes
	points_self = determine_points_self(accuracy, difficulty)
	total_points_self += points_self
	points_conf1, points_conf2 = determine_confederates(total_points_self, total_points_conf1, total_points_conf2, subj_cond, round)
	total_points_conf1 += points_conf1
	total_points_conf2 += points_conf2
	#  display points earned
	parport.send_trigger('start_feedback')
	present_feedback(win, difficulty, accuracy, points_self, total_points_self, 
		     points_conf1, points_conf2, total_points_conf1, total_points_conf2, FEEDBACK_DISPLAY_TIME, round)
	parport.send_trigger('end_feedback')
	# fixation
	fixation_cross(win)

	# save data
	trial_log.write(
		trial_num,
		difficulty,
		question,
		answer[0],
		str.rstrip(response), 
		accuracy,
		points_self,
		points_conf1,
		points_conf2
	)
	trial_num += 1
	
	# trial end

# end state
parport.send_trigger('final_points')
present_end_points(win, total_points_self, total_points_conf1, total_points_conf2, END_DISPLAY_TIME)

t2 = time()
print('Task Complete.')
print('The task took %d minutes.'%((t2 - t1)/60))
print('Participant earned %d points for themselves.'%(total_points_self))
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
