import matplotlib
matplotlib.use('TKAgg')

import numpy as np
from matplotlib import pyplot as plt

from matplotlib import animation
from numpy import genfromtxt

import math
from time import time

import csv
#====================================
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

print info_171
print info_172

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
    x = []
    y = []
    x_stops = []
    y_stops = []
    #name = []

    #Loop through and convert 
    for row in range(1,len(copy)):
        lat2 = float(copy[row][2])
        lon2 = float(copy[row][3])

        dx = (lon2-lon1)*40000*math.cos((lat1+lat2)*math.pi/360)/360
        dy = ((lat1-lat2)*40000/360) * -1
        x.append(dx)
        y.append(dy)
        #name.append(info_array[s][0])
        
        if info_array[row][4] == 'S':
            x_stops.append(dx)
            y_stops.append(dy)
       
    print len(x)
    print len(x_stops)      
    return (x,y, x_stops, y_stops)

    
pattern171 = get_x_y(info_171)
pattern172 = get_x_y(info_172)

patx171, paty171 = pattern171[0], pattern171[1]
patx172, paty172 = pattern172[0], pattern172[1]

stopsx171, stopsy171 = pattern171[2], pattern171[3]
stopsx172, stopsy172 = pattern172[2], pattern172[3]


#Mythili's code from test4.py 
def init():
    patch.center = (-10, -10)
    patch2.center = (-10, -10)
    ax.add_patch(patch)
    ax.add_patch(patch2)
    return [patch,patch2]

def animate(i):
    x, y = patch.center
    x2, y2 = patch2.center

    x = patx171[i]
    y = paty171[i]
    x2 = patx172[i]
    y2 = paty172[i]
    
    patch.center = (x, y)
    patch2.center = (x2, y2)
     
    return (patch, patch2)

fig = plt.figure()
fig.set_dpi(100)
fig.set_size_inches(.7, .65)


ax = plt.axes(xlim=(-0.5, 2), ylim=(-0.5, 2.5))
patch = plt.Circle((.5, -.5), 0.05, fc='y')
patch2 = plt.Circle((.5, -.5), 0.05, fc='b')


plt.scatter(stopsx171, stopsy171)
plt.scatter(stopsx172, stopsy172)
plt.plot(patx171, paty171, 'r')
plt.plot(patx172, paty172, 'c')


anim = animation.FuncAnimation(fig, animate, 
                               init_func=init,
                               frames = len(patx172),
                               interval=100,
                               blit=True,
                               repeat=True)


plt.show()
