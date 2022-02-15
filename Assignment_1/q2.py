from pysat.solvers import Glucose4
import numpy as np
import pandas as pd
g = Glucose4()

k=int(input())


M=0 


def cnum (a,b,c): # a,b are the coordinates of the cell, c is the value, cnum returns a unique id for this tuple
  return 2*((a*(k**4) + b*(k**2) +c+1))+M
  # M denotes the mode of sudoku ie Sudoku 1 or 2



def inv (i): #inv is the inverse of cnum
    if(i<=0):
      return
    c= (i-1 )%(k**2)
    b= (((i-1-c)%(k**4)))//(k**2)
    a=((i-1-c-b*k))//(k**4)
    a= int(a)
    return (a,b,c)





def get_sol(assump):
  # returns 2 numpy arrays,  the solution of the sudoku  pair based on the assumptions = assump
  g.solve(assumptions= assump)
  model= g.get_model()

  if(model==None):
    print("None: No solution found for this pair")
  
    return None,None
  
  ans1 = np.zeros((k*k,k*k), dtype=np.int_)
  ans2 = np.zeros((k*k,k*k), dtype=np.int_)


  for i  in model:
    if(i<=0):

      continue

    # based on even or odd id of literals, use inv to set the correct value in the corresponding sudoku

    if(i%2==0):
      i=i//2
      (a,b,c)= inv(i)
      ans1[a][b]= c+1
    else:
      i=i//2
      (a,b,c)= inv(i)
      ans2[a][b]= c+1
    
  # Uncomment to print this sol
  # for x in range (k**2):
  #   for y in range (k**2):
  #     print(int(ans1[x][y]), end=' ')
  #   print()
  # print()
  # for x in range (k**2):
  #   for y in range (k**2):
  #     print(int(ans2[x][y]), end=' ')
  #   print()
  # print()
  # 
  return ans1, ans2




def unq (x):
  #  takes a list of literals and ensures that only at max one of the literals in the list is true 
  for i in x:
    for j in x:
      if(i<=j):
        continue
      g.add_clause([-i, -j])





def make_sudoku():
  # adds clauses for one individual sudoku

  for i in range(k**2):
    for j in range(k**2):
      x = []
      for value in range(k**2):
        x.append(cnum(i,j,value))
      #  x has literals for all values corresponding to i,j cell

      g.add_clause(x) # atleast one is true
      unq(x)  # atmax one is true

  
  
  # no value is repeated in the kxk block and all values are used
  for value in range (k**2):
    for z in range (k):
      for y in range (k):
        x=[]
        for i in range (z*k , z*k +k):
            for j in range (y*k , y*k +k):
              x.append(cnum(i,j,value))
        unq(x)
        g.add_clause(x)



  # no value is repeated in any row or column and all the values are used

  for value in range (k**2):
    for j in range (k**2):
      x=[]
      y=[]
      for i in range (k**2):
        x.append(cnum(i,j,value))
        y.append(cnum(j,i,value))
        
      unq(x)
      unq(y)
      g.add_clause(x)
      g.add_clause(y)
        





# --------------------Was almost Same as Q1 till here-------------------------#



assump=[]

random_row= np.random.permutation(range(0,k*k))
#  to introduce randomness, set one row of suduko to a random permutation
M= 0 

for cell in range (k*k):
  assump.append (int(cnum(int(0),int(cell),int(random_row[cell]))))

M=0 #make 1st
make_sudoku()
M=1 #make 2nd
make_sudoku()






# 2 sudokus shouldnt have any common cell
for c in range(k**2):
  for i in range (k**2):
    for j in range (k**2):
      M=1
      g.add_clause([-cnum(i,j,c), -cnum(i,j,c)+1])


sol1,sol2= get_sol(assump) # solve for a solution

assump=[]


for x in range (k**2):
  for y in range (k**2):
    M=0
    assump.append (int((cnum(x,y,sol1[x][y]-1))))
    M=1
    assump.append (int((cnum(x,y,sol2[x][y]-1))))

assump_un=[]

for x in assump :
  assump_un.append(-x)
# assump_un contains negations of all the current cells.
# used to detect if some other solution to the sudoku is possible

conf =[]
# would contain the final configration


g.add_clause(assump_un)
#  g now is used as a unique solution tester, g.solve(assumptions=assump) returns true if more than one sol is possible. 


while(len(assump)):

  x= assump.pop()
  if(g.solve(assumptions=assump)):
    # x was essential for unique sol
    g.add_clause ([x])
    conf.append(x)


    
def gen(conf):
  # returns the final sudokus
  
  ans1 = np.zeros((2*k*k,k*k), dtype=np.int_)
#   ans2 = np.zeros((k*k,k*k), dtype=np.int_)

  for i  in conf:
    if(i<=0):

      continue
    if(i%2==0):
      i=i//2
      (a,b,c)= inv(i)
      ans1[a][b]= c+1
    else:
      i=i//2
      (a,b,c)= inv(i)
      ans1[k*k+a][b]= c+1

  # similar to get_sol()
    
  d1= pd.DataFrame(ans1)
  d1.to_csv('out.csv', header=False, index=False)
  
print("Sudokus generated, Saving to out.csv")
gen(conf)

