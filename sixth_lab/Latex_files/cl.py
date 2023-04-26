def min_finder(func,minlim,maxlim,start,alpha):
    """finds the local minima of the given function

    :func: The given input function of which minima must be found
    :start: The starting point
    :alpha: Learning rate
    :returns: the x and y value where minima occures

    """
    #rangemin,rangemax = -2,2
    start = np.array(start)
    rangemax = np.full(len(start), maxlim)
    rangemin = np.full(len(start), minlim)
    try:
        pass
    except Exception as e:
        raise e 
    try :
        if start.any() < rangemin.any() or start.any() > rangemax.any():
            raise MyException
    except MyException as e :
        print(f"Start value out of the range ({rangemin}, {rangemax})")
    bestx = []
    for i in range(len(start)):
        bestx = np.append(bestx,start[i])
    def single_step(frame):
        """single step of gradient desent
        """
        nonlocal func,bestx,alpha
        t = np.zeros(len(bestx))
        for i in range(len(bestx)):
            temp_bestx = np.copy(bestx)
            temp_bestx[i] -= 1e-5
            t[i] = bestx[i] - (func(bestx) - func(temp_bestx)) * 1e5 * alpha
        bestx = t
    
    for i in range(1000):
        single_step(i)        

    return bestx,func(bestx)

