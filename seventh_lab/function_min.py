import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
def func(x):
    return x**2 + np.sin(8*x)
def mysimulated_anneling(func,start,temperature,decayrate):
    """function to implement simulated anneling

    :func: the function that has to be minimised
    :start: starting point
    :temperature: 
    :decayrate:
    :returns: the minima

    """
    bestcost = 100000
    bestx = start
    xbase = np.linspace(-2, 2, 100)
    ybase = func(xbase)
    rangemin, rangemax = -2, 2
    fig, ax = plt.subplots()
    ax.plot(xbase, ybase)
    xall, yall = [], []
    lnall,  = ax.plot([], [], 'ro')
    lngood, = ax.plot([], [], 'go', markersize=10)
    def onestep(frame):
        nonlocal bestcost, bestx, decayrate,temperature 
        # Generate a random value \in -2, +2
        dx = (np.random.random_sample() - 0.5) *temperature 
        x = bestx +dx
        y = func(x)
        if y < bestcost:
            bestcost = y
            bestx = x
            lngood.set_data(x, y)
        else :
            toss = np.random.random_sample()
            if toss < np.exp(-(y-bestcost)/temperature):
                bestcost = y
                bestx = x
                lngood.set_data(x, y)

        temperature = temperature * decayrate
        xall.append(x)
        yall.append(y)
        lnall.set_data(xall, yall)

    # return lngood,

    ani= FuncAnimation(fig, onestep, frames=range(100), interval=100, repeat=False)
    #ani.save('function_minimisation.gif')
    plt.show()
    for i in range(1000) :
        onestep(i)
    #fig.savefig('function_minimisation.jpeg')
    return bestx
bestx = mysimulated_anneling(func,-1,4,0.97)
print(f'The minimum value occurs at {bestx}, minimum being {func(bestx)}')
