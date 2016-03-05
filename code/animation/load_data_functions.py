# TODO
# make master function to include in accurate map


import csv


#Read in the stop/route information from the CSV files
def import_data(filename):
    data = []
    with open(filename, 'rU') as csvfile:
        reader = csv.reader(csvfile, delimiter = ',')
        for row in reader:
            data.append(row)
    return data
    
# extract one day
def one_day(day, data):
  one_day_list = []
  for row in data:
    if row[3] == day:
      one_day_list.append(row)
  return one_day_list

# separate 171 and 172 into two dictionaries 
def sep_routes(one_day_list):
  routes = ('171','172')
  list_171, list_172 = [], []
  
  for row in one_day_list:
    if row[0] == '171':
      list_171.append(row)
    elif row[0] == '172':
      list_172.append(row)
  return list_171, list_172  
  
# make dictionary of order and stop id
def mk_route_order(filename):
  data = import_data(filename)
  route_order = {}
  order = 1
  for row in data:
    if row[4] == 'S':
      if not row[0] in route_order:
        route_order[row[0]] = order
        order += 1
  return route_order
       
  
# sort by date, route, bus, time
def sort_list(route_list, route_order_dict):

  
  for row in route_list:
    if row[2] in route_order_dict:
      row.append(route_order_dict[row[2]])
    else:
      row.append('ERROR')
  
  route_list = sorted(route_list, key=lambda row: (row[1], row[4], row[5]))
  return route_list
    

DATA = '../../data/processed/'
FILE = 'cleaned-june2015.csv'
    
if __name__ == '__main__':
  csvfilename = DATA + FILE
  data = import_data(csvfilename)
  day1 = one_day('01jun2015', data)
  list_171, list_172 = sep_routes(day1)
  
  
  csvfilename = DATA + '171pattern.csv'
  order_171 = mk_route_order(csvfilename)
  
  sort_171 = sort_list(list_171, order_171)
  print sort_171
  for row in sort_171:
    print row
  

  
    