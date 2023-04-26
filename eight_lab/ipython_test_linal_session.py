# coding: utf-8
get_ipython().system('python3 setup_linal_solver.py build_ext -if')
from linal_solver import my_linal_solver
import numpy as np
A = np.random.randint(1,100,size=(100,100))
B = np.random.randint(1,100,size=(100))
A = np.array(A,dtype = complex)
B = np.array(B,dtype = complex)
get_ipython().run_line_magic('timeit', 'my_linal_solver(A,B)')
get_ipython().run_line_magic('run','linal_solver.py')
get_ipython().run_line_magic('timeit', 'my_linal_solver_nopt(A,B)')
