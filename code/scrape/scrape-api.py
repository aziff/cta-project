'''
Code to scrape and organize data from the CTA API
'''
import urllib
import csv
import xml.etree.ElementTree as ET
import os
import time

from scrape_api_functions import get_predictions, get_time, make_xml, parse_xml

# Stop ID's
stops_6 = '2815,1659,5037,14483,1421,1427,4872,5033,1651,5206'
stops_171 = '15919,10567,14033,14019,15433,16036,10563,1520'
stops_172 = '1523,15817,14033,14019,15433,14040,14039,16124'
stops_55 = '10565,15193,10589,10603,10615,14122,10502,10511,10536,10548'

routes = ['171', '172']

# API keys
ANNA    = "6R2fNsXTiZKSzBaC2inDanrKy"
KUTAH   = "hm4pjNYb4WFp9zS44ppn9EceY"
MYTHILI = "Cej7swhuMsmDamZNj7ULZRVsH"

BEGURL  = "http://www.ctabustracker.com/bustime/api/v1/"

HEADER  = 'stpid', 'tmstmp','reptime', 'stpnm', 'prdtm', 'vid'

if __name__ == '__main__':

    date_time = time.strftime("%d-%m-%Y_%I-%M-%S")
    csv_name171 = 'output/171_' + date_time + ".csv"
    csv_name172 = 'output/172_' + date_time + ".csv"


    pred171_xml = make_xml('output/171-test-pred.xml', get_predictions('171',ANNA, stops_171))
    pred172_xml = make_xml('output/172-test-pred.xml', get_predictions('172',ANNA, stops_172))

    time_xml = make_xml('output/171-test-time.xml',get_time(ANNA))
    parse_xml(time_xml, pred171_xml, csv_name171)
    parse_xml(time_xml, pred172_xml, csv_name172)
