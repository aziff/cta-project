'''
Heavily utilized direction and code from David Beazley's talk:
http://pyvideo.org/video/1725/learn-python-through-public-data-hacking
We took the flow of Beazley's code, and abstracted it to functions,
and put the functions together to get the exact .csv's we desired.

XML ElementTree library heavily utilized
https://docs.python.org/2/library/xml.etree.elementtree.html

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
ANNA= "6R2fNsXTiZKSzBaC2inDanrKy"
KUTAH= "hm4pjNYb4WFp9zS44ppn9EceY"

BEGURL= "http://www.ctabustracker.com/bustime/api/v1/"

HEADER= 'stpid', 'tmstmp','reptime', 'stpnm', 'prdtm', 'vid'

# Make string to get predictions
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

'''

Running this block of code gets the XML files. Do not modify.

'''
pred171_xml = make_xml('171-test-pred.xml', get_predictions('171',ANNA, stops_171))
pred172_xml = make_xml('172-test-pred.xml', get_predictions('172',ANNA, stops_172))
pred55_xml = make_xml('55-test-pred.xml', get_predictions('55',ANNA, stops_55))
pred6_xml = make_xml('6-test-pred.xml', get_predictions('6',ANNA, stops_6))

'''

Running this block parses the XML files into .csv files
We changed the dates and times in the filenames everytime we ran
the code in order to differentiate between the different days.
However, for testing purposes, it is fine to run the below block.
The data that will be collected will be for the moment the code is
run, not 2/9/15.

'''
time_xml = make_xml('171-test-time.xml',get_time(ANNA))
parse_xml(time_xml, pred171_xml, '2-9-15_AZ_171_1430.csv')
parse_xml(time_xml, pred172_xml, '2-9-15_AZ_172_1430.csv')
parse_xml(time_xml, pred55_xml, '2-9-15_AZ_55_1430.csv')
parse_xml(time_xml, pred6_xml, '2-9-15_AZ_6_1430.csv')
