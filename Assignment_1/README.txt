# Question 1

Dependencies: Pysat,Numpy, Pandas, Pygame(in order to view graphical output of the sudoku).

If 'x' is not installed run the following command to resolve dependency:
$ pip install 'x'


Comment out lines 199-226 of q1 if you wish to avoid the pygame output. 

Ensure that the input to the problem (csv file) is named as input.csv and is in the same folder as q1.py

Run q1.py by :

    
    $ python q1.py 
    Give the value of k in the terminal.
    If a solution for the problem exists it will be saved as out.csv in the same directory, else "None" shall be reported during execution.


Testcases:
 In directory tests/q1/in/ :
 
    Inputs (generated by either q2.py / hand ) are saved in the format sudoku(x)(y).csv 

    (x) denotes the value of k used. If (x) starts with 0, None is expected as an output.
 
 
 In directory tests/q1/out/ :
 
    Outputs (generated by q1.py ) are saved in the format sudoku(x)(y).csv (same as input name) if the solution exists.

    If an output file corresponding to some input doesn't exist, None was reported during execution.
 

Typical Timing Benchmarks:

k=2 : 0.005s
k=3 : 0.05s
k=4 : 0.2 s
k=5 : 1s
k=6 : 4.5s
k=7 : 50 minutes (All Zero input)



# Question 2

Dependencies: Pysat,Numpy, Pandas

If 'x' is not installed run the following command to resolve dependency:
$ pip install 'x'

Run q2.py by :

    
    $ python q2.py 
    Give the value of k in the terminal.
    A solution for the problem will be saved as out.csv in the same directory.


Testcases:

 In directory tests/q2-outputs/ :
 
    Outputs (generated by q2.py ) are saved in the format sudoku(x)-(y).csv

    (x) denotes the value of k used. 

 

Typical Timing Benchmarks:

k=2 : 0.01s
k=3 : 0.09s
k=4 : 0.4s
k=5 : 5s
k=6 : 60s






