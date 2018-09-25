import math
import numpy as np
import random
from scipy import special
import matplotlib.pyplot as plt
# The coordinates are wrt the object frame
# The polygon shape must be in counterclock-wise order for the simplicity of finding normals
# The slot is for moving the object back

#-------------------added 22062017-----------------------------------------------------
def rigidtransform(shape, xytheta): #takes in 2d array of shapes coordinates wrt object frame and xytheta transform vector
    shape = np.array(shape)

    if (shape.ndim == 2): 
        temp = (len(shape), 2)
        transformed = np.zeros(temp)

        for i in range(len(shape)):
            for j in range(2):
                if(j==0):
                    transformed[i][j] = (np.cos(xytheta[j+2])*shape[i][j]) - (np.sin(xytheta[j+2])*shape[i][j+1]) + xytheta[j]
                else:
                    transformed[i][j] = (np.sin(xytheta[j+1])*shape[i][j-1]) + (np.cos(xytheta[j+1])*shape[i][j]) + xytheta[j]
        
        return transformed.tolist()

    elif (shape.ndim == 1): # input vector case, consecutive x and ys
        transformed = np.zeros(len(shape))

        for i in range(len(shape)):
            if (i%2 == 0): # odd cases, x cases
                transformed[i] = (np.cos(xytheta[2])*shape[i]) - (np.sin(xytheta[2])*shape[i+1]) + xytheta[0]
            else: # even cases, y cases
                transformed[i] = (np.sin(xytheta[2])*shape[i-1]) + (np.cos(xytheta[2])*shape[i]) + xytheta[1]

        return transformed.tolist()


def plottransformed_obj(shapetransformed, colour, fade):
    plt.plot(np.array(shapetransformed)[:,0], np.array(shapetransformed)[:,1], colour, alpha = fade)
    plt.axis('equal')

def plottransformed_pusher(pusherX, pusherY, radius, colour):
    ax = plt.gca()
    pusher = plt.Circle((pusherX, pusherY), radius, color = colour, fill=False)
    ax.add_artist(pusher)

#---------120712--------------------------------------------------------
def sampleShape(polyArray, sampleSize, ranBound):
    if (sampleSize%12 != 0):
        print "sampleSize must be multiple of 12"
    sample_per_side = int(sampleSize/len(polyArray)) # sampleSize must be mutliple of 12
    shapeArray = []
    if (len(polyArray) != 1):
        polyArray.append(polyArray[0])
        for i in range(len(polyArray)-1):
            Xs = np.linspace(polyArray[i][0], polyArray[i+1][0], num=sample_per_side, endpoint=False)
            Ys = np.linspace(polyArray[i][1], polyArray[i+1][1], num=sample_per_side, endpoint=False)
            #euclidian_distance = np.sqrt((np.sq(polyArray[i][0]-polyArray[i+1][0]) + np.sq(polyArray[i][1]-polyArray[i+1][1])))
            for j in range(len(Xs)):
                shapeArray.append(Xs[j])
                shapeArray.append(Ys[j])
        del polyArray[-1]

    else:
        shapeArray = []
        Xs = []
        Ys = []
        a = polyArray[0][1] #must be axis major for ellips
        b = polyArray[0][0] # must be axis minor for ellips
        m = 1-(float(np.square(b))/float(np.square(a)))
        c= 4*a*special.ellipe(m)
        phis = np.linspace(0, 2*np.pi, 100000)

        for k in range(sampleSize):
            arc_length = (float(k)/sampleSize)*c
            counter = 0
            arc_estimates = np.zeros(len(phis))
            for phi in phis: #numerical method to solve inverse, number of steps changes sensitivity
                arc_estimates[counter] = a*(special.ellipeinc(phi, m))
                counter += 1
            idx = (np.abs(arc_estimates-arc_length)).argmin()
            best_phi = phis[idx]
            Xs.append(a*np.sin(best_phi))
            Ys.append(b*np.cos(best_phi))
        
        # flip elements so bounds is counter clockwise
        Xs = np.array(list(reversed(Xs)))
        Ys = np.array(list(reversed(Ys)))

        for j in range(len(Xs)):
            shapeArray.append(Xs[j])
            shapeArray.append(Ys[j])

        shapeArray = rigidtransform(shapeArray, [0,0,1.5708]) # 90 degree correct for ellipses
    
    # random permutation of shapeArray vector, allows for non localised geometric assumptions
    newShapeArray = np.zeros(sampleSize*2)

    if (ranBound == True):
        ran_ord = np.random.permutation(range(sampleSize))
    elif (ranBound == False):
        ran_ord = range(sampleSize)

    counter = 0
    for i in range(sampleSize):
        r_i = ran_ord[i]
        newShapeArray[counter] = shapeArray[r_i*2]
        counter += 1
        newShapeArray[counter] = shapeArray[(r_i*2) +1]
        counter += 1 
    shapeArray = newShapeArray
            
    return shapeArray

