import numpy as np
error_flag = 0
class MyCircuitSolver(Exception):

    """Raises custom errors"""

    def __init__(self,message):
        """constructor
        :message: custom message to be shown

        """
        Exception.__init__(self)

        self._message = message
        
def parse_value(string):
    """converts the string in to a number to pursue computations

    :string: takes a string as input (ex : 2K, 3m ,5u )
    :returns: returns a float value representing the string (ex :  2k --> 2000) 

    """
    convert_dict = {'K': '1e3','k': '1e3', 'M': '1e6', 'G': '1e9', 'n' : '1e-9','N' : '1e-9' ,'m' : '1e-3','u':'1e-6','p' : 
                        '1e-12'}
    t_val =''
    for letter in string.split() :
        if letter in convert_dict.keys():
            t_val = float(t_val)*float(convert_dict[letter])
            break
        t_val += letter
    return float(t_val)

class Circuit_Element():

    """General Class for R,L,C,V,I circuit elements"""

    def __init__(self,line):
        """constructor for this class

        :line: Takes the a line from spice netlist as a input and parses it 

        """
        #attributes of this class
        self._line = line
        self._split_line = line.split()
        self._name = self._split_line[0]
        self._first_node = self._split_line[1]
        self._second_node = self._split_line[2]

        if len(self._split_line) == 4:  #ex : R1 GND 1 2k  # so passive element will have 4 as length of split line active element 
                                                        #    has 4 as the length of the split line
            # r,l or c
            self._type = 'passive'
            self._value = complex(parse_value(self._split_line[3]),0)
        else :
            self._type = 'active'
            if self._split_line[3] == 'dc':
                # dc source v/i
                self._ac_flag = 0
                self._value = complex(parse_value(self._split_line[4]),0)
            else :
                #ac source  v/i
                self._ac_flag = 1
                #phase is assumed to be given in degres !!!
                self._phase = (float(self._split_line[5])/180)*(np.pi)
                self._value = complex(parse_value(self._split_line[4])*np.cos(self._phase),parse_value(self._split_line[4])*np.sin(self._phase))
                
    def name(self):
        """conveys the name of the element
        """
        return self._name
    def impedance(self, omega):
        """calculates the impedance of the element for given omega
        :omega: the operating frequency 
        :returns: impedance of the passive element

        """
        if self._name[0] == 'R':
            return self._value
        elif self._name[0] == 'L':
            return complex(0,self._value * omega)
        elif self._name[0] == 'C' :
            if omega == 0: 
                # impedance is infinity for dc sources to get steady state value
                return complex(0,-np.finfo(np.float64).max)
            return complex(0,-(1)/(omega*self._value))
    def admittance(self, omega):
        """calculates the admitance of the passive element for given omega

        :omega: The operating frequency
        :returns: admittance of the passive element

        """
        if omega != 0 or self._name[0] == 'R' :
            return 1/self.impedance(omega)
        elif self._name[0] == 'L':
            return complex(0,np.finfo(np.float64).max)
        elif self._name[0] == 'C' :
            return complex(0,0)

    def type(self):
        """says whether the element is active or not
        """
        return self._type
    def first_node(self):
       """returns the first node from the parsed line
       """
       return self._first_node 
    def second_node(self):
       """returns the second node from the parsed line
       """
       return self._second_node
    def value(self):
       """returns the value of the element from parsed line
       """
       return element._value

def _file_lines_of(filename):
    """used to divide the file into lines

    :filename: The name of the file that should be opened
    :returns: a list containing the lines of the given file

    """
    file_lines = []
    try :
        with open(f) as file_objects:
            for line in file_objects:
                file_lines.append(line)
    except FileNotFoundError :
        error_flag = 1
        print('error : File not present in the directory')
        return 
    return file_lines


