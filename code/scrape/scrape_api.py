'''
Code to scrape and organize data from the CTA API
'''
import urllib
import csv
import xml.etree.ElementTree as ET
import os
import time

from scrape_api_functions import get_predictions, get_time, make_xml, parse_xml

# API keys
ANNA    = '6R2fNsXTiZKSzBaC2inDanrKy'
KUTAH   = 'hm4pjNYb4WFp9zS44ppn9EceY'
MYTHILI = 'Cej7swhuMsmDamZNj7ULZRVsH'

# Stop IDs
stops_171 = ['10561,17563,10563,15752,13197,17902,14020,15433,17423,1521', '1520,1518,15919,15816,16036,17057,10569,10566,10570,10567', '10569,10566,10570, 10567,10572,18012,14019,14020,14033,14034,17846', '15919']

stops_172 = ['13197,17902,14020,15433,17423,1646,1644,14039,14043,14040', '14041,15818,17057,18012,14019,14020,1523,1528,1525,15671', '14886,14033,14034,17846,14036,15817']

stops = {'171' : (stops_171, MYTHILI), '172' : (stops_172, ANNA)}

# URL
BEGURL  = 'http://www.ctabustracker.com/bustime/api/v1/'

# Header for the .csv
HEADER  = 'stpid', 'tmstmp','reptime', 'stpnm', 'prdtm', 'vid'

# Filepath to save data in .csv files
SAVE_DATA = '../../data/scraped-raw/'

if __name__ == '__main__':

    date_str = time.strftime('%d-%m-%Y')

    # Test this code during the weekdays!
    for r in stops.keys():
        for s in stops[r][0]:

            pred_xml_name = SAVE_DATA + r + '-pred.xml'
            time_xml_name = SAVE_DATA + r + '-time.xml'

            csv_name = SAVE_DATA + r + '-' + date_str + '.csv'

            pred_xml = make_xml(pred_xml_name, get_predictions(r, stops[r][1], s))

            time_xml = make_xml(time_xml_name, get_time(KUTAH))

            parse_xml(time_xml, pred_xml, csv_name)
