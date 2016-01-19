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

stops_171 = ['10561, 17563, 10563, 15752, 13197, 17902, 14020, 15433, 17423, 1521', '1520, 1518, 15919, 15816, 16036, 17057, 10569, 10566, 10570, 10567', '10569, 10566, 10570, 10567, 10572, 18012, 14019, 14020, 14033, 14034, 17846', '15919']

stops_172 = ['13197, 17902, 14020, 15433, 17423, 1646, 1644, 14039, 14043, 14040', '14041, 15818, 17057, 18012, 14019, 14020, 1523, 1528, 1525, 15671', '14886, 14033, 14034, 17846, 14036, 15817']

# Old stops used from CS122
#stops_171 = '15919,10567,14033,14019,15433,16036,10563,1520'
#stops_172 = '1523,15817,14033,14019,15433,14040,14039,16124'

routes = ['171', '172']

# API keys
ANNA    = "6R2fNsXTiZKSzBaC2inDanrKy"
KUTAH   = "hm4pjNYb4WFp9zS44ppn9EceY"
MYTHILI = "Cej7swhuMsmDamZNj7ULZRVsH"

BEGURL  = "http://www.ctabustracker.com/bustime/api/v1/"

HEADER  = 'stpid', 'tmstmp','reptime', 'stpnm', 'prdtm', 'vid'

if __name__ == '__main__':

    date_time = time.strftime("%d-%m-%Y")
    csv_name171 = 'output/171_' + date_time + ".csv"
    csv_name172 = 'output/172_' + date_time + ".csv"

    for i in stops_171:
        pred171_xml = make_xml('output/171-test-pred.xml', get_predictions('171',MYTHILI, i))
        print "new loop 171"
        print i

        time_xml = make_xml('output/171-test-time.xml',get_time(KUTAH))
        parse_xml(time_xml, pred171_xml, csv_name171)

    for i in stops_172:
        pred172_xml = make_xml('output/172-test-pred.xml', get_predictions('172',ANNA, i))
        print i

        time_xml = make_xml('output/171-test-time.xml',get_time(KUTAH))
        parse_xml(time_xml, pred172_xml, csv_name172)
