#!python
#cython: language_level=3
# distutils: language = c++
# cython: boundscheck = False
# cython: wraparound = False
# cython: nonecheck = False


cpdef long long fib(int x):
    """returns the xth fibonnaci number

    :x: TODO
    :returns: TODO

    """
    if x < 2:
        return 1
    cdef long long curr = 1   #chance of overflow so defined as long long
    cdef long long prev = 1
    cdef int i

    for i in range(x - 1):
        curr,prev = curr + prev,curr

    return curr    
#for i in range(7):
    #print(fib(i))
