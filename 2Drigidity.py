import numpy as np

from RobotImpl.triangle_extension import triangle_extension

nodes = np.loadtxt('./node.npy')

RobotNum = len(nodes)
MapSize = 10
Distance = 4.1

Beacon1ID = 1
Beacon2ID = 2
Beacon3ID = 15

# beacons = []
# for i, r in enumerate(nodes):
# 	if r[3]==3 :
# 		beacons.append(i)
# Beacon1ID = beacons[0]
# Beacon2ID = beacons[1]
# Beacon3ID = beacons[2]

class Robot(object):

	def __init__(self):
		self.id = 0
		self.receivedMsg = False
		self.state = 0

		self.locationx = 0
		self.locationy = 0
		self.locationz = 0

		self.parent1 = -1
		self.parent2 = -1
		self.root1 = -1
		self.root2 = -1
		self.extra = -1

		self.root1x = 0
		self.root1y = 0
		self.root1z = 0


		self.root2x = 0
		self.root2y = 0
		self.root2z = 0

		self.parent1x = 0
		self.parent1y = 0
		self.parent1z = 0

		self.parent2x = 0
		self.parent2y = 0
		self.parent2z = 0

		self.myNeighbor = []
		self.query1 = -1
		self.query2 = -1

	def triangle_extension(self, probot):
		triangle_extension(self, probot)


def read3array(pointX, pointY, pointZ):
	
	for i, point in enumerate(nodes):
		pointX[i] = point[0]
		pointY[i] = point[1]
		pointZ[i] = point[2]

	pass

def cmp_by_value(lhs):
	return lhs[1]

def createMap(probot):
	pointX = [0 for i in range(RobotNum)]
	pointY = [0 for i in range(RobotNum)]
	pointZ = [0 for i in range(RobotNum)]

	read3array(pointX, pointY, pointZ)

	for i, r in enumerate(probot):
		r.id = i
		r.locationx = pointX[i]
		r.locationy = pointY[i]
		r.locationz = pointZ[i]

		print("Robot%d Position is (%d, %d, %d)"%(r.id, r.locationx, r.locationy, r.locationz))

	for i in range(RobotNum):
		for j in range(i+1,RobotNum):
			tempDistance = np.sqrt( (probot[i].locationx-probot[j].locationx)**2 + (probot[i].locationy-probot[j].locationy)**2 +
				(probot[i].locationz-probot[j].locationz)**2 )
			if(tempDistance<Distance):
				probot[i].myNeighbor.append( [j, tempDistance] )
				probot[j].myNeighbor.append( [i, tempDistance] )

	for r in probot:
		r.myNeighbor = sorted(r.myNeighbor, key=cmp_by_value)

	for r in probot:
		s = ""
		for t in r.myNeighbor:
			s = s + "%d "%t[0]
		print("Robot%d have neighbor %s"%(r.id, s))


	pass

def main():
	probot = [Robot() for i in range(RobotNum)]

	createMap(probot)

	probot[Beacon1ID].state = 3
	probot[Beacon2ID].state = 3
	probot[Beacon3ID].state = 3

	probot[Beacon1ID].root1 = probot[Beacon1ID].root2 = Beacon1ID
	probot[Beacon2ID].root1 = probot[Beacon2ID].root2 = Beacon2ID
	probot[Beacon3ID].root1 = probot[Beacon3ID].root2 = Beacon3ID

	flexiblecount = 0
	localization = 0
	rigidnum = 0
	flag0 = True

	with open("origin data", "w") as out1 :
		for r in probot:
			out1.write("%d %d %d %d\n"%(r.locationx, r.locationy, r.locationz, r.state))

		pass

	count = 30
	for count_ in range(count):

		for i, r in enumerate(probot):
			print("this is robot %d"%i)

			r.triangle_extension(probot)



			for i in range(RobotNum):
				if probot[i].state==0:
					flexiblecount +=1
			print("flexible robot have %d"%flexiblecount)
			flexiblecount = 0

			for i in range(RobotNum) :
				if probot[i].state==2:
					localization += 1

			print("localization robot have %d"%localization)
			localization = 0

			for i in range(RobotNum):
				if probot[i].state==1:
					rigidnum += 1

			print("rigid robot have %d"%rigidnum)
			rigidnum = 0

	with open("now data","w") as out2, open("line data","w") as out3 :
		for r in probot :
			out2.write("%d %d %d %d\n"%(r.locationx, r.locationy, r.locationz, r.state))

			if r.parent1!=-1 :
				out3.write("%d %d %d %d %d %d %d %d %d\n"%(
					r.locationx, r.locationy, r.locationz,
					r.parent1x, r.parent1y, r.parent1z,
					r.parent2x, r.parent2y, r.parent2z))

		pass

	pass


if __name__ == "__main__":
	main()