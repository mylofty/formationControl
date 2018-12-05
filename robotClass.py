import tensorflow as tf
import numpy as np
import copy
from matplotlib import pyplot as plt


class Robot(object):
    def __init__(self, epoch, lrn):
        self.sess = tf.Session()
        self.coord = tf.Variable(tf.truncated_normal(shape=(2,), mean=5, stddev=1))
        self.forecast_coord = tf.Variable(tf.truncated_normal(shape=(2,), mean=5, stddev=1))
        self.neighbors = tf.placeholder(tf.float32, shape=(None, 2))  # neighbor's coord
        self.dists_gt = tf.placeholder(tf.float32, shape=(None,))

        self.dists_ob = tf.map_fn(lambda x: self.distance(self.coord, x), self.neighbors)

        self.losses = tf.square(tf.square(self.dists_gt)  - tf.square(self.dists_ob))
        self.reduced_loss = tf.reduce_sum(self.losses)

        self.forecast_dists_ob = tf.map_fn(lambda x: self.distance(self.forecast_coord, x), self.neighbors)
        self.forecast_losses = tf.square(tf.square(self.dists_gt) - tf.square(self.forecast_dists_ob))
        self.forecast_reduced_loss = tf.reduce_sum(self.forecast_losses)


        self.epoch = epoch
#        self.optimizer = tf.train.GradientDescentOptimizer(learning_rate=lrn)
        self.optimizer = tf.train.AdamOptimizer(learning_rate=lrn)
        self.forecast_optimizer = tf.train.AdamOptimizer(learning_rate=lrn)
        self.train_op = self.optimizer.minimize(self.reduced_loss)
        self.forecast_train_op = self.forecast_optimizer.minimize(self.forecast_reduced_loss)

        self.sess.run(tf.global_variables_initializer())

        self.loss_dump = []

        self.dic_neighbors = {}
        self.isBeacon = False
        self.isFinalPos = False

        self.parent1 = -1
        self.parent2 = -1
        self.z = -1

        self.centerX = -1
        self.centerY = -1
        self.initX = -1
        self.initY = -1


    def setParents(self, p1, p2):
        self.parent1 = p1
        self.parent2 = p2

    def setBeacon(self, boolean):
        self.isBeacon = boolean

    def distance(self, t1, t2):
        return tf.sqrt(tf.square(t1[0] - t2[0]) + tf.square(t1[1] - t2[1]))

    def run(self, neighbors, dists):
        if(self.isBeacon == True):
            return
        num = len(neighbors)
        nei = []
        dis = []
        indexes = num #np.random.choice(num, num, replace=False)
        for i in range(indexes):
            nei.append(neighbors[i])
            dis.append(dists[i])
        # for key, value in self.dic_neighbors.items():
        #     nei.append(key)
        #     dis.append(value)

        for i in range(self.epoch):
            # if method == 'coord':
            coord, _, loss = self.sess.run([self.coord,
                                            self.train_op,
                                            self.reduced_loss],
                                           feed_dict={
                self.neighbors: nei,
                self.dists_gt: dis
            })
        # print("loss: ", loss)

        self.loss_dump.append(copy.deepcopy(loss))
        # print('loss_dump',self.loss_dump)
        print("loss: ", loss)

    def get_coord(self):
        return self.sess.run(self.coord)

    def set_coord(self,x,y):
        self.sess.run(self.coord.assign([x,y]))

    def get_forecast_coord(self):
        return self.sess.run(self.forecast_coord)

    def set_forecast_coord(self, coord):
        self.sess.run(self.forecast_coord.assign(coord))

    def show_loss_curve(self):
        plt.figure(10)
        print('loss_dump is', self.loss_dump)
        length = len(self.loss_dump)
        print('curve length is ',length)
        plt.annotate(s=round(self.loss_dump[length-1], 2), xy=((length-1)*self.epoch, self.loss_dump[length-1]), xytext=(-5, 5),
                     textcoords='offset points')
        # plt.annotate(s=round(self.loss_dump[length - 2], 2), xy=((length - 2)*self.epoch, self.loss_dump[length - 2]), xytext=(-5, 5),
        #              textcoords='offset points')
        plt.plot(np.arange(0,length,step=1)*self.epoch, self.loss_dump)
        np.savetxt('./loss_dump2.txt',np.array(self.loss_dump))
        plt.show()

    def set_initialPos_centerPos(self, centerPos):
        [self.initX, self.initY] = self.get_coord()
        [self.centerX, self.centerY] = centerPos

    def move(self, time):
        # moving: y = 10*(t/15)**2
        # resx = x+deltaT
        # resy = y + 10*np.sin(2*math.pi*t/40)
        # resy = y + 10 * 2 * x *(1/15)*(1/15)*deltaT
        x0 = time + self.centerX
        y0 = 10 * (time / 15) ** 2 + self.centerY
        slope = 10 * 2 * time * (1 / 15) * (1 / 15)
        angle = np.arctan(slope)
        xp = x0 + (self.initX-self.centerX) * np.cos(angle) - (self.initY - self.centerY) * np.sin(angle)
        yp = y0 + (self.initX-self.centerX) * np.sin(angle) + (self.initY - self.centerY) * np.cos(angle)
        return np.array([xp, yp])


# class Beacon(object):
#     def __init__(self, x, y):
#         self.coord = (x, y)
#
#     def get_coord(self):
#         return self.coord
#
#     def run(self, neighbors, dists):
#         pass
#
#     def show_loss_curve(self):
#         pass
#
#     def set_coord(self,x,y):
#         self.sess.run(self.coord.assign([x,y]))

