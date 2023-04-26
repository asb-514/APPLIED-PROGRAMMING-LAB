import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import sys

def distance(a,b):
    """finds distance between 2 coordinates

    :a: TODO
    :b: TODO
    :returns: TODO

    """
    return np.sqrt(np.square((a[0] - b[0])) + np.square(a[1] - b[1]))

def cost(order):
        """calculates the cost for the given order

        :order: TODO
        :returns: TODO

        """
        global coordinates
        cost = 0
        for i in range(len(coordinates)):
            cost += distance(coordinates[order[i]],coordinates[order[i-1]])
        return cost


def recurse(visited,coordinates,currcity = 0):
    """Recurse to find the solution to travelling salesman problem

    :visited: TODO
    :coordinates: TODO
    :returns: TODO

    """
    order = []
    order.append(currcity)
    if visited.all() == 1:
        return distance(coordinates[currcity],coordinates[0]),order
    ans = 1e100
    for i in range(len(visited)):
        if visited[i] == 0 :
            visited_updated = np.copy(visited)
            visited_updated[i] = 1
            ansnew, ordernew = recurse(visited_updated,coordinates,i)
            ordernew = np.copy(ordernew)
            ansnew += distance(coordinates[i],coordinates[currcity])
            if ansnew < ans:
                ans = ansnew
                ordermin = np.copy(ordernew)
    order = np.append(order,ordermin)
    return ans,order

def read(filename):
    """the initial setup

    :filename: TODO
    :returns: TODO

    """
    with open(filename) as f:
        f = f.readlines()
        n = int(f[0])
    visited = np.zeros(n,dtype = 'int')
    coordinates = np.zeros((n,2),dtype = 'float')
    with open(filename) as f:
        i = 0
        for line in f:
            if len(line.split()) != 1 :
                coordinates[i][0] = float(line.split()[0])
                coordinates[i][1] = float(line.split()[1])
                i += 1
    visited[0] = 1
    return visited,coordinates
def myplot(coordinates,order):
    """plots the final route to traverse

    :coordinates: TODO
    :order: TODO
    :returns: TODO

    """
    xplot = [coordinates[order[i]][0] for i in range(len(order))]
    yplot = [coordinates[order[i]][1] for i in range(len(order))]
    xplot = np.append(xplot, xplot[0])
    yplot = np.append(yplot, yplot[0])
    plt.plot(xplot, yplot, 'o-')
    #plt.savefig('r_tsp10.jpeg')
    plt.show()
visited,coordinates = read('int1.txt')
ans,order = recurse(visited,coordinates)
print(ans,order)
#with open('r_out10.txt','w') as f:
    #f.write(str(cost(order)))
    #f.write('\n')
    #f.write('\n')
    #for i in range(len(order)):
        #f.write(str(order[i]))
        #f.write('\n')


myplot(coordinates,order)

