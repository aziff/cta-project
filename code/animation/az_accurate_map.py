import matplotlib
matplotlib.use('TKAgg')

import numpy as np
from matplotlib import pyplot as plt

from matplotlib import animation
from numpy import genfromtxt

import math
from time import time

import csv

'''
from matplotlib import __version__
print("matplotlib version: {}".format(__version__))
import os
os.system('ffmpeg')
'''
#====================================

# Import data from a .csv-file and put it in a dataframe
def import_data(filename):
	data = []
	with open(filename, 'rU') as csvfile:
		reader = csv.reader(csvfile, delimiter = ',')
		for row in reader:
			data.append(row)
	return data

'''			
info_171 = []
with open('P171stops.csv', 'rU') as csvfile:
        spamreader = csv.reader(csvfile, delimiter = ',')
        for row in spamreader: 
            info_171.append(row)  

info_172 = []
with open('P172stops.csv', 'rU') as csvfile:
        spamreader = csv.reader(csvfile, delimiter = ',')
        for row in spamreader: 
            info_172.append(row)
''' 

#Anna's Code from lat-lon-x-y.py, edited to add stop information
def get_x_y(info_array):
    #make a copy and delete extraneous rows 
    copy = []    
    for row in range(0, len(info_array)):
        if info_array[row][4] == 'W' or info_array[row][4] == 'S':
            copy.append(info_array[row])      
    
    #Set up for conversion 
    lat1 = 41.78588506 # The origin is the most southwest stop (60/Ellis)
    lon1 = -87.60104835
    
    x, y, x_stops, y_stops = [], [], [], []
    stop_dict = {}
    
    i = 1
    order = 1
    #Loop through and convert 
    for row in range(1,len(copy)):
        lat2 = float(copy[row][2])
        lon2 = float(copy[row][3])

        dx = (lon2-lon1)*40000*math.cos((lat1+lat2)*math.pi/360)/360
        dy = ((lat1-lat2)*40000/360) * -1
        x.append(dx)
        y.append(dy)
        
        if info_array[row][4] == 'S':
            x_stops.append(dx)
            y_stops.append(dy)
                        
            if info_array[row][0] not in stop_dict:
                stop_dict[info_array[row][0]] = ((dx, dy),order, i, info_array[row][5])
                order+=1
                #i += 2 # THIS MAKES time at each stop CHANGE
                # Calculate amount of time at each stop
            	# Eventually make a function that takes arrival times and makes an array/dit
            	# that maps stopID to number i
                    
    return (x,y, x_stops, y_stops, stop_dict)


def make_lists_from_dict(get_output):
    dict = get_output[4]
    x = []
    y = []    

    for index in range(len(dict)):
        for key in dict:  
            if dict[key][1] == index:
                x.extend([dict[key][0][0] for i in range(dict[key][2])])
                y.extend([dict[key][0][1] for i in range(dict[key][2])])  
    return (x,y)     
  


#Mythili's code from test4.py 
def init():
	patch.center = (-10, -10)
	patch2.center = (-10, -10)
	ax.add_patch(patch)
	ax.add_patch(patch2)
	return (patch, patch2)
	
def get_riders(stop_dict):
	num_riders, x_riders, y_riders = [], [], []
	for i in range(len(stop_dict)):
		for key in stop_dict:
			if stop_dict[key][1] == i:
				num_riders.append(int(stop_dict[key][3]))
	return num_riders
	
def make_rider_pts(num_riders, i):
	x_riders, y_riders = [], []
	
	if num_riders[i] > 0:
		for j in range(1, num_riders[i]):
			x_riders.append(j*0.001+1.5)
			y_riders.append(0)
	return x_riders, y_riders

def animate(i):
	x, y = patch.center
	x2, y2 = patch2.center

	x = animation_points_171[0][i] 
	y = animation_points_171[1][i]
    
	x2 = stopsx172[i]
	y2 = stopsy172[i]
    
	patch.center = (x, y)
	patch2.center = (x2, y2)
	
	x_riders, y_riders = make_rider_pts(num_riders, i)
	print(x_riders)
	scat = ax.scatter(x_riders, y_riders)
     
	return (patch, patch2, scat)


info_171 = import_data('test-171.csv')
info_172 = import_data('test-172.csv')

pattern171 = get_x_y(info_171) # add number of riders into dictionary
pattern172 = get_x_y(info_172)

animation_points_171 = make_lists_from_dict(pattern171)
animation_points_172 = make_lists_from_dict(pattern172)
	
patx171, paty171 = pattern171[0], pattern171[1]
stopsx171, stopsy171 = pattern171[2], pattern171[3]

patx172, paty172 = pattern172[0], pattern172[1]
stopsx172, stopsy172 = pattern172[2], pattern172[3]
	
fig = plt.figure()
fig.set_dpi(100)
fig.set_size_inches(.7, .65)

ax = plt.axes(xlim=(-0.5, 2), ylim=(-0.5, 2.5))
patch = plt.Circle((.5, -.5), 0.05, fc='r')
patch2 = plt.Circle((.5, -.5), 0.05, fc='b')

num_riders = get_riders(pattern171[4])
x_riders, y_riders = 0,0
scat = ax.scatter(x_riders, y_riders)

plt.scatter(stopsx171, stopsy171)
plt.scatter(stopsx172, stopsy172)
plt.plot(patx171, paty171, 'r')
plt.plot(patx172, paty172, 'b')

anim = animation.FuncAnimation(fig, animate, 
                               init_func=init,
                               frames = len(animation_points_171[0]),
                               interval=100,
                               blit=True,
                               repeat=True)
                               
plt.show() 

    

             
'''                          
Writer = animation.writers['ffmpeg']
writer = Writer(fps=15, metadata=dict(artist='Me'), bitrate=1800)                
anim.save('the_movie.mp4', writer = writer)
'''





