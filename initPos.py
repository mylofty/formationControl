from scipy.optimize import fsolve
import numpy as np
from math import *

Beacon1 = 77
Beacon2 = 46
Beacon3 = 1
Distance = 15


class Robot:
    def __init__(self):
        self.posx = -1
        self.posy = -1
        self.isBeacon = False
        self.myNeighbor = []
        self.dv_distance = []


def main():
    points = np.loadtxt('./node2.npy', dtype=np.float32)
    node_num = len(points)
    robot = [Robot() for i in range(node_num)]
    robot[Beacon1].isBeacon = True
    robot[Beacon2].isBeacon = True
    robot[Beacon3].isBeacon = True
    for index in range(node_num):
        robot[index].posx = points[index, 0]
        robot[index].posy = points[index, 1]
        robot[index].dv_distance = [0] * node_num

    # initial myNeighbor
    for i in range(node_num):
        for j in range(i + 1, node_num):
            tempDistance = np.sqrt(
                (robot[i].posx - robot[j].posx) ** 2 + (robot[i].posy - robot[j].posy) ** 2)

            if (tempDistance < Distance):
                robot[i].myNeighbor.append([j, tempDistance])
                robot[j].myNeighbor.append([i, tempDistance])
    # initial dv_distance
    for i in range(node_num):
        for j in range(node_num):
            robot[i].dv_distance[j] = 999
            if i == j:
                robot[i].dv_distance[j] = 0
    for i in range(node_num):
        for j in range(len(robot[i].myNeighbor)):
            nei_id = robot[i].myNeighbor[j][0]
            nei_distance = robot[i].myNeighbor[j][1]
            print('nei_distance', i, nei_id, nei_distance)
            robot[i].dv_distance[nei_id] = nei_distance

    # dv_distance
    for i in range(node_num):
        for j in range(node_num):
            for k in range(node_num):
                if robot[j].dv_distance[k] > robot[j].dv_distance[i] + robot[i].dv_distance[k]:
                    robot[j].dv_distance[k] = robot[j].dv_distance[i] + robot[i].dv_distance[k]

    # print dv_distance
    for i in range(node_num):
        for j in range(node_num):
            print('%.3f' % robot[i].dv_distance[j], end='   ')
        print()
    coordlist = []
    for index in range(node_num):
        if index == Beacon1 or index == Beacon2 or index == Beacon3:
            coordlist.append([robot[index].posx, robot[index].posy])
        else:
            dis1 = robot[index].dv_distance[Beacon1]
            b1x = robot[Beacon1].posx
            b1y = robot[Beacon1].posy
            dis2 = robot[index].dv_distance[Beacon2]
            b2x = robot[Beacon2].posx
            b2y = robot[Beacon2].posy
            dis3 = robot[index].dv_distance[Beacon3]
            b3x = robot[Beacon3].posx
            b3y = robot[Beacon3].posy

            if dis1 > 900 or dis2 > 900 or dis3 > 900:
                print('node %d can not connect with beacon' % index)

            def function(r):
                x = r[0]
                y = r[1]
                return [
                    2 * (b1x - b2x) * x + 2 * (b1y - b2y) * y - dis2 ** 2 + dis1 ** 2 +
                    b2x ** 2 - b1x ** 2 + b2y ** 2 - b1y ** 2,
                    2 * (b1x - b3x) * x + 2 * (b1y - b3y) * y - dis3 ** 2 + dis1 ** 2 +
                    b3x ** 2 - b1x ** 2 + b3y ** 2 - b1y ** 2
                ]
            if index == 0:
                print('distance with beacon1, beacon2, beacon3: ',dis1, dis2, dis3)
            sol = fsolve(function, np.array([1, 1]), xtol=1e-5)
            coordlist.append(sol)
            print('sol', index, sol)
    print(coordlist)
    np.savetxt('./dv_distance.npy', coordlist)


if __name__ == '__main__':
    main()