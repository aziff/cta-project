import matplotlib
matplotlib.use('TKAgg')

import numpy as np
from matplotlib import pyplot as plt

from matplotlib import animation
from numpy import genfromtxt

import math
from time import time


def load_stop_data(csv):
    data2 = genfromtxt(csv, delimiter = ",")
    t_data2 = np.transpose(data2)
    thisx = t_data2[0]
    print "thisx"
    print thisx
    thisy = t_data2[1]
    print "thisy"
    print thisy
    frames = len(thisx)
    return (thisx, thisy, frames)
    
def load_interval_data(csv):
    data = genfromtxt(csv, delimiter = ",")
    return data
    
def init():
    patch.center = (-10, -10)
    ax.add_patch(patch)
    return patch,

def animate(i):
    print "before"                                                 
    print a
    #global current_interval
    #current_interval = int(intervals[i])
    global a
    a = A[thisx*10]
    x, y = patch.center
    x = thisx[i]
    y = thisy[i]
    patch.center = (x, y)
    print "after"                                                 
    print a   
    return patch, 
    
intervals = load_interval_data("time172.csv")
data = load_stop_data("172routes.csv")
thisx = data[0]
thisy = data[1]
frames = data[2]

fig = plt.figure()
fig.set_dpi(100)
fig.set_size_inches(.7, .65)

ax = plt.axes(xlim=(0, 1), ylim=(0, 1))
plt.scatter(thisx, thisy)
plt.plot(thisx, thisy, 'r')

patch = plt.Circle((.5, -.5), 0.01, fc='y')
intervals = load_interval_data("time172.csv")

current_interval = 100
A = [1000,2000,3000,4000,5000,6000,7000,8000,9000,10000,11000,12000,13000,14000,15000,16000]
a = A[0]

anim = animation.FuncAnimation(fig, animate, 
                               init_func=init, 
                               frames=frames, 
                               interval=a,
                               blit=True,
                               repeat=True)


plt.show()


#anim.save('animation.mp4', fps=30, extra_args=['-vcodec', 'h264', '-pix_fmt', 'yuv420p'])
