import math
import sys
from copy import deepcopy
from statistics import stdev, mean

from matplotlib import pyplot as plt
import numpy as np

n = 79  # m-iterations


def formulate_matrix(file):  # xn will be (n*d) matrix
    Data = np.empty((0, 3), float)
    with open(file, mode='r') as f:  # The file will be f from now on.
        lines = f.read().splitlines()
        for line in lines:
            Data = np.append(Data, [[float(val) for val in line.split(',')]], axis=0)
        features, Y = Data[:, 0:2], deepcopy(Data[:, 2])
        Data[:, 2] = Data[:, 2] / Data[:, 2]
        features = Data[:, 0:3]
        features[:, [0, 2]] = features[:, [2, 0]]
    for i in [1, 2]:
        features[:, i] = (features[:, i]) / stdev(features[:, i])
    return features, Y


def RSS(fx, Y):  # residual sum of squares
    R = 0
    for i in range(n - 1):
        R += (1 / (2 * n)) * ((fx[i] - Y[i]) ** 2)
    return R


def update_betas(α, β, X, fx, Y):
    for j in range(len(β)):
        for i in range(n):
            β[j] += (α / n) * (X[i][j] * (fx[i] - Y[i]))
    return β


def showGraph(data, heights, weights):
    from matplotlib import pyplot
    import pylab
    from mpl_toolkits.mplot3d import Axes3D

    fig = pylab.figure()
    ax = Axes3D(fig)
    xs = data[:, [1]].flatten()
    ys = data[:, [2]].flatten()
    zs = heights
    ax.scatter(xs, ys, zs)
    w = weights
    # xx = np.linspace(min(xs), max(xs))
    # a = -w[1] / w[2]
    # yy = a * xx - (w[0]) / w[2]
    # plt.plot(xx, yy, 'k-')

    xx, yy = np.meshgrid(np.arange(min(xs), max(xs)), np.arange(min(ys), max(ys)))

    # calculate corresponding z
    z = (-w[1] * xx - w[2] * yy - w[0]) * 1. / w[2]

    plt3d = fig.gca(projection='3d')
    plt3d.plot_surface(xx, yy, z)

    pyplot.show()


def Regression():
    X, Y = formulate_matrix('input2.csv')

    with open('Output2.csv', mode='w') as f:
        for α in [0.01*i for i in range(100)]:# [0.001, 0.005, 0.01, 0.05, 0.1, 0.5, 1, 5, 10, 0.0002]:
            β = np.ones(3)
            R, Rp, itr = -math.inf, 0, 0
            m = 1000 if α == 0.0002 else 100
            while abs(Rp - R) >= 0.0001:
                fx = np.zeros(1)
                for i in range(len(X)):
                    fxi = np.dot(β, X[i])
                    fx = np.append(fx, [fxi], axis=0)
                Rp = deepcopy(R)
                R, β = RSS(fx, Y), update_betas(α, β, X, Y, fx)
                itr +=1
            f.write(f'a :{α}' + ',' + f'Iterations: {itr} : ' + str(β[0]) + ',' + str(β[1]) + ',' + str(β[2]) + ',' + str(
                R) + '\n')
            # showGraph(X, Y, β)


if __name__ == "__main__":
    Regression()
