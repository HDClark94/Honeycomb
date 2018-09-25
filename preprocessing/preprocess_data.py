#!/usr/bin/env python

# Harry Clark 2017
# sync times, pull training data

import numpy as np
import json

import matplotlib
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
from matplotlib.collections import PatchCollection

from config.shape_db import ShapeDB

import tf.transformations as tfm
from ik.helper import *
from config.helper import *
from matplotlib.pyplot import savefig
import time

from mpl_toolkits.mplot3d import Axes3D

import pandas as pd

# resamples, interpolates and time syncs tip pose, object pose and force measurements
# each measurement sample is 10ms apart starting from the same time sample
def resample_using_pandas(data):

	tip_pose = data['tip_pose']
	object_pose = data['object_pose']
	ft = data['ft_wrench']
	
	# maximum time range shared between the tip, object and force measurements
	starttime = max(tip_pose[0][0], object_pose[0][0], ft[0][0])
	endtime = min(tip_pose[-1][0], object_pose[-1][0], ft[-1][0])
	pd_starttime = pd.to_datetime(starttime, unit='s')
	pd_endtime = pd.to_datetime(endtime, unit='s')

	# tip
	tip_pose_dt = pd.to_datetime(np.array(tip_pose)[:,0].tolist(), unit='s')
	tip_pose = pd.DataFrame(np.array(tip_pose)[:,1:4].tolist(), index=tip_pose_dt)
	tip_pose_resampled = tip_pose.resample('10ms', how='mean')
	tip_pose_interp = tip_pose_resampled.interpolate()

	start_ = tip_pose_interp.index.searchsorted(pd_starttime)
	end_ = tip_pose_interp.index.searchsorted(pd_endtime)
	tip_pose_interp = tip_pose_interp.ix[start_:end_]
	tip_pose_interp_list = tip_pose_interp.values.tolist()

	# object
	object_pose_dt = pd.to_datetime(np.array(object_pose)[:,0].tolist(), unit='s')
	object_pose = pd.DataFrame(np.array(object_pose)[:,1:4].tolist(), index=object_pose_dt)
	object_pose_resampled = object_pose.resample('10ms', how='mean')
	object_pose_interp = object_pose_resampled.interpolate()

	start_ = object_pose_interp.index.searchsorted(pd_starttime)
	end_ = object_pose_interp.index.searchsorted(pd_endtime)
	object_pose_interp = object_pose_interp.ix[start_:end_]
	object_pose_interp_list = object_pose_interp.values.tolist()

	# force
	force_dt = pd.to_datetime(np.array(ft)[:,0].tolist(), unit='s')
	ft = pd.DataFrame(np.array(ft)[:,1:4].tolist(), index=force_dt)
	ft_resampled = ft.resample('10ms', how='mean')
	ft_interp = ft_resampled.interpolate()

	start_ = ft_interp.index.searchsorted(pd_starttime)
	end_ = ft_interp.index.searchsorted(pd_endtime)
	ft_interp = ft_interp.ix[start_:end_]
	ft_interp_list = ft_interp.values.tolist()

	# repackage
	data_resample = {}
	data_resample['tip_pose'] = tip_pose_interp_list
	data_resample['object_pose'] = object_pose_interp_list
	data_resample['ft'] = ft_interp_list

	return data_resample

# extracts training parameters, original conditions, end conditions
# FOR NOW, assuming data is recorded from first contact to end contact - may need revision

def extract_training_dataset(data):
	tip_pose = data['tip_pose']
	object_pose = data['object_pose']
	ft = data['ft']

	for i in range(len(tip_pose-1))
		

	#--------X-------
	tip_sx = tip_pose[0][0] #1 [0] 
	tip_sy = tip_pose[0][1] #2 [1]
	tip_ex = tip_pose[-1][0] #3 [2]
	tip_ey = tip_pose[-1][1] #4 [3]

	object_sx = object_pose[0][0] #5 [4]
	object_sy = object_pose[0][1] #6 [5]
	object_stheta = object_pose[0][2] #7 [6]

	#-----Y---------
	object_ex = object_pose[-1][0] #8 [7]
	object_ey = object_pose[-1][1] #9 [8]
	object_etheta = object_pose[-1][2] #10 [9]

	training_set = [tip_sx, tip_sy, tip_ex, tip_ey, object_sx, object_sy, object_stheta, object_ex, object_ey, object_etheta]
	return training_set

def json2trainingdata(filepath):
		
	with open(filepath) as data_file:    
		data = json.load(data_file)

		a = getfield_from_filename(filepath, 'a') #acceleration
		v = getfield_from_filename(filepath, 'v') #velocity
		i = getfield_from_filename(filepath, 'i') #side number
		s = getfield_from_filename(filepath, 's') #contact point position on that side 0 to 1
		t = getfield_from_filename(filepath, 't') #contact angle in rad

		avist = [float(a), float(v), float(i), float(s), float(t)]
		data_synced = resample_using_pandas(data)
		data_training_set = extract_training_dataset(data_synced)
		data_training_set.extend(avist)

	return data_training_set

def main(argv):
	import glob
	filelist = glob.glob("%s/motion*.json" % argv[1])
	all_training_data = []
	print filelist

	for json_filepath in filelist:
		# only process v=20
		# if json_filepath.find('v=20_') == -1:
			# continue
			
		# try:
		all_training_data.append(json2trainingdata(json_filepath))
		print 'len(all_training_data)', len(all_training_data)
		# except:
			# print json_filepath
			# pass
	
	outputfile= "%s/data_training.json" % argv[1]
	with open(outputfile, 'w') as outfile:
		json.dump(all_training_data, outfile, indent=4)

if __name__=='__main__':
	import sys
	main(sys.argv)
	
