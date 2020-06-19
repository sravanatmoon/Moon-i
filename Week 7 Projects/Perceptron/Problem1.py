# Perceptron

import matplotlib.pyplot as plt
import numpy as np


# plot xn, and approximate function with weights learned
def Plot(xn, W):
    x1_p, x1_n = np.empty((0, 2), int), np.empty((0, 2), int)
    for i in range(len(xn)):
        if xn[i][-1] == 1:
            x1_p = np.append(x1_p, [[xn[i][0], xn[i][1]]], axis=0)
        else:
            x1_n = np.append(x1_n, [[xn[i][0], xn[i][1]]], axis=0)
    plt.scatter(x1_p[:, 0], x1_p[:, 1], c='b')  # all +1 points
    plt.scatter(x1_n[:, 0], x1_n[:, 1], c='r')  # all -1 points
    plt.plot([0, -W[0] / W[1]], [-W[0] / W[2], 0])  # line to separate +1/-1 points
    plt.show()


# read the input file and form Matrix [Xi,yi]
def formulate_matrix(file):  # xn will be (n*d) matrix
    xn = []
    with open(file, mode='r') as f:  # The file will be f from now on.
        lines = f.read().splitlines()
        for line in lines:
            xn.append([int(val) for val in line.split(',')])
    return xn


def Perceptron():
    xn, i, W = formulate_matrix('input1.csv'), 0, np.zeros(3)  # W = (w0, w1, w2)
    Not_Done = True
    with open('Output1.csv', mode='w') as f:
        while Not_Done:
            for i in range(len(xn)):  # rand_x = xn[np.random.choice(misclassified_indices)]
                fx, y = np.dot(W, [1, xn[i][0], xn[i][1]]), xn[i][-1]
                if i==(len(xn)-1) and fx * y>0:
                    Not_Done = False
                elif fx * y <= 0:
                    W += np.dot(y, [1, xn[i][0], xn[i][1]] )  # update weight, w <- w + yx
                    f.write(str(W[0]) + ',' + str(W[1]) + ',' + str(W[2]) + '\n')
                    break

    Plot(xn, W)


if __name__ == "__main__":
    Perceptron()
