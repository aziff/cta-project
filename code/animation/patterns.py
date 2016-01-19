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

# Direction
directions = 'Northbound','Southbound'

# API keys
ANNA= "6R2fNsXTiZKSzBaC2inDanrKy"
KUTAH= "hm4pjNYb4WFp9zS44ppn9EceY"

BEGURL= "http://www.ctabustracker.com/bustime/api/v1/"

HEADER= 'stpid','stpnm','lat','lon', 'type'

# Make string to get stop locations
def get_stops(route, key):
  request = BEGURL + "getpatterns?key=" + key + "&rt=" + route
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
  header = HEADER
  with open(csvfile, 'a') as f:
    writer = csv.writer(f)
    writer.writerow(header)
    
    for ptr in root_stop.findall('ptr'):
      for prd in ptr.findall('pt'):
        stpid = prd.findtext('stpid')
        stpnm = prd.findtext('stpnm')
        lat = prd.findtext('lat')
        lon = prd.findtext('lon')
        type = prd.findtext('typ')
        row = stpid, stpnm, lat, lon, type
      
        writer.writerow(row)
  return


'''
Running this block of code gets the XML files and puts them into .csv files
'''

stops171_xml = make_xml('P171-stops.xml', get_stops('171',ANNA))
stops172_xml = make_xml('P172-stops.xml', get_stops('172',ANNA))
parse_xml(stops171_xml, 'P171stops.csv')
parse_xml(stops172_xml, 'P172stops.csv')



