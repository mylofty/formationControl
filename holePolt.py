import numpy as np
import sys
import matplotlib.pyplot as plt
import matplotlib
import pylab as pl
#topo=open("topology.out","r")
oldpoint = open("origin data","r")
oldx =[]
oldy = []
oldstate = []

for line in oldpoint:
    s=line.split()
    oldx.append((float(s[0])))
    oldy.append(float(s[1]))
    oldstate.append((float(s[2])))

for index in range(len(oldx)):
    if(oldstate[index]==3):
        plt.scatter(oldx[index],oldy[index],c='gray',alpha=1,marker='v')
    if(oldstate[index]==2):
        plt.scatter(oldx[index],oldy[index],c='gray',alpha=1)
    if (oldstate[index] == 1):
        plt.scatter(oldx[index], oldy[index], c='gray', alpha=1)
    if (oldstate[index] == 0):
        plt.scatter(oldx[index], oldy[index], c='gray', alpha=1)
hole=open("now data","r")
hx=[]
hy=[]
state = []
N=0
for line in hole:
    s=line.split()
    hx.append((float(s[0])))
    hy.append(float(s[1]))
    state.append((float(s[2])))
    N = N+1;
print(len(hx))
lines = open("line data","r")
for line in lines:
    s = line.split()
    x1 = float(s[0])
    y1 = float(s[1])
    x2 = float(s[2])
    y2 = float(s[3])
    x3 = float(s[4])
    y3 = float(s[5])
    plt.plot([x1,x2],[y1,y2],c='b')
    plt.plot([x1,x3],[y1,y3],c='b')
for index in range(len(hx)):
    if(state[index]==3):
        plt.scatter(hx[index],hy[index],c='red',alpha=1,marker='v')
    if(state[index]==2):
        plt.scatter(hx[index],hy[index],c='red',alpha=1)
    if (state[index] == 1):
        plt.scatter(hx[index], hy[index], c='green', alpha=1)
    if (state[index] == 0):
        plt.scatter(hx[index], hy[index], c='black', alpha=1)
plt.title('Scatter')
plt.xlabel('x')
plt.ylabel('y')
plt.grid(True)
plt.show()
