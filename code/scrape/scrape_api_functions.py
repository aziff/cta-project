'''
Functions to scrape data from API
Functions to import to scrape-api.py:
  get_predictions
  get_time
  make_xml
  parse_xml
'''

import urllib
import csv
import xml.etree.ElementTree as ET
import os

# Stop ID's
stops_6 = '2815,1659,5037,14483,1421,1427,4872,5033,1651,5206'
stops_171 = '15919,10567,14033,14019,15433,16036,10563,1520'
stops_172 = '1523,15817,14033,14019,15433,14040,14039,16124'
stops_55 = '10565,15193,10589,10603,10615,14122,10502,10511,10536,10548'

# API keys
ANNA    = "6R2fNsXTiZKSzBaC2inDanrKy"
KUTAH   = "hm4pjNYb4WFp9zS44ppn9EceY"
MYTHILI = "Cej7swhuMsmDamZNj7ULZRVsH"

BEGURL  = "http://www.ctabustracker.com/bustime/api/v1/"

HEADER  = 'stpid', 'tmstmp','reptime', 'stpnm', 'prdtm', 'vid'

# Make string to get predictions from API
def get_predictions(route, key, stops):
  request = BEGURL + "getpredictions?key=" + key + "&rt=" + route + "&stpid=" + stops
  return request

# Make string to get time
def get_time(key):
  return BEGURL + "gettime?key=" + key

# Construct the XML file
def make_xml(xmlname, request_function):
  u = urllib.urlopen(request_function)
  f = open(xmlname,'w')
  f.write(u.read())
  f.close()
  return xmlname

# Parse the XML file
def parse_xml(xmlfile_time, xmlfile_pred, csvfile):
  tree_time = ET.parse(xmlfile_time)
  root_time = tree_time.getroot()
  tree_pred = ET.parse(xmlfile_pred)
  root_pred = tree_pred.getroot()
  header = HEADER
  with open(csvfile, 'a') as f:
    writer = csv.writer(f)
    writer.writerow(" ")
    reptime = root_time.findtext('tm')
    for prd in root_pred.findall('prd'):
      stpid = prd.findtext('stpid')
      tmstmp = prd.findtext('tmstmp')
      stpnm = prd.findtext('stpnm')
      prdtm = prd.findtext('prdtm')
      vid = prd.findtext('vid')
      row = stpid, tmstmp, reptime, stpnm, prdtm, vid
      writer.writerow(row)
  return
