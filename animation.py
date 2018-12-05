import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import copy

times = 1
distance = 4.1
neighbors = []

# def neighbor(points):

def move(x, y, t):
    # moving: y = x*2
    resx = x+t
    resy = y + t*2


def show(points):
    global times
    fig = plt.figure(times)
    plt.scatter(points[:, 0], points[:, 1], c='r')
    print(points)
    plt.plot(16,16,'bo')
    plt.plot(0, 0, 'bo')
    plotx = []
    ploty = []
    for index in range(len(points)):
        plotx.append(points[index][0])
        ploty.append(points[index][1])
        plt.annotate(s=index, xy=(points[index][0], points[index][1]), xytext=(-5, 5), textcoords='offset points')

    times = times + 1


def anim(list_points):
    fig = plt.figure()
    ax = plt.axes(xlim=(-2, 30), ylim=(-2, 30))
    length = len(list_points)
    new_points = np.array(list_points[0])
    scat = ax.scatter(new_points[:, 0], new_points[:, 1], c='r')

    def update(frame_number):
        global new_points
        new_points = np.array(list_points[frame_number])
        new_points = new_points[:,0:2]
        print('update ', frame_number, list_points[frame_number])
        scat.set_offsets(new_points)
        return scat,

    animate = animation.FuncAnimation(fig, update, frames=length, interval=200, blit=False)  # interval是每隔70毫秒更新一次，可以查看help
    animate.save('basic_animation.mp4', fps=30, extra_args=['-vcodec', 'libx264'])
    plt.show()


points = np.loadtxt('./node.npy')
points = points[0:11, :]
list_points = []
list_points.append(copy.deepcopy(points))
iterator_time = 30
robot_num = len(points)
time = 1
# show(points)
while iterator_time > 0:
    for index in range(robot_num):
        if index == 0 or index == 1 or index == 10:
            points[index][0] = points[index][0] + (np.random.random()-0.5) + 0.5
            points[index][1] = points[index][1] + (np.random.random() - 0.5) + 0.5
    # print('iteraotr_time is ', iterator_time, points)
    list_points.append(copy.deepcopy(points))
    # show(points)
    for index in range(robot_num):
        if index != 0 and index != 1 and index != 10:
            points[index][0] = points[index][0] + (np.random.random()-0.5) + 0.5
            points[index][1] = points[index][1] + (np.random.random() - 0.5) + 0.5
            rand = np.random.randint(0, 3)
            if rand == 0:
                points[index][0] = points[index][0] + (np.random.random() - 0.5)
                points[index][1] = points[index][1] + (np.random.random() - 0.5) * 3
    # print('iteraotr_time is ', iterator_time, points)
    list_points.append(copy.deepcopy(points))
    # show(points)
    iterator_time = iterator_time - 1


anim(list_points)
# print(list_points)
# plt.show()


#
# import numpy as np
# import matplotlib
# import matplotlib.pyplot as plt
# from matplotlib.animation import FuncAnimation
# # from matplotlib import animation
# # No toolbar
# matplotlib.rcParams['toolbar'] = 'None'
# # New figure with white background
# fig = plt.figure(figsize=(6,6), facecolor='white')
# # New axis over the whole figureand a 1:1 aspect ratio
# # ax = fig.add_axes([0,0,1,1], frameon=False, aspect=1)
# ax = fig.add_axes([0.005,0.005,0.990,0.990], frameon=True, aspect=1)
# # Number of ring
# n = 50
# size_min = 50
# size_max = 50*50
# # Ring position ，圆环位置，范围在[0,1]之间
# P = np.random.uniform(0,1,(n,2))
# # Ring colors环的颜色
# C = np.ones((n,4)) * (0,1,0,1)
# #C = np.ones((n,3)) * (1,0,1)
# # Alpha color channel goes from 0 (transparent) to 1 (opaque)
# # 透明度，数值在[0,1]之间
# C[:,2] = np.linspace(0,1,n)
# # Ring sizes环的大小，范围在[50,2500]
# S = np.linspace(size_min, size_max, n)
# # Scatter plot
# # 散点图绘制
# scat = ax.scatter(P[:,0], P[:,1], s=S, lw = 0.5,
#          edgecolors = C, facecolors='None')
# # Ensure limits are [0,1] and remove ticks
# #保证x,y的范围在[0,1]之间,移除坐标轴标记
# ax.set_xlim(0,1), ax.set_xticks([])
# ax.set_ylim(0,1), ax.set_yticks([])
# def update(frame):
#   global P, C, S
#   # Every ring is made more transparent每个环变得更透明
#   C[:,3] = np.maximum(0, C[:,3] - 1.0/n)
#   # Each ring is made larger每个环都比原来的大
#   S += (size_max - size_min) / n
#   # Reset ring specific ring (relative to frame number)
#   i = frame % 50
#   P[i] = np.random.uniform(0,1,2) # P[i] = P[i,:],同时改变了x,y两个位置的值
#   S[i] = size_min #从最小的形状开始
#   C[i,3] = 1   #设置透明度为1
#   # Update scatter object
#   # 更新scatter绘图对象的属性，例如edgecolors,sizes,offsets等
#   scat.set_edgecolors(C) #设置边缘颜色
#   scat.set_sizes(S)    #设置大小
#   scat.set_offsets(P)   #设置偏置
#   print('update ',frame)
#   return scat,
# animate = FuncAnimation(fig, update, frames = 300,interval=70)#interval是每隔70毫秒更新一次，可以查看help
# # FFwriter = animation.FFMpegWriter(fps=20)  #frame per second帧每秒
# # animate.save('rain.mp4', writer=FFwriter,dpi=360)#设置分辨率
# plt.show()