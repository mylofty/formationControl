from sympy import symbol, solve
import numpy as np

def distance(p1, p2):
    return np.sqrt(np.sum(np.square(p1-p2)))

def measure(coord, n1coord, n2coord):
	mcoord = np.array(coord)

	inc = np.random.randint(-10, 10)
	print(inc)

	mcoord[2] = mcoord[2]+inc

	return distance(coord, n1coord), distance(coord, n2coord), distance(mcoord, n1coord), distance(mcoord, n2coord)

def solve_distance(p1, p2):
	return ((p1[0]-p2[0])**2+(p1[1]-p2[1])**2+(p1[2]-p2[2])**2)**0.5

# nei1 = np.array([0, 2, 6])
# nei2 = np.array([-2, 2, 7])
# p = np.array([5, 1, 9])

nei1 = np.array([1, 1, 0])
nei2 = np.array([10, 10, 0])
p = np.array([5, 1, 3])

x = symbol.Symbol('x')
y = symbol.Symbol('y')
z = symbol.Symbol('z')
t = symbol.Symbol('t')

d = measure(p, nei1, nei2)
print(d)
print(d[2]**2-d[0]**2, d[3]**2-d[1]**2)

# sol = solve([
# 	solve_distance([x, y, z], nei1)-d[0],
# 	solve_distance([x, y, z], nei2)-d[1],
# 	solve_distance([x, y, z-2], nei1)-d[2],
# 	# solve_distance([x, y, z-t], nei2)-d[3]
# 	], [x, y, z], dict=False)

sol = solve([
	2*z*t+(t-0)**2-0**2-d[2]**2+d[0]**2,
	2*z*t+(t-0)**2-0**2-d[3]**2+d[1]**2,
	], [z, t], dict=False)

print(sol)