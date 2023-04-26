def mysimulated_anneling(visited,coordinates,temperature,starting_order,decayrate):
    """using simulated anneling to solve tsp

    :visited: the array that keeps track of visited cities
    :coordinates: coordinates of the cities
    :starting_order: the starting plan of travel
    """
    global bestcost,bestorder
    random_order = np.copy(starting_order)
    random_order = shuffle(random_order)
    newcost = cost(random_order)
    if bestcost > newcost:
        bestcost = newcost
        bestorder = np.copy(random_order)
    else :
        toss = np.random.random_sample()
        if toss < np.exp(-(newcost-bestcost)/temperature) :
            bestcost = newcost
            bestorder = np.copy(random_order)
    temperature = decayrate * temperature
    return temperature

