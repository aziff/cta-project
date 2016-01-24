import csv
import numpy


def import_csv():
  data = []
  r = csv.reader(open('171schedule.csv','rt',newline=''), dialect='excel')
  for l in r:
    data.append(l)
  return data

if __name__ == '__main__':
  data = import_csv()