def sampleButter(butterPoly, sampleSize, ranBound):
    butterLength = len(butterPoly[0])
    sampleFreq = int(round(float(butterLength)/sampleSize))
    shapeArray = []
    counter = 0
    for i in range(sampleSize):
        shapeArray.append(butterPoly[0][counter][0])
        shapeArray.append(butterPoly[0][counter][1])
        counter += sampleFreq

    # random permutation of shapeArray vector, allows for non localised geometric assumptions
    newShapeArray = np.zeros(sampleSize*2)

    if (ranBound == True):
        ran_ord = np.random.permutation(range(sampleSize))
    elif (ranBound == False):
        ran_ord = range(sampleSize)
    
    counter = 0
    for i in range(sampleSize):
        r_i = ran_ord[i]
        newShapeArray[counter] = shapeArray[r_i*2]
        counter += 1
        newShapeArray[counter] = shapeArray[(r_i*2) +1]
        counter += 1 
    shapeArray = newShapeArray    

    return shapeArray #should be 1d


def organiseBounds(nptransformed_bounds, xytheta):
    # find closest point to most vertical point above shape centre
    counter = 1
    minDist = 1000 # arbitatily big
    minIdx = 1000 # arbitatily big
    for i in range(len(nptransformed_bounds)/2):
        y = nptransformed_bounds[counter]
        x = nptransformed_bounds[counter-1]
        if (y>xytheta[1]) and (np.abs(xytheta[0]-x)<minDist):
            minDist = np.abs(xytheta[0]-x)
            minIdx = counter
        counter += 2
    #minIdx note denotes the index of the point that should begin the reorganised vector
    newNpTransformed_bounds = np.zeros(np.shape(nptransformed_bounds))
    counter = minIdx-1 #counter starts at x
    for i in range(len(nptransformed_bounds)):
        if (counter==len(nptransformed_bounds)):
            counter = 0
        newNpTransformed_bounds[i] = nptransformed_bounds[counter]
        counter += 1

    nptransformed_bounds = newNpTransformed_bounds
    return nptransformed_bounds


#------------------------------------------------------------------------

def makeShapePolyRect(longSide, shortSide):
    a = longSide / 2.0
    b = shortSide / 2.0
    return [[a,b], [-a,b], [-a,-b], [a,-b]]
    
def makeShapePolyTri(shortSide1, shortSide2, longSide):
    a = shortSide1
    b = shortSide2
    c = longSide
    d = 0.090 / 2.0  # from the rectangle coordinate system
    
    return [[d, d], [d-b,d], [d,d-a]]

def makeShapeEllip(a, b):
    return [[a, b]]

def makeShapePolyNGon(side, n):
    poly = []
    for i in range(n):
        theta = (2*math.pi/n)*i
        poly.append([side*math.cos(theta), side*math.sin(theta)])
    return poly

import copy
def processButtShape(shape):
    ss = shape[0]
    ss = ss[:len(ss)/2]
    total = np.array([0,0])
    
    for i in range(len(ss)):
        total = total + np.array(ss[i])
        
    center = total / len(ss)
    tmp = copy.deepcopy(ss)
    for i in range(len(ss)):
        ss[i] = ((np.array(tmp[len(tmp)-i-1]) - np.array(center)) / 1000.0).tolist()
    
    ydel = ss[0][1]
    xdel = (ss[0][0] + ss[-1][0]) / 2
    for i in range(len(ss)):
        ss[i][1] -= ydel
        ss[i][0] -= xdel
    
    nss = len(ss)
    for i in range(nss):
       ss.append([-ss[i][0], -ss[i][1]])
    
    newss = []
    # remove redundant
    for s in ss:
       if not(len(newss) > 0 and (s[0] == newss[-1][0] and s[1] == newss[-1][1])):
           newss.append(s)
    ss = newss
    #print np.max(np.array(ss)[:,0]) - np.min(np.array(ss)[:,0])
    #print np.max(np.array(ss)[:,1]) - np.min(np.array(ss)[:,1])
    #print 'len(ss)', len(ss)
    #plt.plot(np.array(ss)[:,0], np.array(ss)[:,1])
    #plt.axis('equal')
    #plt.show()
    return [ss]

