import os
import csv
import matplotlib
from pylab import *

'''

This file takes the csv files with all the prediction data and organizes it.
The functions in this file and the structure are original.
Help on the os library from:
http://stackoverflow.com/questions/273192/in-python-check-if-a-directory-exists-and-create-it-if-necessary
https://docs.python.org/2/library/os.html

'''

# Function that figures out when bus actually arrives at a stop
def calc_time(time):
  hour = (time - (time % 100))/100
  minute = time % 100
  time_min = hour * 60 + minute
  if time_min< 300:
    time_min= time_min +1400

  return time_min

# Parses .csv files and puts the time attached to the prediction,
# the real time and the prediction time into a dictionary
def route_day_dict(filename, date, route):
  with open(filename) as csvfile:
    dict_route = {}
    read = csv.reader(csvfile)
    for row in read:
      row[0] = row[0].strip()
      if row[0]:
        stpid = row[0]
        vid = row[5]
        bustime = int(row[1][9:11]+row[1][12:])
        timestamp = int(row[2][9:11] + row[2][12:14])
        prediction = int(row[4][9:11] + row[4][12:])
        if not stpid in dict_route:
          dict_route[stpid] = {}
        if not vid in dict_route[stpid]:
          dict_route[stpid][vid] = [[calc_time(bustime), calc_time(timestamp), calc_time(prediction)]]
        else:
          dict_route[stpid][vid].append([calc_time(bustime), calc_time(timestamp), calc_time(prediction)])
  return dict_route

#creates dictionary with the keys: cta route, date, stop id, and vehicle id
#vehicle id contains the time attached to the prediction, the real time and the predicted bus arrival time
def mk_data_dict():
  data_dict = {}
  for route in ["6","55","171","172"]:
    data_dict[route] = {}
    for day in range(8,29):
      if day != 21:
        date_feb = "2-" + str(day) + "-15"
        filename =  str(route) + "_" + date_feb + ".csv"
        filename = os.path.join("Data",filename)
        data_dict[route][date_feb] = route_day_dict(filename, date_feb, route)
    for day in range(1,5):
      if day != 2:
        date_march = "3-" + str(day) + "-15"
        filename =  str(route) + "_" + date_march + ".csv"
        filename = os.path.join("Data",filename)
        data_dict[route][date_march] = route_day_dict(filename, date_march, route)

  return data_dict

'''
Takes the data dictionary and figures out when a bus arrived and appeneds bus_pred, real_pred, bus_diff,
real_diff and the time the bus arrived to the appropriate list items in the dictionary
'''
def where_art_thou_bus(data_dict):
  time_block = []# keeps track of which prediction times the arrival time corresponds to
  for route in data_dict:
    for date in data_dict[route]:
      for stpid in data_dict[route][date]:
        for vid in data_dict[route][date][stpid]:
          prev_line = data_dict[route][date][stpid][vid][0]#first line of predicitons for the current vehicle
          time_block.append(prev_line)
          for line in data_dict[route][date][stpid][vid]:
            time_lag = line[1] - prev_line[1]#time difference between the last request made and current request
            pred_lag = line[2] - prev_line[2]#diff between the prediction from the last request and the prediction from the current request
            if time_lag <= 1:
              if abs(pred_lag)<=10:
                time_block.append(line)
              else:
                for v in data_dict[route][date][stpid][vid]:
                  if v in time_block and len(v)==3:
                    bus_pred=v[2]-v[0] #minutes predicted according to bus time
                    real_pred= v[2]-v[1] #minutes predicted according to real time
                    bus_diff=prev_line[1]-v[0] #minutes between this prediction (according to bus) and bus arrival
                    real_diff =  prev_line[1]-v[1] #minutes between this prediction (in real time) and bus arrival

                    v.extend([bus_pred, real_pred, bus_diff, real_diff, prev_line[1]])
                time_block = []

            elif abs(pred_lag)<=10:
                time_block.append(line)

            elif abs(prev_line[2] - prev_line [1])<2 :
              for v in data_dict[route][date][stpid][vid]:
                if v in time_block and len(v)==3:
                  bus_pred=v[2]-v[0] #minutes predicted according to bus time
                  real_pred= v[2]-v[1] #minutes predicted according to real time
                  bus_diff=prev_line[1]-v[0] #minutes between this prediction (According to bus) and bus arrival
                  real_diff =  prev_line[1]-v[1] #minutes between this prediction (in real time) and bus arrival
                  v.extend([bus_pred, real_pred, bus_diff, real_diff, prev_line[1]])

              time_block = []
            else:
                time_block = []
                time_block.append(line)
            prev_line = line
          time_block = []
  return data_dict


