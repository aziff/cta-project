'''
Code to stitch together .csv files that are scraped from the API
'''

import os
import numpy as np
from numpy import genfromtxt
import math
from time import time
import csv

from combine_csv_functions import get_files, get_route, read_csv, write_csv, split_date

# Filepaths
RAW_DATA = '../../data/scraped-raw/'
SAVE_DATA = '../../data/processed/'

if __name__ == '__main__':


  full_list = []

  file_list = get_files(RAW_DATA)

  for f in file_list:
    data = read_csv(f)
    full_list.append(data)

  csv_filename = SAVE_DATA + 'combined.csv'
  write_csv(csv_filename, full_list)
