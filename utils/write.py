import os


class CSVWriter_trial:

    def __init__(self, subj_num, dir = 'logs'):
        '''
        opens a file in which to log subject history
        '''
        if not os.path.exists(dir):
            os.makedirs(dir)
        fpath = os.path.join(dir, 'subject%d_trial_dat.csv'%subj_num)
        self._f = open(fpath, 'w')
        self._f.write('trial_num,difficulty,question,answer,response,accuracy,points_earned,conf1_points,conf2_points')

    def write(self, trial_num, difficulty, question, answer, response, accuracy, points_earned, conf1_points, conf2_points):
        '''
        writes a trial's parameters to log
        '''

        line = '\n%i,%s,%s,%s,%s,%f,%f,%i,%i'%(
            trial_num, difficulty, question, answer, response, accuracy, points_earned, conf1_points, conf2_points)
        self._f.write(line)

    def close(self):
        self._f.close()

    def __del__(self):
        self.close()


class CSVWriter_subj:

    def __init__(self, subj_num, dir = 'logs'):
        '''
        opens a file in which to log subject history
        '''
        if not os.path.exists(dir):
            os.makedirs(dir)
        fpath = os.path.join(dir, 'subject%d_subj_dat.csv'%subj_num)
        self._f = open(fpath, 'w')
        self._f.write('subj_id,condition')

    def write(self, subj_num, subj_cond):
        '''
        writes a trial's parameters to log
        '''

        line = '\n%i,%s'%(
            subj_num, subj_cond)
        self._f.write(line)

    def close(self):
        self._f.close()

    def __del__(self):
        self.close()