def recurse(visited,coordinates,currcity = 0):
    """Recurse to find the solution to travelling salesman problem

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
