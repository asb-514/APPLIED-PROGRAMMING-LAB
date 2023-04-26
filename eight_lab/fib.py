def fib_nopt(x):
    """returns the xth fibonnaci number

    :x: TODO
    :returns: TODO

    """
    if x < 2:
        return 1
    curr = 1
    prev = 1
    for i in range(x - 1):
        curr,prev = curr + prev,curr

    return curr    
#for i in range(7):
    #print(fib(i))
