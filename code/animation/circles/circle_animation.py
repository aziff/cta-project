'''
Animate circles to approximate distance and time of busses
'''

import matplotlib

import numpy as np
from numpy import genfromtxt

from matplotlib import pyplot as plt
from matplotlib import animation
from matplotlib import __version__

from math import *
from time import time

from collections import OrderedDict

import csv

import os

from circle_animation_functions import read_csv, convert_lat_lon, haversine, load_data, get_distance, route_info, circle_points

'''
Define lat and lon constants
The origin is the most southwest stop for both routes (60/Ellis)
'''
LAT_ORIGIN = 41.78588506
LON_ORIGIN = -87.60104835

FILE_PATH = '../../../data/processed/'




if __name__ == '__main__':
  data = load_data()

  for r in data:
    data[r] = get_distance(data[r])

  # Get stops and points
  stops171, stops172 = route_info(data['171']), route_info(data['172'])
  points171, points172 = circle_points(stops171), circle_points(stops172)

  plt.figure(1)

  #Set figure
  fig172 = plt.subplot(212)
  plt.axes().set_aspect('equal', 'datalim')

  # Add circle
  circle1=plt.Circle((0,0),1,color='black',fill=False)
  plt.gcf().gca().add_artist(circle1)

  # Add stops
  plt.scatter(points172[0]['x'], points172[0]['y'], s=40, c='black')


  for x, y, i in zip(points172[0]['x'], points172[0]['y'], data['172']):
    txt = data['172'][i][1]
    plt.annotate(txt, xy=(x,y))

  fig171 = plt.subplot(212)
  plt.axes().set_aspect('equal', 'datalim')

  # Add circle
  circle1=plt.Circle((0,0),1,color='black',fill=False)
  plt.gcf().gca().add_artist(circle1)

  # Add stops
  plt.scatter(points171[0]['x'], points171[0]['y'], s=40, c='black')


  for x, y, i in zip(points171[0]['x'], points171[0]['y'], data['171']):
    txt = data['171'][i][1]
    plt.annotate(txt, xy=(x,y))

  plt.show()
