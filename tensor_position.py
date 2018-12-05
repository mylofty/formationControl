import tensorflow as tf
import numpy as np
import random

from matplotlib import pyplot as plt

from robotClass import *
from function1 import *
import copy

deltaT = 0.8  # time increase ratio
time = 0  # time increase


def move2(coordinate):
    x, y = coordinate
    # moving curve y = 10*(t/15)**2
    x = x + deltaT
    y = y + 10 * 2 * time * (1/15)*(1/15)*deltaT
    # y = y + 2
    return x, y


def main():
    global time
    points = np.loadtxt('./node2.npy')
    robot_num = points.shape[0]
    robots = [Robot(epoch=50, lrn=0.02) for x in range(robot_num)]
    listPoints = []
    listPoints.append(copy.deepcopy(points))
    # robots[0].setBeacon(True)
    # robots[1].setBeacon(True)
    # robots[16].setBeacon(True)
    robots[28].setBeacon(True)
    robots[8].setBeacon(True)
    robots[10].setBeacon(True)
    setInitial(robots)

    neighbors, dists = set_2Ddistance_parents_z(robots, points)
    localization_ontime(points, robots, neighbors, dists, 50)
    forecast_position = []
    for index in range(robot_num):
        forecast_position.append(robots[index].get_coord())
    np.savetxt('forecast_position.npy', forecast_position)
    # for index in range(robot_num):
    #     robots[index].set_initialPos_centerPos([6, 6])
    # old_neighbors, old_dists = set_2Ddistance_parents_z(robots, points)
    # iterator_time = 20
    # while iterator_time > 0:
    #     oldpoints = copy.deepcopy(points)
    #
    #     # move beacon
    #     for index in range(robot_num):
    #         if (True == robots[index].isBeacon):
    #             [points[index][0], points[index][1]] = robots[index].move(time)\
    #                                                  + (np.random.random()-0.5)*0.3
    #             robots[index].isBeacon = False
    #         else:
    #             [points[index][0], points[index][1]] = robots[index].get_coord()
    #             # points[index][2] = robots[index].z
    #             robots[index].isBeacon = True
    #     neighbors, dists = set_2Ddistance_parents_z(robots, points)
    #     localization_ontime(robots, neighbors, dists, 100)
    #
    #     show(points, robots)
    #     listPoints.append(copy.deepcopy(points))
    #     for index in range(robot_num):
    #         robots[index].isBeacon = not robots[index].isBeacon
    #
    #     #  calculate forecast non-beacon coordinate
    #     # forecast_coordinate(robots, old_neighbors, old_dists, epochs=200)
    #     #  moving non-beacon
    #     for index in range(robot_num):
    #         if((robots[index].isBeacon !=True)):
    #             # [points[index][0],points[index][1]] = robots[index].get_forecast_coord() + (np.random.random()-0.5)*0.5
    #             [points[index][0], points[index][1]] = robots[index].move(time) + (
    #                         np.random.random() - 0.5) * 0.3
    #         else:
    #             [points[index][0], points[index][1]] = robots[index].get_coord()
    #
    #
    #     neighbors, dists = set_2Ddistance_parents_z(robots, points)
    #     localization_ontime(robots, neighbors, dists, 100)
    #     show(points, robots)
    #     listPoints.append(copy.deepcopy(points))
    #
    #     iterator_time = iterator_time - 1
    #     time = time + deltaT

    # anim(listPoints)
    plt.show()


if __name__ == "__main__":
    main()
