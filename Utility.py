import sys
import numpy as np
import matplotlib.pyplot as plt
import time

def TimeFormat(CalcTime):
    RET = "error"
    if CalcTime < 60: RET = "{:.2f}s".format(CalcTime%60)
    elif CalcTime < 60*60: RET = str(int(CalcTime/(60)%60))+"m "+"{:.2f}s".format(CalcTime%60)
    else: RET = str(int(CalcTime/(60*60)))+"h "+str(int(CalcTime/(60)%60))+"m "+"{:.2f}s".format(CalcTime%60)
    return RET

class Tracker:
    def __init__(self):
        self.start_time = time.time()
        self.stringlength = 64
    def FLUSH(self,i,I):
        '''Display percentage of completion'''
        try: percentage = i/I
        except: percentage = 0
        tim = time.time() - self.start_time
        try: remaining_tim = TimeFormat(tim / percentage * (1 - percentage))
        except: remaining_tim = "unknown time"
        text = "\r"+"{:.2f}% done ({}/{}) ".format(percentage*100,i,I)+remaining_tim+" remaining "
        sys.stdout.write(text + " "*(self.stringlength-len(text)))
        sys.stdout.flush()
    def FLUSH_Final(self,i,I):
        '''Display Final percentage of completion'''
        try: percentage = i/I
        except: percentage = 0
        tim = time.time() - self.start_time
        text = "\r"+"{:.2f}% done ({}/{}) after ".format(percentage*100,i,I,tim)+TimeFormat(tim)
        sys.stdout.write(text + " "*(self.stringlength-len(text)))
        sys.stdout.flush()
    def START(self):
        self.start_time = time.time()

def bootstrap(s,nbs):
    '''bootstrap algorithm for error estimation

        Input:  trajectory s
                number of bootstrap elements nbs

        Return: boostrap estimate for the error of mean(s)'''
    return s[np.random.randint(s.size,size=(nbs,s.size))].mean(axis=1).std()