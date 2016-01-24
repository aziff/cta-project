'''
Code to stitch together .csv files that are scraped from the API
'''

# Filepaths
RAW_DATA = '../data/scraped-raw/'
SAVE_DATA = '../data/processed'

# Identify the .csv files that are in the folder
# Loop through .csv files that are in the folder
# read them in
# combine them excluding (1) headers and (2) blank lines

if __name__ == '__main__':
