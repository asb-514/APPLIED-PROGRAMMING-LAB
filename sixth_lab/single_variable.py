import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from functools import partial
from PIL import Image
import math
from numpy import cos, sin, pi, exp
class MyException(Exception):
    pass
def func(x):
    #testcase 1
    #return x ** 2 + 3 * x + 8

    #return x**4 - 3*x**2 + 1*x

    #testcase 2
    return cos(x)**4 - sin(x)**3 - 4*sin(x)**2 + cos(x) + 1

def min_finder(func,start,rangemin,rangemax, alpha = 0.1):
    """finds the local minima of the given function

    :func: The given input function of which minima must be found
    :start: The starting point
    :alpha: Learning rate DEFAULT VALUE 0.1
    :returns: the x and y value where minima occures

    """
    rangemax = math.ceil(rangemax)
    rangemin = math.ceil(rangemin)
    try :
        if start < rangemin or start > rangemax:
            raise MyException
    except MyException as e :
        print(f"Start value out of the range ({rangemin}, {rangemax})")
    xbase = np.linspace(rangemin,rangemax,(rangemax-rangemin)*30)
    ybase = func(xbase)
    fig,ax = plt.subplots()
    ax.plot(xbase,ybase,'k-')
    xall, yall = [], []
    lnall,  = ax.plot([], [], 'bo', alpha = 0.4)
    lngood, = ax.plot([], [], 'ro', alpha = 0.5, markersize=10)
    bestx = start
    bestcost = func(start)
    
    def single_step(frame):
        """single step of gradient desent

        """
        nonlocal func,bestx,xall,yall,lnall,lngood,alpha
        #print(bestx,alpha)
        x = bestx - (func(bestx + 1e-5) - func(bestx)) *1e5* alpha 
        bestx = x
        y = func(x)
        lngood.set_data(x, y)
        xall.append(x)
        yall.append(y)
        lnall.set_data(xall, yall)
    
    #animation runs for 10 times
    ani= FuncAnimation(fig, single_step, frames=range(10), interval=1000, repeat=False)

    #ani.save('gradient_decent_single_variable.gif')
    #ani.save('testcase_single_variable.gif')
    plt.show()
    #fig.savefig('gradient_decent_single_variable.jpg')
    #fig.savefig('testcase_single_variable.jpg')
    #fig.savefig('testcase_single_variable_2.jpg')
    
    #to get better results running it for some more iterations
    for i in range(0,1000):
        single_step(i)
    return bestx,func(bestx)

#testcase 1
#x,y = min_finder(func,3,-5,5,0.15)

#testcase 2
x,y = min_finder(func,0.1,0,2*np.pi,0.1)
print(f'Min occurs at x = {x},where y = {y}')
