'''
Code to stitch together .csv files that are scraped from the API
'''

import os
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

# Filepaths
RAW_DATA = '../../data/scraped-raw/'
SAVE_DATA = '../../data/processed'

# Identify the .csv files that are in the folder
def get_files(raw_dir):
  file_list = []
  for file in os.listdir(raw_dir):
    if file.endswith('.csv'):
      full_file = RAW_DATA + file
      file_list.append(full_file)
  return file_list

# Loop through .csv files that are in the folder
# read them in

# Read a csv file in
def read_csv(filename):
    data = []
    with open(filename, 'rU') as csvfile:
        reader = csv.reader(csvfile, delimiter = ',')
        for row in reader:
            if row != [' ']:
                data.append(row)
    return data

#def read_files(file_list, save_dir):


# combine them excluding (1) headers and (2) blank lines

if __name__ == '__main__':
  file_list = get_files(RAW_DATA)
  read_csv(file_list[0])
