import tensorflow as tf
import numpy as np

from matplotlib import pyplot as plt
from scipy.optimize import fsolve
from sympy import symbol, solve

min_distance = 4.5

beacon_id = [0, 1, 16]

def distance(p1, p2):
    return np.sqrt(np.sum(np.square(p1-p2)))

def solve_distance(p1, p2):
	return ((p1[0]-p2[0])**2+(p1[1]-p2[1])**2+(p1[2]-p2[2])**2)**0.5

def set_neighbors(points, robots):
    robot_num = len(robots)
    neighbors = [0 for x in range(robot_num)]
    dists = [0 for x in range(robot_num)]
    for i in range(robot_num):
        neighbors[i] = []
        dists[i] = []
        for j in range(robot_num):
            dis = distance(points[i], points[j])
            if (dis < min_distance and i != j):
                neighbors[i].append(j)
                dists[i].append(dis)
                robots[i].dic_neighbors[j] = dis
    # for i in range(robot_num):
    #     dists[i] = []
    #     for j in neighbors[i]:
    #         dists[i].append(distance(points[i], points[j]))
    return neighbors, dists

points = np.loadtxt('./node.npy')

def measure(robot_id, nei1, nei2):
	coord = np.array(points[robot_id])
	mcoord = np.array(points[robot_id])
	mcoord[2] -= 2

	n1coord = points[nei1]
	n2coord = points[nei2]

	return distance(coord, n1coord), distance(coord, n2coord), distance(mcoord, n1coord), distance(mcoord, n2coord)

class Robot(object):
    def __init__(self, id):

        self.dic_neighbors = {}
        self.isBeacon = False

        self.x = None
        self.y = None

        self.z = None

        self.id = id

        self.dic_2Ddistance = {}

    def setBeacon(self, boolean, coord):
        self.isBeacon = boolean
        self.x, self.y, self.z = coord

    def get_coord(self):
    	return self.x, self.y, self.z

    def cal_2Ddistance(self, robots):
    	for nei in self.dic_neighbors:
    		_3Ddistance = self.dic_neighbors[nei]
    		# print(_3Ddistance, self.z)
    		self.dic_2Ddistance[nei] = (_3Ddistance**2-(self.z-robots[nei].z)**2)**0.5

    def run(self, robots):
        if(self.isBeacon == True):
            return

        if(self.z):
        	return

        for nei1 in self.dic_neighbors:
        	for nei2 in self.dic_neighbors:
        		if nei1!=nei2 and robots[nei1].z!=None and robots[nei2].z!=None:


        			print("index: ", self.id)
        			print("Nei1: ", nei1, "Nei2: ", nei2)

        			# print("Nei1 coord: ", robots[nei1].get_coord())
        			# print("Nei2 coord: ", robots[nei2].get_coord())


        			d1, d2, d3, d4 = measure(self.id, nei1, nei2)
        			# # print(d1, d2, d3, d4)
        			
        			# self.x, self.y, self.z = np.random.normal(loc=5, scale=5, size=(3, ))
        			# # self.x = self.y = self.z = 1
        			# def solve_dis(para):
        			# 	mpara = np.copy(para)
        			# 	mpara[2] -= 2
        			# 	return [
        			# 		distance(para, robots[nei1].get_coord())-d1,
        			# 		distance(para, robots[nei2].get_coord())-d2,
        			# 		distance(mpara, robots[nei1].get_coord())-d3,
        			# 	]

        			# sol = np.real(fsolve(solve_dis, np.array([self.x, self.y, self.z]), xtol=1e-6))

        			# self.x, self.y, self.z = sol

        			t = -2
        			x1 = robots[nei1].x
        			y1 = robots[nei1].y
        			z1 = robots[nei1].z

        			x2 = robots[nei2].x
        			y2 = robots[nei2].y
        			z2 = robots[nei2].z


        			self.z = (d3**2-d1**2+2*z1*t-t**2)/(2*t)

        			x = symbol.Symbol('x')
        			y = symbol.Symbol('y')
        			# z = symbol.Symbol('z')
        			# t = symbol.Symbol('t')


        			sol = solve([
        				solve_distance([x, y, self.z], robots[nei1].get_coord())-d1,
        				2*(x1-x2)*x+x2**2-x1**2 + 2*(y1-y2)*y+y2**2-y1**2 + 2*(z1-z2)*self.z+z2**-z1**2 -d2**2+d1**2
        				# solve_distance([x, y, self.z], robots[nei2].get_coord())-d2,
        				# solve_distance([x, y, z-2], robots[nei1].get_coord())-d3,
        				# solve_distance([x, y, z-2], robots[nei2].get_coord())-d4,
        				], [x, y], dict=False)

        			self.x, self.y = sol[0]

        			# # print(sol)

        			# self.x, self.y, self.z = sol[0]
        			# print("t: ", t)

        			# for s in sol:
        			# 	self.x, self.y, self.z, t = s
        			# 	print(t)



        			return






def main():

	robot_num = points.shape[0]
	robots = [Robot(x) for x in range(robot_num)]

	for i in beacon_id:
		robots[i].setBeacon(True, points[i])

	set_neighbors(points, robots)

	for ep in range(20):
		for i in range(robot_num):
			robots[i].run(robots)

	loss = 0
	for i in range(robot_num):
		loss += np.square(robots[i].z-points[i][2])
		print(robots[i].z, " versus ", points[i][2])

	print("loss: ", loss)


	for i in range(robot_num):
		robots[i].cal_2Ddistance(robots)

		# print(robots[i].dic_2Ddistance)


if __name__ == "__main__":
	main()


