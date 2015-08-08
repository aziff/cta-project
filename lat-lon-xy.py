import math
from numpy import genfromtxt

import numpy as np
from matplotlib import pyplot as plt

def get_x_y(csv):
    stops = genfromtxt(csv, delimiter = ",")
    lat1 = 41.78588506
    lon1 = -87.60104835
    x = []
    y = []

    for s in range(2,len(stops)):
        lat2 = stops[s,2]
        lon2 = stops[s,3]
    
        dx = (lon2-lon1)*40000*math.cos((lat1+lat2)*math.pi/360)/360
        dy = ((lat1-lat2)*40000/360) * -1
    
        x.append(dx)
        y.append(dy)

    return (x,y)
    
stops171 = get_x_y('171stops.csv')
stops172 = get_x_y('172stops.csv')

x171 = stops171[0]
y171 = stops171[1] 
x172 = stops172[0]
y172 = stops172[1]

for v in [x171,x172,y171,y172]:
    print v
    print len(v)

plt.scatter(x171,y171)
plt.scatter(x172,y172,color='r')
plt.show()


