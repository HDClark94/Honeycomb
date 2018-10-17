# -*- coding: utf-8 -*-
"""
    
    @author: Sarah Tennant
    
    Includes all core functions which are imported into main code for analysis.
    
    """

# Import packages
from Functions_Core_0100 import *
import matplotlib.pyplot as plt
import numpy as np
from scipy import stats
import math
from scipy.stats import uniform

def find_nearest(a, a0):
    "Element in nd array `a` closest to the scalar value `a0`"
    idx = np.abs(a - a0).argmin()
    return idx

def expression_set(mice, expression):
    #expession average per mouse
    counter = 1
    expression_mus = []
    for mcount,mouse in enumerate(mice):
        if(mouse == 'M1' or mouse == 'M3' or mouse == 'M4' or mouse == 'M11'):
            expression_mus.append(0)
        else:
            mouse_expression = np.delete(expression, np.where(expression[:, 0].astype(int) != mcount+1), 0)
            expression_mus.append(np.mean(mouse_expression[:,2]))
    return expression_mus

# takes trial from h5 format
def process_trials(mice, days, filename, expression_mus):
    trialtype_name = ['Beaconed', 'Non-Beaconed', 'Probe']
    l = 0

    # initialise empty trial list
    b_trials = []
    nb_trials = []
    p_trials = []

    b_trials_expression = []
    nb_trials_expression = []
    p_trials_expression = []

    b_mouse =[]
    nb_mouse = []
    p_mouse = []

    for mcount,mouse in enumerate(mice):
        try:
            for dcount,day in enumerate(days): #load mouse and day
                try:
                    print ('Processing...',day,mouse)
            
                    # initialise empty trial list
                    b_trials_temp = []
                    nb_trials_temp = []
                    p_trials_temp = []
                    b_trials_counter = 0
                    nb_trials_counter = 0
                    p_trials_counter = 0
            
                    #load HDF5 data set for that day and mouse
                    saraharray = readhdfdata(filename,day,mouse,'raw_data')
            
                    # make array of trial number per row of data in dataset
                    trialarray = maketrialarray(saraharray) # make array of trial number same size as saraharray
                    saraharray[:,9] = trialarray[:,0] # replace trial number because of increment error (see README.py)
            
                    trarray = np.arange(np.min(saraharray[:,9]),np.max(saraharray[:,9]),1) #array of trial number
                    trialno = np.max(saraharray[:,9]) # total number of trials for that day and mouse
                    print("total trials for",mouse, "=", int(trialno))
            
                    for j in trarray:
                        trial = np.delete(saraharray, np.where(saraharray[:, 9] != j), 0)   # select trial
                        trial_location = trial[:, np.r_[1]]                               # location vector for each trial
                        trial_time =     trial[:, np.r_[0]]-trial[0][0]                   # standardize time vector for each trial
                        trialtype = trial[0, 8] # 0 = beaconed, 10 = non-beaconed, 20 = probe # trial type
                        trial = np.column_stack((trial_time, trial_location))             # location and time matrix
            
                        # assign trial per category
                        if (trialtype == 0):
                            b_trials.append(trial)
                            b_trials_temp.append(trial)
                            b_trials_counter +=1
                            b_trials_expression.append(expression_mus[mcount])
                            b_mouse.append(mouse)
                    
                        elif (trialtype == 10):
                            nb_trials.append(trial)
                            nb_trials_temp.append(trial)
                            nb_trials_counter += 1
                            nb_trials_expression.append(expression_mus[mcount])
                            nb_mouse.append(mouse)
        
                        elif (trialtype == 20):
                            p_trials.append(trial)
                            p_trials_temp.append(trial)
                            p_trials_counter += 1
                            p_trials_expression.append(expression_mus[mcount])
                            p_mouse.append(mouse)
        
                    print("beaconed trials = ",b_trials_counter)
                    print("non-beaconed trials = ",nb_trials_counter)
                    print("probe trials = ",p_trials_counter)
        
                    trialtype_counter = 0
                    for trialtype in [b_trials_temp, nb_trials_temp, p_trials_temp]:
                        if len(trialtype) != 0:
                            for i in range(len(trialtype)):
                                trial = trialtype[i]
                                plt.plot(trial[:,np.r_[0]], trial[:,np.r_[1]])
                                plt.xlabel('Time')
                                plt.ylabel('Location')
                                plt.title((mouse, day, trialtype_name[trialtype_counter]))
                        plt.show()
                        trialtype_counter += 1
            
    
                    l += trialno
                    print("total trials = ", int(l))
                except Exception:
                    pass
        except Exception:
            pass
    
    return [b_trials, nb_trials, p_trials], [b_trials_expression, nb_trials_expression, p_trials_expression], [b_mouse, nb_mouse, p_mouse]

#gives trial set same length per trial, trials expressed as time point at each location on virtual track
def resample_trials(trials, sample_rate, track_length):
    # track length in virtual units
    # sample_rate in virtual units
    # change decimals to match sample_rate
    rs_trials  =[]
    for j in range(len(trials)):
        # initialise array to be filled by timings
        resampled = np.column_stack((np.arange(0,track_length,sample_rate),np.arange(0,track_length,sample_rate)))
        #loop over highly sampled location to find time at which mouse was at location
        i = 0
        for locale in np.round(np.arange(0,track_length,sample_rate), decimals=3):
            closest_location_index = find_nearest(np.round(trials[j][:,1],decimals=1),locale)
            time = trials[j][closest_location_index,0]
            resampled[i,1] = trials[j][closest_location_index,0]
            i += 1
        rs_trials.append(resampled)
    return rs_trials