# Makes new dictionary that contains the difference between prediction times and arrival times
def mk_dist_dict(data_dict):
  distribution = {}
  for route in data_dict:
    if route not in distribution:
      distribution[route]={}
    for date in data_dict[route]:
      for stpid in data_dict[route][date]:
        if stpid not in distribution[route]:
          #Bus=time diff relative to "bus time" Official=time diff relative to real time
          distribution[route][stpid]={"Bus":{}, "Official":{}}
        for vid in data_dict[route][date][stpid]:
          for v in data_dict[route][date][stpid][vid]:
            if len(v) > 3:
              arr_bus = v[5]#how long it took for bus to arrive compared to "bus time"
              pred_bus = v[3]#how far in advance the prediction was made compared to "bus time"
              arr_official = v[6]#how long it took for bus to arrive compared to the real time
              pred_official = v[4]#how far in advance the prediction was made compared to the real time
              k= str(v[3])
              if arr_bus - pred_bus < abs(30):
                if k not in distribution[route][stpid]["Bus"]:
                  distribution[route][stpid]["Bus"][k] = [arr_bus - pred_bus]
                else:
                  distribution[route][stpid]["Bus"][k].append(arr_bus - pred_bus)

              k= str(v[4])
              if arr_official - pred_official < abs(30):
                if arr_official - pred_official < abs(30):
                  if k not in distribution[route][stpid]["Official"]:
                    distribution[route][stpid]["Official"][k] = [arr_official - pred_official]
                  else:
                    distribution[route][stpid]["Official"][k].append(arr_official - pred_official)
  return distribution

#Puts the errors from the distribution dictionary into a .txt file
def mk_r_csv(route,stop,distribution):
  if not os.path.exists("Output"):
    os.mkdir("Output")
  for time_type in distribution[route][stop]:
    for k in distribution[route][stop][time_type]:
      if int(k) >= 0 and int(k) <= 30:
        filename = k + "_" + str(route) + "_" + str(stop) + "_" + str(time_type) + ".txt"
        filename = os.path.join("Output",filename)
        with open(filename,"a") as f:
          writer = csv.writer(f)
          writer.writerow(distribution[route][stop][time_type][k])
  return

# Makes dictionary of the errors for the stops aggregated over all times
def mk_avg_dist_dict(data_dict):
  distribution = {}
  for route in data_dict:
    if route not in distribution:
      distribution[route]={}
    for date in data_dict[route]:
      for stpid in data_dict[route][date]:
        if stpid not in distribution[route]:
          distribution[route][stpid]=[]
        for vid in data_dict[route][date][stpid]:
          for v in data_dict[route][date][stpid][vid]:
             if len(v) > 3:
               arr_bus = v[5]
               pred_bus = v[3]
               if arr_bus - pred_bus < abs(30):
                 distribution[route][stpid].append(arr_bus - pred_bus)
  return distribution


# Puts errors based on stop (aggregated over all times) into a .txt file
def mk_avg_r_csv(route,stop, distribution):
  if not os.path.exists("Output"):
    os.mkdir("Output")
  filename = "AVG" + str(route) + "_" + str(stop) + ".txt"
  filename = os.path.join("Output",filename)
  with open(filename,"a") as f:
    writer = csv.writer(f)
    writer.writerow(distribution[route][stop])
  return

data_dict = mk_data_dict()
better = where_art_thou_bus(data_dict)
distribution = mk_dist_dict(better)

for r in distribution:
  for stop in distribution[r]:
    mk_r_csv(r, stop, distribution)

avg_dist_dict = mk_avg_dist_dict(data_dict)
for r in avg_dist_dict:
  for stop in avg_dist_dict[r]:
    mk_avg_r_csv(r, stop, avg_dist_dict)
