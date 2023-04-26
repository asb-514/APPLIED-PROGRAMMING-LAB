#!python
#cython: language_level=3
#cython:profile=True


# distutils: language = c++
# distutils: extra_compile_args = -Wall -O3 -ffast-math -ffinite-math-only -funsafe-math-optimizations -funsafe-math-optimizations -Wno-unreachable-code-fallthrough




cimport numpy as np
import numpy as np
cimport cython

cdef extern from "helper.h":
    float norm2(float a,float b)

@cython.boundscheck(False)
@cython.wraparound(False)
@cython.nonecheck(False)
@cython.cdivision(True)
cpdef np.ndarray[np.complex128_t, ndim=1] my_linal_solver(np.ndarray[np.complex128_t, ndim=2] a, np.ndarray[np.complex128_t, ndim=1] b):
    # Define typed memoryviews for a and b
    cdef np.complex128_t[:, :] virtual_a = a
    cdef np.complex128_t[:] virtual_b = b
    
    # Define loop variables
    cdef int i, j, k, N = len(a)
    cdef int index
    cdef float temp1_real, temp2_real, temp2_imag, temp1_imag
    cdef np.complex128_t temp
    
    for i in range(N):
        index = i  # max_value index
        for j in range(i, N):
            temp1_real = float(virtual_a[j, i].real)
            temp2_real = float(virtual_a[index, i].real)
            temp2_imag = float(virtual_a[index, i].imag)
            temp1_imag = float(virtual_a[j, i].imag)
            if norm2(temp1_real, temp1_imag) > norm2(temp2_real, temp2_imag):
                index = j
        
        # swapping
        virtual_a[i, index] = virtual_a[index, i]
        virtual_b[i],virtual_b[index] = virtual_b[index],virtual_b[i]
        
        # if the maximum element is also zero then the matrix is singular
        temp1_real = float(virtual_a[i, i].real)
        temp1_imag = float(virtual_a[i, i].imag)
        if norm2(temp1_real, temp1_imag)== 0:
            print("Exception occured : Matrix is singular")
            return np.array([-1])
        
        # taking norm now
        for j in range(i + 1, N):
            virtual_a[i, j] /= virtual_a[i, i]
        virtual_b[i] /= virtual_a[i, i]
        virtual_a[i, i] = 1
        
        # subtracting a[i] row from a[j] row with suitable multiplying factor
        for j in range(i + 1, N):
            temp = (virtual_a[j, i] / virtual_a[i, i])
            for k in range(i + 1, N):
                virtual_a[j, k] -= (temp) * virtual_a[i, k]
            virtual_b[j] -= (temp) * virtual_b[i]
            virtual_a[j, i] = 0
    
    # now we have the upper triangular matrix so we reverse our process from bottom to top, making elements in coefficient matrix zero
    for i in reversed(range(0, N)):
        for j in range(0, i):
            virtual_b[j] -= virtual_a[j, i] * virtual_b[i]
            virtual_a[j, i] = 0
    return np.array(virtual_b)
