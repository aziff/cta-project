import matplotlib
matplotlib.use('TKAgg')

import numpy as np
from matplotlib import pyplot as plt

from matplotlib import animation
from numpy import genfromtxt

import math
from time import time

import csv

from matplotlib import __version__
print("matplotlib version: {}".format(__version__))
import os
os.system('ffmpeg')

#====================================

#Read in the stop information from the CSV files
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



#Anna's Code from lat-lon-x-y.py, edited to add stop information
def get_x_y(info_array):
    print info_array
    #make a copy and delete extraneous rows
    copy = []
    for row in range(0, len(info_array)):
        if info_array[row][4] == 'W' or info_array[row][4] == 'S':
            copy.append(info_array[row])

    #Set up for conversion from latitude/longitude
    #Also, make a dictionary to restructure the information
    lat1 = 41.78588506 # The origin is the most southwest stop (60/Ellis)
    lon1 = -87.60104835
    x = []
    y = []
    x_stops = []
    y_stops = []
    stop_dict = {}
    #name = []

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
        #name.append(info_array[s][0])


        if info_array[row][4] == 'S':
            x_stops.append(dx)
            y_stops.append(dy)

            if info_array[row][0] not in stop_dict:
                stop_dict[info_array[row][0]] = ((dx, dy),order, i)
                order+=1
                i += 2 # THIS MAKES time at each stop CHANGE
                # Calculate amount of time at each stop
            	# Eventually make a function that takes arrival times and makes an array/dit
            	# that maps stopID to number i

    return (x,y, x_stops, y_stops, stop_dict)


#get_x_y is giving us a list of lists with the latitude and longitude
pattern171 = get_x_y(info_171)
pattern172 = get_x_y(info_172)


def make_lists_from_dict(get_output):
    dict = get_output[4]
    x = []
    y = []

    for index in range(len(dict)):
        for key in dict:
            if dict[key][1] == index:
                x.extend([dict[key][0][0] for i in range(dict[key][2])])
                y.extend([dict[key][0][1] for i in range(dict[key][2])])
        print len(dict)
    return (x,y)


anim_points_171_1 = make_lists_from_dict(pattern171)
anim_points_172_1 = make_lists_from_dict(pattern172)

patx171, paty171 = pattern171[0], pattern171[1]
patx172, paty172 = pattern172[0], pattern172[1]

stopsx171, stopsy171 = pattern171[2], pattern171[3]
stopsx172, stopsy172 = pattern172[2], pattern172[3]


#Mythili's code from test4.py
def init():
    patch1.center = (-10, -10)
    patch2.center = (-10, -10)
    patch3.center = (-10, -10)
    patch4.center = (-10, -10)
    patch5.center = (-10, -10)
    patch6.center = (-10, -10)

    ax.add_patch(patch1)
    ax.add_patch(patch2)
    ax.add_patch(patch3)
    ax.add_patch(patch4)
    ax.add_patch(patch5)
    ax.add_patch(patch6)

    return [patch1, patch2, patch3, patch4, patch5, patch6]

def animate(i):
    #update animate so that we have SIX patches: three for 171, three for 172
    x_171_1, y_171_1 = patch1.center
    x_171_2, y_171_2 = patch2.center
    x_171_3, y_171_3 = patch3.center

    x_172_1, y_172_1 = patch4.center
    x_172_2, y_172_2 = patch5.center
    x_172_3, y_172_3 = patch6.center

    x_171_1 = anim_points_171_1[0][i]
    y_171_1 = anim_points_171_1[1][i]

    x_171_1 = anim_points_171_1[0][i+2]
    y_171_1 = anim_points_171_1[1][i+2]

    x_171_1 = anim_points_171_1[0][i+4]
    y_171_1 = anim_points_171_1[1][i+4]

    x_172_1 = anim_points_172_1[0][i]
    y_172_1 = anim_points_172_1[1][i]

    x_172_2 = anim_points_172_1[0][i+2]
    y_172_2 = anim_points_172_1[1][i+2]

    x_172_3 = anim_points_172_1[0][i+4]
    y_172_3 = anim_points_172_1[1][i+4]

    patch1.center = (x_171_1, y_171_1)
    patch2.center = (x_171_2, y_171_2)
    patch3.center = (x_171_3, y_171_3)
    patch4.center = (x_172_1, y_172_1)
    patch5.center = (x_172_2, y_172_2)
    patch6.center = (x_172_3, y_172_3)

    return (patch1, patch2, patch3, patch4, patch5, patch6)


#Set figure
fig = plt.figure()
fig.set_dpi(100)
fig.set_size_inches(.7, .65)


ax = plt.axes(xlim=(-0.5, 2), ylim=(-0.5, 2.5))
patch1 = plt.Circle((.5, -.5), 0.05, fc='y')
patch2 = plt.Circle((.5, -.5), 0.05, fc='b')
patch3 = plt.Circle((.5, -.5), 0.05, fc='r')
patch4 = plt.Circle((.5, -.5), 0.05, fc='c')
patch5 = plt.Circle((.5, -.5), 0.05, fc='b')
patch6 = plt.Circle((.5, -.5), 0.05, fc='b')

#Plot the lines for the route and the points for the stops
plt.scatter(stopsx171, stopsy171)
plt.scatter(stopsx172, stopsy172)
plt.plot(patx171, paty171, 'r')
plt.plot(patx172, paty172, 'c')


anim = animation.FuncAnimation(fig, animate,
                               init_func=init,
                               frames = 100,
                               interval=100,
                               blit=True,
                               repeat=True)


#Writer = animation.writers['ffmpeg']
#writer = Writer(fps=15, metadata=dict(artist='Me'), bitrate=1800)
#anim.save('the_movie.mp4', writer = writer)


plt.show()
