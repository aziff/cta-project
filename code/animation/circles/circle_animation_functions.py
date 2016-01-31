import matplotlib
matplotlib.use('TKAgg')

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

'''
Define lat and lon constants
The origin is the most southwest stop for both routes (60/Ellis)
'''
LAT_ORIGIN = 41.78588506
LON_ORIGIN = -87.60104835

FILE_PATH = '../../../data/processed/'


'''
Import data from a csv file
'''
def read_csv(filename):
  data = []
  with open(filename, 'rU') as csvfile:
    reader = csv.reader(csvfile, delimiter = ',')
    for row in reader:
      data.append(row)
  return data

'''
Given lat and lon (floats), convert to xy-coordinates using origin latitude and longitude defined above
Won't actually be necessary for this particular code
'''
def convert_lat_lon(lat, lon):
  dx = (lon-LON_ORIGIN)*40000*math.cos((lat+LAT_ORIGIN)*math.pi/360)/360
  dy = ((lat-LAT_ORIGIN)*40000/360) * -1
  return (dx, dy)

'''
Calculate distance between two points in latitude and longitude
Haversine Formula
http://stackoverflow.com/questions/4913349/haversine-formula-in-python-bearing-and-distance-between-two-gps-points
'''
def haversine(lon1, lat1, lon2, lat2):
  lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
  dlon = lon2 - lon1
  dlat = lat2 - lat1
  a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
  c = 2 * asin(sqrt(a))
  r = 6371000 # meters
  return c * r

'''
Load data and put into clean dictionary
'''
def load_data():
  data = {}
  routes = ['171','172']

  for r in routes:
    file = FILE_PATH + r + 'pattern.csv'
    raw_data = read_csv(file)
    data[r] = {}

    order = 1
    for row in raw_data:
      if row[0] != 'stpid':
        data[r][order] = [row[4], row[0], row[1], float(row[2]), float(row[3])]
        order += 1
  return data

'''
Get distances between all the points. Must insert dict of the individual routes
'''
def get_distance(route_dict):
  for i in route_dict:
    lat2 = route_dict[i][3]
    lon2 = route_dict[i][4]
    if i == 1:
      lat1 = lat2
      lon1 = lon2

    else:
      lat1 = route_dict[i-1][3]
      lon1 = route_dict[i-1][4]

    route_dict[i].append(haversine(lon1, lat1, lon2, lat2))
  return route_dict

'''
Get a list of stops and route length
'''
def route_info(route_dict):
  stops = []
  all_points = []
  route_length = 0

  for i in route_dict:
    if route_dict[i][0] == 'S':
      stops.append(route_dict[i][5])
      
    all_points.append(route_dict[i][5])
    
    route_length += route_dict[i][5]

  return stops, all_points, route_length

def unit_circle_points(arc_distance, tot_distance, distance):
  c = (float(2) * pi) / tot_distance
  arc_length = distance * c
  arc_distance += arc_length
    
  theta = (float(180) * arc_length)/pi
  x, y = cos(theta), sin(theta)
  return x, y

'''
Make points for the unit circle
'''
def circle_points(route_info_output):
  stop_distance = route_info_output[0]
  all_distance 	= route_info_output[1]
  tot_distance 	= route_info_output[2]
  
  stop_points = {'x': [], 'y': []}
  all_points = {'x': [], 'y': []}
  
  arc_distance = 0
  for d in stop_distance:
    coord_temp = unit_circle_points(arc_distance, tot_distance, d)
    stop_points['x'].append(coord_temp[0])
    stop_points['y'].append(coord_temp[1])
  
  arc_distance = 0
  for d in all_distance:
    coord_temp = unit_circle_points(arc_distance, tot_distance, d) 
    all_points['x'].append(coord_temp[0])
    all_points['y'].append(coord_temp[1])
       
  return stop_points, all_points