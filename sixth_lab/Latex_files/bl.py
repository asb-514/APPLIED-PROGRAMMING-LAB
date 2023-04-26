def min_finder(func,start,min_lim,max_lim,alpha = 0.1):
    """finds the local minima of the given function

    :func: The given input function of which minima must be found
    :start: The starting point
    :alpha: Learning rate
    :returns: the x and y value where minima occures

    """
    start = np.array(start)
    rangemax = np.full(len(start), math.ceil(max_lim))
    rangemin = np.full(len(start),math.floor(min_lim))
    try:
        pass
    except Exception as e:
        raise e 
    try :
        if start.any() < rangemin.any() or start.any() > rangemax.any():
            raise MyException
    except MyException as e :
        print(f"Start value out of the range ({rangemin}, {rangemax})")
    ybase = np.linspace(rangemin[0],rangemax[0],(rangemax[0] - rangemin[0])*100)
    xbase = np.linspace(rangemin[0],rangemax[0],(rangemax[0] - rangemin[0])*100)
    xbase, ybase = np.meshgrid(xbase, ybase)
    z = func(xbase,ybase)
    fig = plt.figure(figsize=(10, 10))
    ax = fig.add_subplot(111, projection='3d')
    ax.set_xlim3d([rangemin[0], rangemax[0]])
    ax.set_xlabel('X')

    ax.set_ylim3d([rangemin[0], rangemax[0]])
    ax.set_ylabel('Y')

    #ax.set_zlim3d(func(rangemin[0], rangemax[0]))
    ax.set_zlabel('Z')
    ax.plot_surface(xbase,ybase,z,cmap = 'binary',alpha = 0.4)
    xall, yall ,zall = [], [], []
    lnall,  = ax.plot([],[],[], 'k--')
    lngood, = ax.plot([],[],[], 'ro',alpha = 0.5, markersize=10)
    bestx = start[0]
    besty = start[1]
    bestcost = func(*start)

    def single_step(frame):
        """single step of gradient desent
        """
        nonlocal func,bestx,besty,xall,yall,lnall,lngood,alpha,zall
        x = [0]
        y = [0]
        z = [0]
        # the derivative is found from the (y2-y1)/(x2-x1) rather from the given function 
        x[0] = bestx - (func(bestx,besty) - func(bestx - 1e-5,besty)) * alpha * 1e5
        y[0] = besty - (func(bestx,besty) - func(bestx,besty - 1e-5)) * alpha * 1e5
        bestx = x[0]
        besty = y[0]
        z[0] = func(x[0],y[0])
        lngood.set_data(x,y)
        lngood.set_3d_properties(z)
        xall.append(x[0])
        yall.append(y[0])
        zall.append(z[0])
        lnall.set_data(xall,yall)
        lnall.set_3d_properties(zall)
        #return lnall,
    
    ani = FuncAnimation(fig, single_step, frames=range(10), interval=1000, repeat=False)
    plt.show()
    for i in range(1,10000):
        single_step(i)
    return bestx,besty,func(bestx,besty)