def find_frequency(file_lines):
    """finds the value of frequency (if ac circuit is given)

    :file_lines: a list containing lines from netlist
    :returns: return frequency if given circuit is ac, if there is no ac source (or frequency not mentioned in netlist)

    """
    for line in file_lines:
        if len(line.split()) != 0 and line.split()[0] == '.ac':
            freq = line.split()[2]
            return parse_value(freq)
    return 0
def unknowns(dic):
    """this function creates a map to keep track of the information of unknowns

    :dic: the nodal_equation_dict is given as input.
    :returns: a map containing the unknowns (that have to be found).

    """
    unknowns_map = {}
    index = 0
    for node1 in dic.keys():
        for unknowns in dic[node1].keys():
            if unknowns not in unknowns_map.keys() and unknowns != 'CONSTANT':
                unknowns_map[unknowns] = index
                index += 1
    return unknowns_map            
def add_to_dict(dictionary,first_node,second_node,val):
    """function helps in maintaining and adding elements to the dict 

    :dictionary: dictionary to which element must be added
    :first_node: first_node represents where at which node is the nodal equation is being written at
    """
    if first_node not in dictionary.keys():
        dictionary[first_node] = {}   
    if second_node not in dictionary[first_node].keys():
        dictionary[first_node][second_node] = complex(float(0),float(0))
    dictionary[first_node][second_node] += complex(val)
    return 

#now we will form the matrix that is obtained from nodal equation

#in nodal_equation_dict[key1][key2] (nodal_eqation_dict is a map of maps), the key1 represensts the node at which the nodal eq is written and 
# nodal_equation_dict[key1][key2] represents the coefficient of the "key2" in the equation formed at node of key1


#read from file
f = input('please enter the input:')
file_lines = _file_lines_of(f)

#this dict maintains the system of nodal equations
nodal_equation_dict = {}  

#find frequency
omega = find_frequency(file_lines)*2*np.pi  

#finding the index at which .circuit  and .end are present
start = '.circuit'
end = '.end'
start_index = -1 
end_index = -1 
#should we give error for one dc and one ac source?
for line in file_lines:
    if start == line[:len(start)]:
        start_index = file_lines.index(line)
    elif end == line[:len(end)] :
        end_index = file_lines.index(line)
try :        
    if end_index <= start_index:
        raise MyCircuitSolver('Error : the given circuit is invalid')
except MyCircuitSolver as e:
    error_flag = 1
    print(f'{e._message}')


for line in file_lines[start_index+1 : end_index] :
    #now we have to ignore the comments in the netlist
    line = line.split('#')[0]  
    
    if line.split()[0][0] == '#':
        continue   #skips a line starting with comment between .circuit and .end
    try :
        if line.split()[0][0] != 'V' and line.split()[0][0] != 'I' and line.split()[0][0] != 'R' and line.split()[0][0] != 'L' and line.split()[0][0] != 'C':
            raise MyCircuitSolver('ERROR : unidentified component')
    except MyCircuitSolver as e:
        error_flag = 1
        print(f'{e._message}')
    element = Circuit_Element(line)

    #nodal equation --> sum of total current leaving a node is zero
    if element.type() == 'passive':
        #passive element stamp

        #second argument in add_to_dict represents the node at which nodal equation is written, nodal_eqation_dict[node1][node2]
        #represents the coefficient of V_node2(unknown) in the nodal equation at node1
        #effect of passive element on nodal equation at first_node
        add_to_dict(nodal_equation_dict,'V(' + element.first_node() +')','V(' + element.first_node() +')',element.admittance(omega))
        add_to_dict(nodal_equation_dict,'V(' + element.first_node() +')','V(' + element.second_node() +')',-element.admittance(omega))

       #effect of passive element on nodal equation at second_node 
        add_to_dict(nodal_equation_dict,'V(' + element.second_node() +')','V(' + element.second_node() +')',element.admittance(omega))
        add_to_dict(nodal_equation_dict,'V(' + element.second_node() +')','V(' + element.first_node() +')',-element.admittance(omega))

    else :
        try:
            if (element._ac_flag == 1 and omega == 0) or (element._ac_flag == 0 and omega != 0):
                raise MyCircuitSolver('ERROR : both ac and dc sources are involved')
        except MyCircuitSolver as e:
            error_flag = 1
            print(f'{e._message}')
            break
        if element.name()[0] == 'V':
            #voltage source stamp

            #the effect of the assumed current flown through the present voltage source
            #on nodal equation at first_node (I_v1 assumed to be flown from negitive termial of battery to positive termianl)
            add_to_dict(nodal_equation_dict,'V('+ element.first_node() + ')' , 'I_' + element.name(), -1)

            #the effect of the assumed current flown through the present voltage source
            # on nodal equation at second_node
            add_to_dict(nodal_equation_dict,'V('+ element.second_node() + ')', 'I_' + element.name(), +1)

            #auxilary equation  v(node1) - v(node2) - value_of_v = 0
            add_to_dict(nodal_equation_dict, 'AUX_' + element.name(),'V('+ element.first_node() + ')', 1)
            add_to_dict(nodal_equation_dict, 'AUX_' + element.name(),'V('+ element.second_node() + ')', -1)
            add_to_dict(nodal_equation_dict, 'AUX_' + element.name(),'CONSTANT', -element.value())

        elif element.name()[0] == 'I' :
            #current source stamp
            #effect of current source on first_node
            add_to_dict(nodal_equation_dict,'V(' + element.first_node() + ')','CONSTANT',-element.value())


            #effect of current source on first_node
            add_to_dict(nodal_equation_dict,'V(' + element.second_node() + ')','CONSTANT',element.value())

