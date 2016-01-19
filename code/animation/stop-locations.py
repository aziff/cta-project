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
#stops_171 = '15919,10567,14033,14019,15433,16036,10563,1520'
#stops_172 = '1523,15817,14033,14019,15433,14040,14039,16124'

# Direction
directions = 'Northbound','Southbound'

# API keys
ANNA= "6R2fNsXTiZKSzBaC2inDanrKy"
KUTAH= "hm4pjNYb4WFp9zS44ppn9EceY"

BEGURL= "http://www.ctabustracker.com/bustime/api/v1/"

HEADER= 'stpid','stpnm','lat','lon'

# Make string to get stop locations
def get_stops(route, key, direction):
  request = BEGURL + "getstops?key=" + key + "&rt=" + route + "&dir=" + direction
  return request

# Construct the XML file
def make_xml(xmlname, request_function):
  u = urllib.urlopen(request_function)
  f = open(xmlname,'w')
  f.write(u.read())
  f.close()
  return xmlname

# Parse the XML file
def parse_xml(xmlfile_stops, csvfile):
  tree_stop = ET.parse(xmlfile_stops)
  root_stop = tree_stop.getroot()
  print(root_stop)
  header = HEADER
  with open(csvfile, 'a') as f:
    writer = csv.writer(f)
    writer.writerow(header)
    
    for prd in root_stop.findall('stop'):
      print "prd"
      print prd
      stpid = prd.findtext('stpid')
      stpnm = prd.findtext('stpnm')
      lat = prd.findtext('lat')
      lon = prd.findtext('lon')
      row = stpid, stpnm, lat, lon
      
      writer.writerow(row)
  return


'''
Running this block of code gets the XML files and puts them into .csv files
'''
for dir in directions:
    stops171_xml = make_xml(dir+'171-stops.xml', get_stops('171',ANNA, dir))
    stops172_xml = make_xml(dir+'172-stops.xml', get_stops('172',ANNA, dir))
    parse_xml(stops171_xml, dir+'171stops.csv')
    parse_xml(stops172_xml, dir+'172stops.csv')



