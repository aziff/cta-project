import math
from numpy import genfromtxt

import numpy as np
from matplotlib import pyplot as plt

def get_x_y(csv):
    stops = genfromtxt(csv, delimiter = ",")
    lat1 = 41.78588506 # The origin is the most southwest stop (60/Ellis)
    lon1 = -87.60104835
    x = []
    y = []
    name = []

    for s in range(2,len(stops)):
        lat2 = stops[s,2]
        lon2 = stops[s,3]
    
        dx = (lon2-lon1)*40000*math.cos((lat1+lat2)*math.pi/360)/360
        dy = ((lat1-lat2)*40000/360) * -1
    
        x.append(dx)
        y.append(dy)
        name.append(stops[s,0])

    return (x,y, name)
    
#stops171 = get_x_y('171stops.csv')
#stops172 = get_x_y('172stops.csv')

#x171, y171, name171 = stops171[0], stops171[1] , stops171[2]
#x172, y172, name172 = stops172[0], stops172[1], stops172[2]

pattern171 = get_x_y('171pattern.csv')
pattern172 = get_x_y('172pattern.csv')


patx171, paty171 = pattern171[0], pattern171[1]
patx172, paty172 = pattern172[0], pattern172[1]

plt.plot(patx171,paty171)
plt.plot(patx172,paty172,color='r')
plt.show()


