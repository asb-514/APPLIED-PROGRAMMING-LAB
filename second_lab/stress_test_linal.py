import numpy as np
class MyLinalError(Exception):
    """raises custom errors"""

    def __init__(self,message):
        """constructor for the error class

        :message: the message that is displayed when a error occurs

        """
        Exception.__init__(self)
        self._message = message

def my_linal_solver(a,b):
    """will solve the system of equation given

    :a: The coefficient matrix
    :b: The constants matrix
    :returns: solution of the system of linear equation ax = b
    
    raises : MyLinalError when the matrix 'a' is singular 
    """
    #first converting the input to a numpy array and check for dimentions of a and b matrix 
    #and raising appropriate errors
   
    try:
        a = np.array(a,dtype = complex)
        b = np.array(b,dtype = complex)
        if len(a) != len(b):
            raise MyLinalError
    except ValueError as e:
        print('error : The dimentions of the matrix are not correct')
        return 
    except MyLinalError as e :
        print(format(e._message))
        return 
    
    #The solution to a system of equations do not change if we substract or add any 2 (distinct) of
    #the equations picked randomly (infact any linear combination of the picked equations)
    #and replace the newly 
    #created equation in place of any of the two picked equations.
    #for example :
    #   5x + 6y = 11  ...eq1
    #ans x + y = 2   ...eq2
    # have the same solutions as the system of equations - 
    #   4x + 5y = 9  (eq1 - eq2)
    #and x + y = 2

    #exploiting this fact we first convert the coefficient matrix(n x n dimensions) to a upper triangular matrix by 
    #first picking the topmost row and substract all the row's below (with a multipling factor) such as to elemenate 
    #all the elements in 1st coloum except for the pivot element(picking multiplying factor becomes more easier if leftmost element in the topmost row is 1, this is 
    #achived by dividing the whole
    #row by a[0][0], including the constant matrix). now (remember to perform the same substractions in the costant
    # matrix also) now pick the (n-1)x(n-1) matrix(the solution to the this matrix combined with the top row gives the the 
    #solution to the system of equation so now we have to find the solution to the n-1xn-1 matrix) and perform the same operations(to make all the elements below a[1][1] in the 
    #column to be zero and repeat it until you reach (like reccursion))
    # a 1x1 matrix, now we are left with a uppter triangular matrix
    
    #note :- assume a and b as augumented matrix,so any changes performed on 'a' shall also be performed on 'b'
    #we have to convert the uppter triangular matrix coefficient matrix to a identity matrix for finding the solution
    #Now we have to modify process done to find the upper triangular matrix, instead of starting from the above row, we start from teh 
    #bottomost row (n x n dimensions) and come to the topmost row (1x1 matrix)in a same recursive way , finaly the b matrix represents the 
    # solutions because 'a' matrix is identity matrix

    for i in range(0,len(a)):
        #partial pivoting (to decrease errors)
        #our method involves us to first divide the whole row by a[i][i] (taking norm, for ixi matrix in recursive method)
        #and we dont want a[i][i] to be a small number as this leads to blowing up of numbers in matrix so we swap
        #with a row which is in between (i,len(a)) (we cant select a row in [0,i) as this wont lead to a upper triangular matrix)
        #and has the highest absolute value comperted to a[j][i] for j belonging to [i,len(a)) this leads to stable solution rather that blowing up in values.
        
        
        # finding the index of row which has the highest absolute value
        index = i # max_value index
        for j in range(i,len(a)):
            if abs(a[j][i]) > abs(a[index][i]) :
                index = j
        #swapping
        a[[i,index]] = a[[index,i]]
        b[[i,index]] = b[[index,i]]
        # if the maximum element is also zero then the matrix is singular, consider ixi matrix formed with the first coloum entries all as 
        #zeros. it will have the none or infinite solutions so the solution to the previous matrix i+1 x i+1 also has none or infinite solution 
        # similarly the nxn matrix also has none or infinite solution.
        try :
            if abs(a[i][i]) == 0:
                raise MyLinalError("Exception occured : Matrix is singular")
        except MyLinalError as e:
            print (format(e._message))
            return 1

        #taking norm now
        for j in range(i + 1,len(a[i])):
            a[i][j] /=  a[i][i]
        b[i] /= a[i][i]
        a[i][i] = 1

        #substracting a[i] row from a[j] row with suitable multiplying factor
        for j in range(i + 1,len(a)):
            temp = (a[j][i]/a[i][i])
            for k in range(i + 1,len(a[i])):
                a[j][k] -= (temp)*a[i][k]
            b[j] -= (temp)*b[i]
            a[j][i] = 0

    #now we have the upper triangular matrix so we reverse our process from bottom to top, making elements in coefficient matrix zero
    for i in reversed(range(0,len(a))):
        for j in range(0,i):
            b[j] -= a[j][i]*b[i]
            a[j][i] = 0      #a[j][i] = a[j][i] - (a[j][i]/ a[i][i]) * a[i][i] = 0)  a[i][i] == 1 so multiplying factor is a[j][i] itself
    return b        
#A = np.random.randint(1,100,size=(3,3))
#B = np.random.randint(1,100,size=(3))
A = [[0,1,1],[3,2,1],[2,3,7]]
B = [5,10,29]

c= (my_linal_solver(A,B))
print(np.allclose(np.dot(A, c), B))

        
#i = 1 
#while i > 0 :
    #print(f'checking for {i} iteration')
    #i += 1
    #flag = 0
    #A1 = np.random.randint(1,100,size=(10,10))
    #B1 = np.random.randint(1,100,size=(10))
    #c = (my_linal_solver(A1,B1))
    #if np.allclose(np.dot(A1, c), B1) == 0:
        #print("ERROR!!!")
        #print(A1,B1,c)
        #print(np.allclose(np.dot(A1, c), B1))
        #print(np.linalg.det(A1))
        #d = np.linalg.solve(A1,B1)
        #print(d)
        #print(np.allclose(np.dot(A1, d), B1))
        #break