class ShapeDB:
    def __init__(self):
        sampleSize = 24
        self.shape_db["rect1"]["shape"] = makeShapePolyRect(0.090, 0.090)
        self.shape_db["rect1"]["bounds"] = sampleShape(self.shape_db["rect1"]["shape"], sampleSize, False)
        self.shape_db["rect1"]["ranbounds"] = sampleShape(self.shape_db["rect1"]["shape"], sampleSize, True)
        self.shape_db["rect2"]["shape"] = makeShapePolyRect(0.08991, 0.11258)
        self.shape_db["rect2"]["bounds"] = sampleShape(self.shape_db["rect2"]["shape"], sampleSize, False)
        self.shape_db["rect2"]["ranbounds"] = sampleShape(self.shape_db["rect2"]["shape"], sampleSize, True)
        self.shape_db["rect3"]["shape"] = makeShapePolyRect(0.13501, 0.08994)
        self.shape_db["rect3"]["bounds"] = sampleShape(self.shape_db["rect3"]["shape"], sampleSize, False)
        self.shape_db["rect3"]["ranbounds"] = sampleShape(self.shape_db["rect3"]["shape"], sampleSize, True)
        
        self.shape_db["tri1"]["shape"] = makeShapePolyTri(0.12587, 0.12590, 0.178)
        self.shape_db["tri1"]["bounds"] = sampleShape(self.shape_db["tri1"]["shape"], sampleSize, False)
        self.shape_db["tri1"]["ranbounds"] = sampleShape(self.shape_db["tri1"]["shape"], sampleSize, True)
        self.shape_db["tri2"]["shape"] = makeShapePolyTri(0.12587, 0.15100, 0.1962)
        self.shape_db["tri2"]["bounds"] = sampleShape(self.shape_db["tri2"]["shape"], sampleSize, False)
        self.shape_db["tri2"]["ranbounds"] = sampleShape(self.shape_db["tri2"]["shape"], sampleSize, True)
        self.shape_db["tri3"]["shape"] = makeShapePolyTri(0.12561, 0.1765, 0.2152)
        self.shape_db["tri3"]["bounds"] = sampleShape(self.shape_db["tri3"]["shape"], sampleSize, False)
        self.shape_db["tri3"]["ranbounds"] = sampleShape(self.shape_db["tri3"]["shape"], sampleSize, True)
        
        self.shape_db["ellip1"]["shape"] = makeShapeEllip(0.105/2, 0.105/2)
        self.shape_db["ellip1"]["bounds"] = sampleShape(self.shape_db["ellip1"]["shape"], sampleSize, False)
        self.shape_db["ellip1"]["ranbounds"] = sampleShape(self.shape_db["ellip1"]["shape"], sampleSize, True)
        self.shape_db["ellip2"]["shape"] = makeShapeEllip(0.105/2, 0.13089/2)
        self.shape_db["ellip2"]["bounds"] = sampleShape(self.shape_db["ellip2"]["shape"], sampleSize, False)
        self.shape_db["ellip2"]["ranbounds"] = sampleShape(self.shape_db["ellip2"]["shape"], sampleSize, True)
        self.shape_db["ellip3"]["shape"] = makeShapeEllip(0.105/2, 0.157/2)
        self.shape_db["ellip3"]["bounds"] = sampleShape(self.shape_db["ellip3"]["shape"], sampleSize, False)
        self.shape_db["ellip3"]["ranbounds"] = sampleShape(self.shape_db["ellip3"]["shape"], sampleSize, True)
        
        self.shape_db["hex"]["shape"] = makeShapePolyNGon(0.06050, 6)
        self.shape_db["hex"]["bounds"] = sampleShape(self.shape_db["hex"]["shape"], sampleSize, False)
        self.shape_db["hex"]["ranbounds"] = sampleShape(self.shape_db["hex"]["shape"], sampleSize, True)
        
        self.shape_db["butter"]["shape"] = processButtShape(self.shape_db["butter"]["shape"])
        self.shape_db["butter"]["bounds"] = sampleButter(self.shape_db["butter"]["shape"], sampleSize, False)
        self.shape_db["butter"]["ranbounds"] = sampleButter(self.shape_db["butter"]["shape"], sampleSize, True)
        #-------------------------polygon sampling-------added 120717---------------------------

        # butter already done 
        #-------------------------polygon sampling---------------------------------------------
        # all have same thickness
        for key in self.shape_db:
            self.shape_db[key]["thickness"] = 0.013
            
        for key in self.shape_db:
            self.shape_db[key]["frame_id"] = '/vicon/StainlessSteel/StainlessSteel'
            
        for key in self.shape_db:
            self.shape_db[key]["mesh"] = 'package://pnpush_config/models/object_meshes/StainlessSteel_%s.stl' % key
            
        for key in self.shape_db:
            #self.shape_db[key]["slot_pos"] = [-0.03, -0.03]
            a = 1/np.sqrt(2) *  (0.03/2)
            self.shape_db[key]["slot_pos"] = [-a, a]

        
    shape_db = {
        "rect1" : {
            "slot_pos" : [],
            "shape_type" : 'poly',
            "mass" : 0.8374,
            "moment_of_inertia": 0.001131,  # kgm^2
            "centroid": (0,0)
        },
        "rect2" : {
            "slot_pos" : [],
            "shape_type" : 'poly',
            "mass" : 1.045,
            "moment_of_inertia": 0.001808,
            "centroid": (0,0)
        },
        "rect3" : {
            "slot_pos" : [],
            "shape_type" : 'poly',
            "mass" : 1.2508,
            "moment_of_inertia": 0.002744,
            "centroid": (0,0)
        },
        "tri1" : {
            "slot_pos" : [],
            "shape_type" : 'poly',
            "mass" : 0.8028,
            "moment_of_inertia": 0.001414,
            "centroid": (0.00303333, 0.00306333)
        },
        "tri2" : {
            "slot_pos" : [],
            "shape_type" : 'poly',
            "mass" : 0.9826,
            "moment_of_inertia": 0.002108,
            "centroid": (-0.00541556, 0.00309479)
        },
        "tri3" : {
            "slot_pos" : [],
            "shape_type" : 'poly',
            "mass" : 1.1326,
            "moment_of_inertia": 0.002957,
            "centroid": (-0.01387576, 0.0031902 )
        },
        "ellip1" : {
            "slot_pos" : [],
            "shape_type" : 'ellip',
            "mass" : 0.8937,
            "moment_of_inertia": 0.001231,
            "centroid": (0,0)
        },
        "ellip2" : {
            "slot_pos" : [],
            "shape_type" : 'ellip',
            "mass" : 1.1104,
            "moment_of_inertia": 0.001953,
            "centroid": (0,0)
        },
        "ellip3" : {
            "slot_pos" : [],
            "shape_type" : 'ellip',
            "mass" : 1.3338,
            "moment_of_inertia": 0.002973,
            "centroid": (0,0)
        },
        "hex" : {
            "slot_pos" : [],
            "shape_type" : 'poly',
            "mass" : 0.9827,
            "moment_of_inertia": 0.001497
        },
        "butter" : {
            "slot_pos" : [],
            "shape_type" : 'polyapprox',
            "mass" : 1.1974,
            "centroid": (0,0),
            "moment_of_inertia": 0.00295433407908,
            "shape": [[[430.6373116,305.3778861],
[430.717624,304.7557722],
[430.7979365,304.1336582],
[430.8782489,303.5115443],
[430.9585613,302.8894304],
[431.0388737,302.2673165],
[431.1191861,301.6452026],
[431.1994985,301.0230886],
[431.2798109,300.4015753],
[431.4962498,299.780062],
[431.7126887,299.1585486],
[431.9291276,298.5370353],
[432.1455665,297.9155219],
[432.3620053,297.2940086],
[432.5784442,296.6724952],
[432.7948831,296.0509819],
[433.011322,295.4306697],
[433.3271398,294.8103575],
[433.6429577,294.1900453],
[433.9587755,293.5697331],
[434.2745933,292.9494209],
[434.5904112,292.3291087],
[434.906229,291.7087965],
[435.2220468,291.0884843],
[435.5378647,290.4699738],
[435.9163139,289.8514633],
[436.2947632,289.2329528],
[436.6732125,288.6144423],
[437.0516617,287.9959318],
[437.430111,287.3774213],
[437.8085602,286.7589108],
[438.1870095,286.1404004],
[438.5654588,285.5242922],
[438.9697919,284.908184],
[439.3741251,284.2920758],
[439.7784583,283.6759676],
[440.1827914,283.0598594],
[440.5871246,282.4437512],
[440.9914578,281.827643],
[441.3957909,281.2115348],
[441.8001241,280.5984294],
[442.1935936,279.9853241],
[442.5870632,279.3722188],
[442.9805327,278.7591134],
[443.3740023,278.1460081],
[443.7674718,277.5329027],
[444.1609414,276.9197974],
[444.5544109,276.3066921],
[444.9478805,275.6971902],
[445.2937389,275.0876883],
[445.6395973,274.4781863],
[445.9854557,273.8686844],
[446.3313141,273.2591825],
[446.6771725,272.6496806],
[447.0230309,272.0401787],
[447.3688893,271.4306768],
[447.7147477,270.8253789],
[447.9762475,270.220081],
[448.2377472,269.6147831],
[448.499247,269.0094852],
[448.7607467,268.4041873],
[449.0222465,267.7988894],
[449.2837462,267.1935915],
[449.545246,266.5882936],
[449.8067457,265.9878003],
[449.9471393,265.3873069],
[450.0875328,264.7868136],
[450.2279264,264.1863203],
[450.3683199,263.585827],
[450.5087135,262.9853336],
[450.649107,262.3848403],
[450.7895006,261.784347],
[450.9298942,261.1900913],
[450.9174833,260.5958357],
[450.9050725,260.00158],
[450.8926617,259.4073244],
[450.8802509,258.8130687],
[450.8678401,258.218813],
[450.8554293,257.6245574],
[450.8430185,257.0303017],
[450.8306077,256.449207],
[450.6669932,255.8681124],
[450.5033787,255.2870177],
[450.3397642,254.705923],
[450.1761497,254.1248283],
[450.0125352,253.5437336],
[449.8489207,252.9626389],
[449.6853062,252.3815442],
[449.5216917,251.8227572],
[449.2219595,251.2639702],
[448.9222273,250.7051832],
[448.6224951,250.1463962],
[448.3227629,249.5876092],
[448.0230306,249.0288222],
[447.7232984,248.4700352],
[447.4235662,247.9112482],
[447.123834,247.3839219],
[446.7031083,246.8565956],
[446.2823825,246.3292693],
[445.8616568,245.801943],
[445.4409311,245.2746167],
[445.0202053,244.7472904],
[444.5994796,244.2199641],
[444.1787539,243.6926378],
[443.7580281,243.2059253],
[443.2314331,242.7192127],
[442.704838,242.2325001],
[442.1782429,241.7457875],
[441.6516479,241.2590749],
[441.1250528,240.7723624],
[440.5984577,240.2856498],
[440.0718627,239.7989372],
[439.5452676,239.3619914],
[438.9279274,238.9250455],
[438.3105872,238.4880997],
[437.693247,238.0511538],
[437.0759068,237.614208],
[436.4585666,237.1772621],
[435.8412264,236.7403163],
[435.2238861,236.3033705],
[434.6065459,235.9253444],
[433.9135848,235.5473183],
[433.2206236,235.1692922],
[432.5276625,234.7912661],
[431.8347013,234.41324],
[431.1417401,234.0352139],
[430.448779,233.6571878],
[429.7558178,233.2791617],
[429.0628567,232.9692084],
[428.3093988,232.6592551],
[427.5559408,232.3493018],
[426.8024829,232.0393485],
[426.049025,231.7293951],
[425.2955671,231.4194418],
[424.5421092,231.1094885],
[423.7886512,230.7995352],
[423.0351933,230.5668076],
[422.2363628,230.3340801],
[421.4375323,230.1013526],
[420.6387018,229.868625],
[419.8398713,229.6358975],
[419.0410409,229.40317],
[418.2422104,229.1704424],
[417.4433799,228.9377149],
[416.6445494,228.7913661],
[415.8154705,228.6450174],
[414.9863916,228.4986687],
[414.1573128,228.3523199],
[413.3282339,228.2059712],
[412.499155,228.0596225],
[411.6700762,227.9132737],
[410.8409973,227.766925],
[410.0119184,227.7161081],
[409.1677154,227.6652912],
[408.3235123,227.6144743],
[407.4793092,227.5636574],
[406.6351062,227.5128404],
[405.7909031,227.4620235],
[404.9467,227.4112066],
[404.102497,227.3603897],
[403.2582939,227.4112066],
[402.4140909,227.4620235],
[401.5698878,227.5128404],
[400.7256847,227.5636574],
[399.8814817,227.6144743],
[399.0372786,227.6652912],
[398.1930756,227.7161081],
[397.3488725,227.766925],
[396.5046694,227.9132737],
[395.6755906,228.0596225],
[394.8465117,228.2059712],
[394.0174328,228.3523199],
[393.188354,228.4986687],
[392.3592751,228.6450174],
[391.5301962,228.7913661],
[390.7011173,228.9377149],
[389.8720385,229.1704424],
[389.073208,229.40317],
[388.2743775,229.6358975],
[387.475547,229.868625],
[386.6767165,230.1013526],
[385.877886,230.3340801],
[385.0790555,230.5668076],
[384.280225,230.7995352],
[383.4813945,231.1094885],
[382.7279366,231.4194418],
[381.9744787,231.7293951],
[381.2210208,232.0393485],
[380.4675629,232.3493018],
[379.7141049,232.6592551],
[378.960647,232.9692084],
[378.2071891,233.2791617],
[377.4537312,233.6571878],
[376.76077,234.0352139],
[376.0678089,234.41324],
[375.3748477,234.7912661],
[374.6818865,235.1692922],
[373.9889254,235.5473183],
[373.2959642,235.9253444],
[372.6030031,236.3033705],
[371.9100419,236.7403163],
[371.2927017,237.1772621],
[370.6753615,237.614208],
[370.0580213,238.0511538],
[369.4406811,238.4880997],
[368.8233409,238.9250455],
[368.2060007,239.3619914],
[367.5886605,239.7989372],
[366.9713203,240.2856498],
[366.4447252,240.7723624],
[365.9181301,241.2590749],
[365.3915351,241.7457875],
[364.86494,242.2325001],
[364.3383449,242.7192127],
[363.8117499,243.2059253],
[363.2851548,243.6926378],
[362.7585597,244.2199641],
[362.337834,244.7472904],
[361.9171083,245.2746167],
[361.4963825,245.801943],
[361.0756568,246.3292693],
[360.654931,246.8565956],
[360.2342053,247.3839219],
[359.8134796,247.9112482],
[359.3927538,248.4700352],
[359.0930216,249.0288222],
[358.7932894,249.5876092],
[358.4935572,250.1463962],
[358.193825,250.7051832],
[357.8940928,251.2639702],
[357.5943606,251.8227572],
[357.2946284,252.3815442],
[356.9948961,252.9626389],
[356.8312816,253.5437336],
[356.6676671,254.1248283],
[356.5040526,254.705923],
[356.3404381,255.2870177],
[356.1768236,255.8681124],
[356.0132091,256.449207],
[355.8495946,257.0303017],
[355.6859801,257.6245574],
[355.6735693,258.218813],
[355.6611585,258.8130687],
[355.6487477,259.4073244],
[355.6363369,260.00158],
[355.6239261,260.5958357],
[355.6115153,261.1900913],
[355.5991045,261.784347],
[355.5866937,262.3848403],
[355.7270873,262.9853336],
[355.8674808,263.585827],
[356.0078744,264.1863203],
[356.1482679,264.7868136],
[356.2886615,265.3873069],
[356.429055,265.9878003],
[356.5694486,266.5882936],
[356.7098422,267.1935915],
[356.9713419,267.7988894],
[357.2328416,268.4041873],
[357.4943414,269.0094852],
[357.7558411,269.6147831],
[358.0173409,270.220081],
[358.2788406,270.8253789],
[358.5403404,271.4306768],
[358.8018401,272.0401787],
[359.1476985,272.6496806],
[359.4935569,273.2591825],
[359.8394153,273.8686844],
[360.1852737,274.4781863],
[360.5311321,275.0876883],
[360.8769906,275.6971902],
[361.222849,276.3066921],
[361.5687074,276.9197974],
[361.9621769,277.5329027],
[362.3556465,278.1460081],
[362.749116,278.7591134],
[363.1425856,279.3722188],
[363.5360551,279.9853241],
[363.9295247,280.5984294],
[364.3229942,281.2115348],
[364.7164638,281.827643],
[365.1207969,282.4437512],
[365.5251301,283.0598594],
[365.9294633,283.6759676],
[366.3337964,284.2920758],
[366.7381296,284.908184],
[367.1424628,285.5242922],
[367.5467959,286.1404004],
[367.9511291,286.7589108],
[368.3295784,287.3774213],
[368.7080276,287.9959318],
[369.0864769,288.6144423],
[369.4649261,289.2329528],
[369.8433754,289.8514633],
[370.2218247,290.4699738],
[370.6002739,291.0884843],
[370.9787232,291.7087965],
[371.294541,292.3291087],
[371.6103589,292.9494209],
[371.9261767,293.5697331],
[372.2419945,294.1900453],
[372.5578124,294.8103575],
[372.8736302,295.4306697],
[373.189448,296.0509819],
[373.5052659,296.6724952],
[373.7217047,297.2940086],
[373.9381436,297.9155219],
[374.1545825,298.5370353],
[374.3710214,299.1585486],
[374.5874603,299.780062],
[374.8038992,300.4015753],
[375.0203381,301.0230886],
[375.2367769,301.6452026],
[375.3170893,302.2673165],
[375.3974018,302.8894304],
[375.4777142,303.5115443],
[375.5580266,304.1336582],
[375.638339,304.7557722],
[375.7186514,305.3778861],
[375.7989638,375.8792762],
[306.6221139,375.7989638],
[307.2442278,375.7186514],
[307.8663418,375.638339],
[308.4884557,375.5580266],
[309.1105696,375.4777142],
[309.7326835,375.3974018],
[310.3547974,375.3170893],
[310.9769114,375.2367769],
[311.5984247,375.0203381],
[312.219938,374.8038992],
[312.8414514,374.5874603],
[313.4629647,374.3710214],
[314.0844781,374.1545825],
[314.7059914,373.9381436],
[315.3275048,373.7217047],
[315.9490181,373.5052659],
[316.5693303,373.189448],
[317.1896425,372.8736302],
[317.8099547,372.5578124],
[318.4302669,372.2419945],
[319.0505791,371.9261767],
[319.6708913,371.6103589],
[320.2912035,371.294541],
[320.9115157,370.9787232],
[321.5300262,370.6002739],
[322.1485367,370.2218247],
[322.7670472,369.8433754],
[323.3855577,369.4649261],
[324.0040682,369.0864769],
[324.6225787,368.7080276],
[325.2410892,368.3295784],
[325.8595996,367.9511291],
[326.4757078,367.5467959],
[327.091816,367.1424628],
[327.7079242,366.7381296],
[328.3240324,366.3337964],
[328.9401406,365.9294633],
[329.5562488,365.5251301],
[330.172357,365.1207969],
[330.7884652,364.7164638],
[331.4015706,364.3229942],
[332.0146759,363.9295247],
[332.6277812,363.5360551],
[333.2408866,363.1425856],
[333.8539919,362.749116],
[334.4670973,362.3556465],
[335.0802026,361.9621769],
[335.6933079,361.5687074],
[336.3028098,361.222849],
[336.9123117,360.8769906],
[337.5218137,360.5311321],
[338.1313156,360.1852737],
[338.7408175,359.8394153],
[339.3503194,359.4935569],
[339.9598213,359.1476985],
[340.5693232,358.8018401],
[341.1746211,358.5403404],
[341.779919,358.2788406],
[342.3852169,358.0173409],
[342.9905148,357.7558411],
[343.5958127,357.4943414],
[344.2011106,357.2328416],
[344.8064085,356.9713419],
[345.4117064,356.7098422],
[346.0121997,356.5694486],
[346.6126931,356.429055],
[347.2131864,356.2886615],
[347.8136797,356.1482679],
[348.414173,356.0078744],
[349.0146664,355.8674808],
[349.6151597,355.7270873],
[350.215653,355.5866937],
[350.8099087,355.5991045],
[351.4041643,355.6115153],
[351.99842,355.6239261],
[352.5926756,355.6363369],
[353.1869313,355.6487477],
[353.781187,355.6611585],
[354.3754426,355.6735693],
[354.9696983,355.6859801],
[355.550793,355.8495946],
[356.1318876,356.0132091],
[356.7129823,356.1768236],
[357.294077,356.3404381],
[357.8751717,356.5040526],
[358.4562664,356.6676671],
[359.0373611,356.8312816],
[359.6184558,356.9948961],
[360.1772428,357.2946284],
[360.7360298,357.5943606],
[361.2948168,357.8940928],
[361.8536038,358.193825],
[362.4123908,358.4935572],
[362.9711778,358.7932894],
[363.5299648,359.0930216],
[364.0887518,359.3927538],
[364.6160781,359.8134796],
[365.1434044,360.2342053],
[365.6707307,360.654931],
[366.198057,361.0756568],
[366.7253833,361.4963825],
[367.2527096,361.9171083],
[367.7800359,362.337834],
[368.3073622,362.7585597],
[368.7940747,363.2851548],
[369.2807873,363.8117499],
[369.7674999,364.3383449],
[370.2542125,364.86494],
[370.7409251,365.3915351],
[371.2276376,365.9181301],
[371.7143502,366.4447252],
[372.2010628,366.9713203],
[372.6380086,367.5886605],
[373.0749545,368.2060007],
[373.5119003,368.8233409],
[373.9488462,369.4406811],
[374.385792,370.0580213],
[374.8227379,370.6753615],
[375.2596837,371.2927017],
[375.6966295,371.9100419],
[376.0746556,372.6030031],
[376.4526817,373.2959642],
[376.8307078,373.9889254],
[377.2087339,374.6818865],
[377.58676,375.3748477],
[377.9647861,376.0678089],
[378.3428122,376.76077],
[378.7208383,377.4537312],
[379.0307916,378.2071891],
[379.3407449,378.960647],
[379.6506982,379.7141049],
[379.9606515,380.4675629],
[380.2706049,381.2210208],
[380.5805582,381.9744787],
[380.8905115,382.7279366],
[381.2004648,383.4813945],
[381.4331924,384.280225],
[381.6659199,385.0790555],
[381.8986474,385.877886],
[382.131375,386.6767165],
[382.3641025,387.475547],
[382.59683,388.2743775],
[382.8295576,389.073208],
[383.0622851,389.8720385],
[383.2086339,390.7011173],
[383.3549826,391.5301962],
[383.5013313,392.3592751],
[383.6476801,393.188354],
[383.7940288,394.0174328],
[383.9403775,394.8465117],
[384.0867263,395.6755906],
[384.233075,396.5046694],
[384.2838919,397.3488725],
[384.3347088,398.1930756],
[384.3855257,399.0372786],
[384.4363426,399.8814817],
[384.4871596,400.7256847],
[384.5379765,401.5698878],
[384.5887934,402.4140909],
[384.6396103,403.2582939],
[384.5887934,404.102497],
[384.5379765,404.9467],
[384.4871596,405.7909031],
[384.4363426,406.6351062],
[384.3855257,407.4793092],
[384.3347088,408.3235123],
[384.2838919,409.1677154],
[384.233075,410.0119184],
[384.0867263,410.8409973],
[383.9403775,411.6700762],
[383.7940288,412.499155],
[383.6476801,413.3282339],
[383.5013313,414.1573128],
[383.3549826,414.9863916],
[383.2086339,415.8154705],
[383.0622851,416.6445494],
[382.8295576,417.4433799],
[382.59683,418.2422104],
[382.3641025,419.0410409],
[382.131375,419.8398713],
[381.8986474,420.6387018],
[381.6659199,421.4375323],
[381.4331924,422.2363628],
[381.2004648,423.0351933],
[380.8905115,423.7886512],
[380.5805582,424.5421092],
[380.2706049,425.2955671],
[379.9606515,426.049025],
[379.6506982,426.8024829],
[379.3407449,427.5559408],
[379.0307916,428.3093988],
[378.7208383,429.0628567],
[378.3428122,429.7558178],
[377.9647861,430.448779],
[377.58676,431.1417401],
[377.2087339,431.8347013],
[376.8307078,432.5276625],
[376.4526817,433.2206236],
[376.0746556,433.9135848],
[375.6966295,434.6065459],
[375.2596837,435.2238861],
[374.8227379,435.8412264],
[374.385792,436.4585666],
[373.9488462,437.0759068],
[373.5119003,437.693247],
[373.0749545,438.3105872],
[372.6380086,438.9279274],
[372.2010628,439.5452676],
[371.7143502,440.0718627],
[371.2276376,440.5984577],
[370.7409251,441.1250528],
[370.2542125,441.6516479],
[369.7674999,442.1782429],
[369.2807873,442.704838],
[368.7940747,443.2314331],
[368.3073622,443.7580281],
[367.7800359,444.1787539],
[367.2527096,444.5994796],
[366.7253833,445.0202053],
[366.198057,445.4409311],
[365.6707307,445.8616568],
[365.1434044,446.2823825],
[364.6160781,446.7031083],
[364.0887518,447.123834],
[363.5299648,447.4235662],
[362.9711778,447.7232984],
[362.4123908,448.0230306],
[361.8536038,448.3227629],
[361.2948168,448.6224951],
[360.7360298,448.9222273],
[360.1772428,449.2219595],
[359.6184558,449.5216917],
[359.0373611,449.6853062],
[358.4562664,449.8489207],
[357.8751717,450.0125352],
[357.294077,450.1761497],
[356.7129823,450.3397642],
[356.1318876,450.5033787],
[355.550793,450.6669932],
[354.9696983,450.8306077],
[354.3754426,450.8430185],
[353.781187,450.8554293],
[353.1869313,450.8678401],
[352.5926756,450.8802509],
[351.99842,450.8926617],
[351.4041643,450.9050725],
[350.8099087,450.9174833],
[350.215653,450.9298942],
[349.6151597,450.7895006],
[349.0146664,450.649107],
[348.414173,450.5087135],
[347.8136797,450.3683199],
[347.2131864,450.2279264],
[346.6126931,450.0875328],
[346.0121997,449.9471393],
[345.4117064,449.8067457],
[344.8064085,449.545246],
[344.2011106,449.2837462],
[343.5958127,449.0222465],
[342.9905148,448.7607467],
[342.3852169,448.499247],
[341.779919,448.2377472],
[341.1746211,447.9762475],
[340.5693232,447.7147477],
[339.9598213,447.3688893],
[339.3503194,447.0230309],
[338.7408175,446.6771725],
[338.1313156,446.3313141],
[337.5218137,445.9854557],
[336.9123117,445.6395973],
[336.3028098,445.2937389],
[335.6933079,444.9478805],
[335.0802026,444.5544109],
[334.4670973,444.1609414],
[333.8539919,443.7674718],
[333.2408866,443.3740023],
[332.6277812,442.9805327],
[332.0146759,442.5870632],
[331.4015706,442.1935936],
[330.7884652,441.8001241],
[330.172357,441.3957909],
[329.5562488,440.9914578],
[328.9401406,440.5871246],
[328.3240324,440.1827914],
[327.7079242,439.7784583],
[327.091816,439.3741251],
[326.4757078,438.9697919],
[325.8595996,438.5654588],
[325.2410892,438.1870095],
[324.6225787,437.8085602],
[324.0040682,437.430111],
[323.3855577,437.0516617],
[322.7670472,436.6732125],
[322.1485367,436.2947632],
[321.5300262,435.9163139],
[320.9115157,435.5378647],
[320.2912035,435.2220468],
[319.6708913,434.906229],
[319.0505791,434.5904112],
[318.4302669,434.2745933],
[317.8099547,433.9587755],
[317.1896425,433.6429577],
[316.5693303,433.3271398],
[315.9490181,433.011322],
[315.3275048,432.7948831],
[314.7059914,432.5784442],
[314.0844781,432.3620053],
[313.4629647,432.1455665],
[312.8414514,431.9291276],
[312.219938,431.7126887],
[311.5984247,431.4962498],
[310.9769114,431.2798109],
[310.3547974,431.1994985],
[309.7326835,431.1191861],
[309.1105696,431.0388737],
[308.4884557,430.9585613],
[307.8663418,430.8782489],
[307.2442278,430.7979365],
[306.6221139,430.717624]]]
        }
    }

if __name__=='__main__':
    sdb = ShapeDB()
