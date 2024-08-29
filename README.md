# inequality_trivia

To run this task script:

1. Navigate to the directory with the experiment.py script in it.
2. activate the indicated conda environment (e.g., "inequality_trivia")
3. type `sudo modprobe -r lp` in the terminal and enter the computer password when prompted
4. type in `sudo chmod 777 /dev/parport0` in the terminal. You should not have to re-enter the password.
5. type in `python experiment.py` in the terminal to call the main experiment script.
6. When prompted, type in the subject number (must be numerical).
7. When prompted, type in the experiment condition. The only valid options are the following strings:
    - "shark" for the inequality condition
    - "whale" for the equality condition
    - "seal" for the meritocracy condition

Collected experiment data will be saved by subject id in the logs directory.
