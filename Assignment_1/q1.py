from pysat.solvers import Glucose4
import numpy as np
import pandas as pd
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame
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
  # gives the solution of the sudoku  pair based on the assumptions = assump
  g.solve(assumptions= assump)
  x= g.get_model()

  if(x==None):
    print("None: No solution found for this pair")
    l=[]
    return l
  
  ans1 = np.zeros((2*k*k,k*k), dtype=np.int_)



  for i  in x:
    if(i<=0):

      continue

    # based on even or odd literals, use inv to set the correct value in the corresponding sudoku

    if(i%2==0):
      i=i//2
      (a,b,c)= inv(i)
      ans1[a][b]= c+1
    else:
      i=i//2
      (a,b,c)= inv(i)
      ans1[k*k+a][b]= c+1
    
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
  print("Solution found,  saving to out.csv")
  
  d1= pd.DataFrame(ans1)
  d1.to_csv('out.csv', header=False, index=False)
  # print(d1)
  return ans1




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
        




assump=[]


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




#  take input 

q=pd.read_csv("./input.csv", header=None).values.tolist()
M=0

for i in range(k**2):
  for j in range(k**2):
    if(q[i][j]==0):
      continue

    assump.append(cnum(i,j,q[i][j]-1))
    
M=1
for i in range(k**2, 2*(k**2)):
  for j in range(k**2):
    if(q[i][j]==0):
      continue

    assump.append(cnum(i-k**2,j,q[i][j]-1))

ans=get_sol(assump) # solve for a solution

if(len(ans)>0):
  print("Starting Pygame..")
  print("Note : It is possible that Pygame visualization may not work correctly due to resolution issues")

  s1=[]
  s2=[]
  # print('hello')
  for i in range(k*k):
    l=[]
    for j in range(k*k):
      l.append(ans[i][j])
    s1.append(l)
  for i in range(k*k):
    l=[]
    for j in range(k*k):
      l.append(ans[k*k+i][j])
    s2.append(l)



  pygame.font.init()
  screen = pygame.display.set_mode((720, 720))
  for j in range(k*k):
      p=j*(720/(k*k))
      pygame.draw.line(screen, (0,0,255),(p,0),(p,720),1)
      pygame.draw.line(screen, (0,0,255),(0,p),(720,p),1)

  font = pygame.font.Font( 'freesansbold.ttf',(140//(k*k)))
  

  for i in range(k*k):
      for j in range(k*k):
          k1=(360/(k*k))+((i*720)/(k*k))-(90/(k*k))
          k11=(360/(k*k))+((i*720)/(k*k))+(90/(k*k))
          k2=(360/(k*k))+((j*720)/(k*k))
          val1 = font.render(str(s1[i][j]), True, (255,255,255), (0,0,0))
          val2= font.render(str(s2[i][j]), True, (0,255,0), (0,0,0))
  

          val1R = val1.get_rect()
          val2R=val2.get_rect()
          val1R.center = (k1,k2)
          val2R.center=(k11,k2)
          screen.blit(val1,val1R)
          screen.blit(val2,val2R)
  pygame.display.update()
  # print('hello')
  running = True
  while running:
      for event in pygame.event.get():
          if event.type == pygame.QUIT:
              running = False

  pygame.quit()
  # pygame.time.delay(15000)



