import numpy as np
import random
import matplotlib.pyplot as plt

def create_map(nodeNum, mapSize):
    random.seed(15)
    lx = list(range(mapSize* 10))
    ly = list(range(mapSize* 10))
    random.shuffle(lx)
    random.shuffle(ly)
    lx = lx[0: nodeNum]
    ly = ly[0: nodeNum]
    arr = np.append(np.divide(lx, 10), np.divide(ly, 10)).reshape((nodeNum, 2))
    lz = [0 for i in range(nodeNum)]
    arr= np.column_stack((arr, lz))
    plt.scatter(arr[:, 0], arr[:, 1], c='b')
    np.savetxt('node2.npy', arr)
    for i in range(nodeNum):
        plt.annotate(s=i, xy=(arr[i, 0], arr[i, 1]), xytext=(-5, 5), textcoords='offset points')
    plt.show()


if __name__ == '__main__':
    # create_map(80, 50)
    old = np.loadtxt('node2.npy')
    new = np.loadtxt('forecast_position.npy')
    plt.title('nodes\' number is 80\n global ')
    plt.scatter(old[:, 0], old[:, 1], c='b')
    plt.scatter(new[:, 0], new[:, 1], c='r')
    for i in range(len(new)):
        plt.annotate(s=i, xy=(old[i, 0], old[i, 1]), xytext=(-5, 5), textcoords='offset points')
        plt.annotate(s=i, xy=(new[i, 0], new[i, 1]), xytext=(-5, 5), textcoords='offset points')
    plt.show()