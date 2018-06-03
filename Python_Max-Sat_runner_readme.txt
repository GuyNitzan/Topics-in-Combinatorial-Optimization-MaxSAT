################################################################################
################################################################################
#####################   Python_Max-Sat_runner_readme   #########################
################################################################################
################################################################################



1. In order to run the code use python 3 and above. The file to run is algorithms.py

2. The file utils.py consists of code regarding the algorithms and all of the classes built for this code. It must be in the same folder as the algorithms.py file.
There is no need to update utils.py file in any way.

3. Consult the Max-SAT Problem Algorithms Survey and Testing for "Topics in Combinatorial Optimization" paper to undersatand for each algorithm number, what algorithm does it run.

4. In lines 1-5 in the algorithms.py file, program variables are decided.
Default settings are:
NUM_OF_DIFFERENT_CNFS = 25  # Number of iteration to run the algorithm. answer will be average on all
NUM_OF_CLAUSES = 1000  # Number of clauses in each CNF
MIN_NUM_LITS_PER_CLAUSE = 3  # minimum number of literals per clause - minimum optional is 2
MAX_NUM_LITS_PER_CLAUSE = 3  # maximum number of literals per claus
NUM_OF_VARS = 100

This example translates into
Number of variables: 100
Number of clauses: 540
Number of literals per clause: 3 (3-CNF problem)
Number of iterations of the algorithm in order to 'clean'/avoid irregular results: 25

5. In line 68, assign the "assignment" variable with the return value of the wanted algorithm. Default value: Algorithm 1.
Note: some algorithms recieves a cnf as a variable - main function generates a random one for the user with the name "my_cnf"
For example - To run algorithm 1 we run the line: assignment = algorithm_1()
To run algorithm 2 we run the line: assignment = algorithm_2(my_cnf)

6. Lines 71-72 are optional and run one of two local searchs algorithm. For more information adress the survey paper.

7. Lines 76-85 are printing the results. they are obviously optional and can be updated according to user needs.

8. Default printings are a suggestion only and can be changed or ignored. in the dfault setting, the printing of the running algorithm number 
and program vars are commented out for aesthetic reasons. it can easily be changed.

################################################################################
################################################################################
#####################   Python_Max-Sat_runner_readme   #########################
################################################################################
################################################################################
