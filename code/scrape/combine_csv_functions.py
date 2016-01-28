'''
Functions to stitch together .csv files that are scraped from the API
'''

import os
import numpy as np
from numpy import genfromtxt
import math
from time import time
import csv

# Filepaths
RAW_DATA = '../../data/scraped-raw/'
SAVE_DATA = '../../data/processed/'

'''
Identify the .csv files that are in the folder
'''
def get_files(raw_dir):
  file_list = []
  for file in os.listdir(raw_dir):
    if file.endswith('.csv'):
      full_file = RAW_DATA + file
      file_list.append(full_file)
  return file_list

# Loop through .csv files that are in the folder
# read them in


'''
Split date and time variables
'''
def split_date(row):
  cols_to_split = [1,3,6]

  for j in cols_to_split:
    date_time = row[j].split()
    row[j:j+1] = date_time
  return row


'''
Extract bus route
'''
def get_route(filename):
  split_path = filename.split('/', filename.count('/'))
  split_name = split_path[-1].split('_', split_path[-1].count('_'))
  if len(split_name) == 2:
    return split_name[0]
  else:
    return 'error'


'''
Read a csv file
'''
def read_csv(filename):
  data = []
  route = get_route(filename)
  with open(filename, 'rU') as csvfile:
    reader = csv.reader(csvfile, delimiter = ',')
    for row in reader:
      if row != [' ']:
        row.append(route)
        data.append(row)
  return data


'''
Write a new combined csv file
'''
def write_csv(filename, full_list):
  with open(filename, 'wb') as csvfile:
    writer = csv.writer(csvfile, delimiter=',')
    for date in full_list:
      for row in date:
        row = split_date(row)
        writer.writerow(row)
  return
