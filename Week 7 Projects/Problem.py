import matplotlib.pyplot as plt
import numpy as np

# plot xn, and approximate function with weights learned
def Plot(xn, weights):
    x1_p, x1_n = np.empty((0, 2), int), np.empty((0, 2), int)
    for i in range(len(xn)):
        if xn[i][-1] == 1:
            x1_p = np.append(x1_p, [[xn[i][0], xn[i][1]]], axis=0)
        else:
            x1_n = np.append(x1_n, [[xn[i][0], xn[i][1]]], axis=0)
    plt.scatter(x1_p[:, 0], x1_p[:, 1], c='b')  # all +1 points
    plt.scatter(x1_n[:, 0], x1_n[:, 1], c='r')  # all -1 points
    plt.plot([0, -weights[0] / weights[2]], [-weights[0] / weights[1], 0])  # line to separate +1/-1 points
    plt.show()

# read the input file and form Matrix [Xi,yi]
def formulate_matrix(file):  # xn will be (n*d) matrix
    xn = []
    with open(file, mode='r') as f:  # The file will be f from now on.
        lines = f.read().splitlines()
        for line in lines:
            xn.append([int(val) for val in line.split(',')])
    return xn


def main():
    xn, i,weights = formulate_matrix('input.csv'),0, np.zeros(3)# (w0, w1, w2)

    with open('output.csv', mode='w') as f:
        while i < (len(xn) - 1):
            for i in range(len(xn)):  # rand_x = xn[np.random.choice(misclassified_indices)]
                fx, y = np.dot(weights, [1, xn[i][0], xn[i][1]]), xn[i][-1]
                if fx * y <= 0:
                    weights += np.dot(y, [1, xn[i][0], xn[i][1]], )  # update weight, w <- w + yx
                    f.write(str(weights[0]) + ',' + str(weights[1]) + ',' + str(weights[2])+'\n')
                    break

    Plot(xn, weights)


if __name__ == "__main__":
    main()
