import numpy as np
import json
from psychopy import visual, event
from time import time
import random

from utils.ui import (
    PointCounter,
    translate_condition_codes,
    fixation_cross,
    present_text,
    wait_for_keypress,
    determine_start,
    present_start_points,
    choose_difficulty,
    present_question,
    check_answer,
    determine_points_self,
    determine_confederates,
    present_practice_feedback,
    present_feedback,
    present_end_points,
)

from utils.write import CSVWriter_trial, CSVWriter_subj

from utils.triggerer import Triggerer

#### initialize some things

# parport triggers
parport = Triggerer(0)
parport.set_trigger_labels(
    [
        "baseline_start",
        "baseline_end",
        "choose_difficulty",
        "answer_question",
        "start_feedback",
        "end_feedback",
        "initial_points",
        "final_points",
    ]
)

# data handling
subj_num = input("Enter subject number: ")
subj_num = int(subj_num)
trial_log = CSVWriter_trial(subj_num)
subj_log = CSVWriter_subj(subj_num)
subj_cond = input("Enter subject condition: ")
subj_cond = translate_condition_codes(str(subj_cond))
subj_log.write(subj_num, subj_cond)
np.random.seed(subj_num)

# starting points
points_self, points_conf1, points_conf2 = determine_start(subj_cond)
self_point_counter = PointCounter(player="You", starting_points=points_self)
conf1_point_counter = PointCounter(player="Player 2", starting_points=points_conf1)
conf2_point_counter = PointCounter(player="Player 3", starting_points=points_conf2)
total_points_self = points_self
total_points_conf1 = points_conf1
total_points_conf2 = points_conf2
trial_num = 1
n_wrong = 0
n_correct = 0

# read in question and answer lists
with open("trivia_questions.json") as f:
    all_qs = json.load(f)

super_easy_qs = all_qs["super_easy_qs"]
easy_qs = all_qs["easy_qs"]
medium_qs = all_qs["medium_qs"]
hard_qs = all_qs["hard_qs"]
super_hard_qs = all_qs["super_hard_qs"]

random.shuffle(easy_qs)
random.shuffle(medium_qs)
random.shuffle(hard_qs)

# psychopy viz
win = visual.Window(
    size=(1920, 1080),
    color=(0, 0, 0),
    colorSpace="rgb255",
    screen=2,
    units="norm",
    fullscr=False,
    pos=(0, 0),
    allowGUI=False,
)


BASELINE_TIME = 300  # 5 minutes (300s)
DIFFICULTY_WAIT_TIME = 30  # 30s to choose difficulty
ROUND_TIME = 20  # 20s to answer question
N_ROUNDS = 8  # 8 rounds total
START_DISPLAY_TIME = 6  # 6s for display of initial points
END_DISPLAY_TIME = 5  # 5s for display of end points
FEEDBACK_DISPLAY_TIME = 5  # 5s for display of trial feedback


########################
# Baseline Physio
########################

# Instructions
txt = """
Now we are going to collect a 5-minute baseline measurement for the ECG. 
Sit comfortably, relax and breathe normally. \n
Press the spacebar when you're ready to begin.
"""
wait_for_keypress(win, txt)

# Get Baseline Physio
parport.send_trigger("baseline_start")
present_text(win=win, text_block="Relax", text_col="white", display_time=BASELINE_TIME)
parport.send_trigger("baseline_end")

########################
# Trivia Task
########################

t1 = time()

# Instructions
txt = """
In the present study, you will first play a Trivia game during which you 
are able to earn raffle tickets for a lucky draw to earn a 100 dollar Amazon gift card. 
  \n
Press the spacebar to continue.
"""
wait_for_keypress(win, txt)

txt = """
You will be given an initial amount of tickets and depending on your 
performance in the game you will either win or lose some tickets.  \n
Press the spacebar to continue.
"""
wait_for_keypress(win, txt)

txt = """
You will play a total of eight rounds simultaneously with the two other players, 
although your outcome will not be influenced by their performance.\n
Press the spacebar to continue.
"""
wait_for_keypress(win, txt)

txt = """
Next, you will be asked to complete a short survey on the computer 
pertaining to your experience of playing the game and provide some
 feedback on the game for future sessions. 
 \n
Press the spacebar to continue.
"""
wait_for_keypress(win, txt)

txt = """
We will begin with some practice questions to get you used 
to the trivia answering format. You will have 10 seconds to answer each question. \n
Press the spacebar to continue.
"""
wait_for_keypress(win, txt)

txt = """
To answer the questions you will type your answers and press enter. 
Numbers and letters are appropriate and spelling does count. \n
Press the spacebar when you're ready to begin.
"""
wait_for_keypress(win, txt)

