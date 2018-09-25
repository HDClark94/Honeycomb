#!/usr/bin/env python

# Harry Clark 2017
# sync times, pull training data

# preprocessing script with parameters explained below, produces a non random bounds vector wrt the object frame 
# and each push only produces a single data vector for training

import numpy as np
import json

import matplotlib
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
from matplotlib.collections import PatchCollection

from config.shape_db import *

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
	training_set = []
	time_interval = len(ft)-1 # 1000ms
	print len(ft)
	for i in range(0, len(ft)-time_interval, time_interval): # change step for number of samples per file
	#--------X-------
		tip_sx = tip_pose[i][0] #1 [0] 
		tip_sy = tip_pose[i][1] #2 [1]
		tip_ex = tip_pose[i+time_interval][0] #3 [2]
		tip_ey = tip_pose[i+time_interval][1] #4 [3]

		object_sx = object_pose[i][0] #5 [4]
		object_sy = object_pose[i][1] #6 [5]
		object_stheta = object_pose[i][2] #7 [6]

	#-----Y---------
		object_ex = object_pose[i+time_interval][0] #8 [7]
		object_ey = object_pose[i+time_interval][1] #9 [8]
		object_etheta = object_pose[i+time_interval][2] #10 [9]

		sum_ft = np.sum(ft[i:i+time_interval], 0)
		sum_ftx = sum_ft[0] #11 [10]
		sum_fty = sum_ft[1] #12 [11]
		sum_ftt = sum_ft[2] #13 [12]

		training_seti = [tip_sx, tip_sy, tip_ex, tip_ey, object_sx, object_sy, object_stheta, object_ex, object_ey, object_etheta, sum_ftx, sum_fty, sum_ftt]
		training_set.append(training_seti)
	return training_set

def json2trainingdata(filepath, shape_db):
		
	with open(filepath) as data_file:    
		data = json.load(data_file)

		data_synced = resample_using_pandas(data)
		data_training_set = extract_training_dataset(data_synced)

		#shape_id = getfield_from_filename(filepath, 'shape')
		#shape_bounds = shape_db.shape_db[shape_id]['bounds']
		#shape_mass = shape_db.shape_db[shape_id]['mass']
		#shape_moi = shape_db.shape_db[shape_id]['moment_of_inertia']#moment of inertia

		#v = getfield_from_filename(filepath, 'v') #velocity
		#i = getfield_from_filename(filepath, 'i') #side number
		#s = getfield_from_filename(filepath, 's') #contact point position on that side 0 to 1
		#t = getfield_from_filename(filepath, 't') #contact angle in rad
		#vt = [float(v), float(t)]

		#xytheta = data_training_set[4:7] #xytheta from training set (size = 3)
		#transformed_bounds = rigidtransform(shape_bounds, xytheta) # sample bounds transformed to starter bounds

		# reshape to 1d vector
		#nptransformed_bounds = np.array(transformed_bounds)
		#nptransformed_bounds = np.reshape(nptransformed_bounds, np.prod(nptransformed_bounds.shape))
		#transformed_bounds = nptransformed_bounds.tolist()

		#data_training_set.extend(vt)
		#data_training_set.append(shape_mass)
		#data_training_set.append(shape_moi)
		#data_training_set.extend(transformed_bounds)

		# labels tip_sx[0], tip_sy[1], tip_ex[2], tip_ey[3], object_sx[4], object_sy[5], 
		# object_stheta[6], object_ex[7], object_ey[8], object_etheta[9], avg_ftx[10], avg_fty[11], avg_ftt[12], 
		# v[13], t[14], mass[15], moi[16],
		# 24 x and y values for shape boundary (total 48)

		# training_set has 48 + 17 elements (=65)

	return data_training_set



def main(argv):
	import glob
	filelist = glob.glob("%s/motion*.json" % argv[1])
	all_training_data = []
	#print filelist
	shape_db = ShapeDB()

	for json_filepath in filelist:
		# only process v=20
		# if json_filepath.find('v=20_') == -1:
			# continue	
		# try:
		a = getfield_from_filename(json_filepath, 'a') #acceleration
		v = getfield_from_filename(json_filepath, 'v') #velocity
		print a, v
		
		if (a == '0') and (v == '10'): 
			all_training_data.extend(json2trainingdata(json_filepath, shape_db))
			print 'len(all_training_data)', len(all_training_data)
			# except:
			# print json_filepath
			# pass
	
	outputfile= "%s/data_training_with_multidata_and_Force_6000ms.json" % argv[1]
	with open(outputfile, 'w') as outfile:
		json.dump(all_training_data, outfile, indent=4)

if __name__=='__main__':
	import sys
	main(sys.argv)
	
