import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation
from matplotlib.animation import FuncAnimation
import math

fig, ax = plt.subplots()
xdata, ydata = [], []
ln, = ax.plot([], [], 'r')
def factorial(n):
    """computes the factorial of the number

    :n: the number for which factorial is computed
    :returns: the factorial of n

    """
    ans = 1
    for i in range(1,n+1):
        ans *= i
    return ans    
def init(): 
    ax.set_xlim(-1.2, 1.2) 
    ax.set_ylim(-1.2, 1.2) 
    return ln,
def circle(t):
    return np.cos(t), np.sin(t)
def morph(alpha,side_current,upflag,change):
    #print(len(x2))
    #side_current_temp = side_current
    #x1 = x1[::len(x1)//side_current]
    #y1 = y1[::len(y1)//side_current]
    #x2 = x2[::len(x2)//(side_current + 1)]
    #y2 = y2[::len(y2)//(side_current + 1)]
    if upflag == 0 and change != 1 :
        side_current -= 1
    t = []
    t = np.append(t,np.linspace(0,np.pi*2,side_current + 1))
    x4,y4 = circle(t)
    t = []
    t = np.append(t,np.linspace(0,np.pi*2,side_current + 2))
    x2,y2 = circle(t)
     
    xm = np.zeros(2*len(x4))
    ym = np.zeros(2*len(x4))
    alpha = alpha ** (0.7)
    for i in range(len(x4)):
        xm[2*i] = (alpha*(x2[i]) + (1-alpha)*(x4[i])) 
        xm[2*i + 1] = (alpha*(x2[i + 1]) + (1-alpha)*(x4[i])) 
        ym[2*i] = (alpha*(y2[i]) + (1-alpha)*(y4[i])) 
        ym[2*i + 1] = (alpha*(y2[i + 1]) + (1-alpha)*(y4[i]))
    return xm, ym
def update(frame):
    # xdata.append(frame)
    # ydata.append(np.sin(frame))
    global upflag
    #print(f'{upflag}')
    change = 0
    if upflag == 1 :
        temp2 = []
        for i in range(no_of_sides - 3) :
            temp2 = np.append(temp2 , np.linspace(i,i + 1,frame_max))
        side_current = 3 
        for f in temp2:
            if frame == 0 :
                break
            if f == 0 : 
                continue
            if f == int(f) :
                side_current = int(f) + 3
            if f == frame:
                break
        if side_current >= no_of_sides:
            side_current = no_of_sides - 1   
            #print('came')
            upflag = 0
            change = 1
        xdata, ydata = morph(frame  - side_current + 3,side_current,upflag,change) 
    else :
        temp3 = []
        for i in reversed(range(no_of_sides - 3)):
            i += 1
            temp3 = np.append(temp3 , np.linspace(i,i - 1,frame_max))
        side_current = no_of_sides 
        for f in temp3:
            if frame == 5 :
                break
            if f == 5 : 
                continue
            if f == int(f) :
                side_current = int(f) + 3
            if f == frame:
                break
        if side_current < 4 :
            side_current = 4   
        xdata, ydata = morph(frame - side_current + 4,side_current,upflag,change) 

    ln.set_data(xdata, ydata)
    return ln,

no_of_sides =  8
size1 = factorial(no_of_sides)
t = np.linspace(0*np.pi/4, 8*np.pi/4, size1)
if len(t) % 4 != 0:
    raise BaseException("Number of points should be multiple of 4...") 
#print(f"Square: {np.shape(x_polygon)}")
radius = 1
frame_max = 100
#plt.plot(polygons_x_coordinates[5],polygons_y_coordinates[5])
#plt.show()
temp = []
upflag = 1
for i in range(no_of_sides - 3):
    temp = np.append(temp ,np.linspace(i,i + 1,frame_max))
for i in reversed(range(no_of_sides - 3)):
    i += 1
    temp = np.append(temp ,np.linspace(i,i - 1,frame_max))
fig.suptitle("Name : Annangi Shashank Babu EE21B021")
ani = FuncAnimation(fig, update, frames=temp, init_func=init, blit=True, interval=10, repeat=False)
plt.show()