no_of_unknowns = len(nodal_equation_dict.keys()) - 1  # aussuming V_GND = 0 hence the number of unknowns is reduces by one
unknowns = unknowns(nodal_equation_dict)  #unkowns are loaded in map and their key is the name of the unknown (ex : V1) and their 
                                          # value is their index at which their coefficients are loaded in matrix

#initilizing empty numpy array of appropriate size to form  A (unkowns) = B
A = np.zeros((len(nodal_equation_dict.keys()),len(nodal_equation_dict.keys())),dtype = complex)
B = np.zeros((len(nodal_equation_dict.keys())),dtype = complex)

#now we have to convert the nodal_equation_dict into a matrix for solving it 
index = -1
for node in nodal_equation_dict.keys():
    index += 1
    if node == 'V(GND)':
        index_gnd = index    #storing index of ground to delete from the matrix as V_gnd = 0
    for unknown in nodal_equation_dict[node].keys():
        if unknown != 'CONSTANT':
            A[index][unknowns[unknown]] += nodal_equation_dict[node][unknown]
        elif unknown == 'CONSTANT':
            B[index] -= nodal_equation_dict[node][unknown]
#now we have to solve A and B matrices

#deleting the nodal equation fromed at GND node and keeping V(GND) as zero
A = np.delete(A , index_gnd , axis = 0)
A = np.delete(A , unknowns['V(GND)'], axis = 1)
B = np.delete(B , index_gnd)
try :
    ans = np.linalg.solve(A,B)   # has inconsistent solution if 2 voltage solutions are connected in a loop
except MyLinalError as e:
    error_flag = 1
    print('{e._message}')
if error_flag == 0 :
    print("The solution of unknown voltages and currents are :")
    left_heading = "Unknowns"
    Right_heading = "Complex form"
    Middle_heading = "Magnitude"
    print ( f'{left_heading : <10} {Middle_heading  :^30}{Right_heading : >50}')
    for unknown in unknowns.keys():
        if(unknown != 'V(GND)') :
            if unknowns[unknown] < unknowns['V(GND)'] :
                print ( f'{unknown : <10} {abs(ans[unknowns[unknown]]) :^30}{ans[unknowns[unknown]] : >50}')
            else :
                print ( f'{unknown : <10} {abs(ans[unknowns[unknown] - 1]) :^30}{ans[unknowns[unknown] - 1] : >50}')



print(ans)
print(unknowns)
