
# move into test_space 
# enter python


# loads sample code
import json
with open("motion_surface=abs_shape=butter_a=0_v=10_i=0.000_s=0.000_t=0.000.json") as data_file:    
        data = json.load(data_file)

# loads training data
        json_filepath = '/home/harry/Projects/butter_json/data_training.json'
with open(filepath) as data_file:    
		data = json.load(data_file)

# drawing shapes and pusher special case butter 

# def rigidbodytransform(shape, XYtheta):
# 	temp = (len(shape), 2)
# 	transformed = np.zeros(temp)

# 	for i in range(len(shape)):
# 		for j in range(2):
# 			if(j==0):
# 				transformed[i][j] = np.cos(dataXYtheta[i][j+2])*dataXYtheta[i][j] - np.sin(theta)*dataXYtheta[i][j+1] + dataXYtheta[i][j]
# 			else(j==1):
# 				transformed[i][j] = np.sin(dataXYtheta[i][j+2])*dataXYtheta[i][j-1] + np.cos(theta)*dataXYtheta[i][j] + dataXYtheta[i][j]

from config.shape_db import *
import matplotlib.pyplot as plt
import tf.transformations as tfm

shape_id = 'butter'
probe_radius = 0.004745

shape_db = ShapeDB()
shape_polygon = shape_db.shape_db[shape_id]['shape'][0]
pred = predictions[0].T

def rigidtransform(shape, xytheta): #takes in 2d array of shapes coordinates wrt object frame and xytheta transform vector
	temp = (len(shape), 2)
	transformed = np.zeros(temp)

	for i in range(len(shape)):
	    for j in range(2):
	        if(j==0):
	            transformed[i][j] = (np.cos(xytheta[0][j+2])*shape[i][j]) - (np.sin(xytheta[0][j+2])*shape[i][j+1]) + xytheta[0][j]
	        else:
	            transformed[i][j] = (np.sin(xytheta[0][j+1])*shape[i][j-1]) + (np.cos(xytheta[0][j+1])*shape[i][j]) + xytheta[0][j]

	return transformed

def plottransformed_obj(shapetransformed)
	plt.plot(np.array(shapetransformed)[:,0], np.array(shapetransformed)[:,1])
    plt.axis('equal')
    plt.show()

    