# Practice Questions
practice_qs = [
    # easy q
    {
        "difficulty": "easy",
        "question": "How many legs does a spider have?",
        "answers": ["8", "eight"],
    },
    # medium q
    {
        "difficulty": "medium",
        "question": "What food do pandas eat?",
        "answers": ["bamboo"],
    },
    # hard q
    {
        "difficulty": "hard",
        "question": "How many bones do sharks have?",
        "answers": ["0", "zero", "none"],
    },
]
for q in practice_qs:
    question = q["question"]
    answer = q["answers"]
    response = present_question(win, question, ROUND_TIME)
    accuracy = check_answer(response, answer)
    present_practice_feedback(win, accuracy, q["difficulty"], FEEDBACK_DISPLAY_TIME)

# Run Trivia Task

# present starting state
parport.send_trigger("initial_points")
present_start_points(
    win, total_points_self, total_points_conf1, total_points_conf2, START_DISPLAY_TIME
)

# cycle through rounds
for round in range(1, N_ROUNDS + 1, 1):
    # choose difficulty
    parport.send_trigger("choose_difficulty")
    difficulty = choose_difficulty(
        win,
        DIFFICULTY_WAIT_TIME,
        round,
        self_point_counter,
        conf1_point_counter,
        conf2_point_counter,
    )
    # present question and get response
    if difficulty == "easy":
        # if got 4 easy questions wrong in a row show super easy q
        if n_wrong < 4:
            q_chosen = easy_qs.pop()
            question = q_chosen["question"]
            answer = q_chosen["answers"]
            parport.send_trigger("answer_question")
            response = present_question(win, question, ROUND_TIME, round)
        else:
            q_chosen = super_easy_qs.pop()
            question = q_chosen["question"]
            answer = q_chosen["answers"]
            parport.send_trigger("answer_question")
            response = present_question(win, question, ROUND_TIME, round)
    elif difficulty == "medium":
        q_chosen = medium_qs.pop()
        question = q_chosen["question"]
        answer = q_chosen["answers"]
        parport.send_trigger("answer_question")
        response = present_question(win, question, ROUND_TIME, round)
    elif difficulty == "hard":
        # if got 4 hard questions correct in a row show super hard q
        if n_correct < 4:
            q_chosen = hard_qs.pop()
            question = q_chosen["question"]
            answer = q_chosen["answers"]
            parport.send_trigger("answer_question")
            response = present_question(win, question, ROUND_TIME, round)
        else:
            q_chosen = super_hard_qs.pop()
            question = q_chosen["question"]
            answer = q_chosen["answers"]
            parport.send_trigger("answer_question")
            response = present_question(win, question, ROUND_TIME, round)
    else:
        present_text(win, "No difficulty level chosen.", "white", ROUND_TIME)
    # check answer and determine point changes
    accuracy = check_answer(response, answer)
    # decide to conditionally present super easy/super hard qs
    if (difficulty == "easy") & (accuracy == 1):
        n_wrong = 0
    elif (difficulty == "easy") & (accuracy == 0):
        n_wrong += 1
    elif (difficulty == "hard") & (accuracy == 0):
        n_correct = 0
    elif (difficulty == "hard") & (accuracy == 1):
        n_correct += 1
    # determine point changes
    points_self = determine_points_self(accuracy, difficulty)
    self_point_counter.update_points(points_self)
    total_points_self += points_self
    points_conf1, points_conf2 = determine_confederates(
        total_points_self, total_points_conf1, total_points_conf2, subj_cond, round
    )
    conf1_point_counter.update_points(points_conf1)
    conf2_point_counter.update_points(points_conf2)
    total_points_conf1 += points_conf1
    total_points_conf2 += points_conf2
    #  display points earned
    parport.send_trigger("start_feedback")
    present_feedback(
        win,
        difficulty,
        accuracy,
        points_self,
        total_points_self,
        points_conf1,
        points_conf2,
        total_points_conf1,
        total_points_conf2,
        FEEDBACK_DISPLAY_TIME,
        round,
    )
    parport.send_trigger("end_feedback")
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
        points_conf2,
    )
    trial_num += 1

    # trial end

# end state
parport.send_trigger("final_points")
present_end_points(
    win, total_points_self, total_points_conf1, total_points_conf2, END_DISPLAY_TIME
)

t2 = time()
print("Task Complete.")
print("The task took %d minutes." % ((t2 - t1) / 60))
print("Participant earned %d points for themselves." % (total_points_self))
# print('Participant earned %d points for the next participant.'%(points_other))

##########################
# and we're done!
##########################
txt = """
That’s all! You can press the space bar to end the experiment. 
Please let the experimenter know that you are done.
"""
wait_for_keypress(win, txt)
