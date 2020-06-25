import sys

import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import GridSearchCV, train_test_split
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier as RFC
from sklearn.linear_model import LogisticRegression as lr
from sklearn.neighbors import KNeighborsClassifier as KNN
from sklearn.tree import DecisionTreeClassifier as DTC


def formulate_data(file):
    Data = np.loadtxt(file, delimiter=',')
    x_train, x_test, y_train, y_test = train_test_split(Data[:, [0, 1]], Data[:, [2]].flatten(),
                                                        test_size=0.4, random_state=42)
    return x_train, x_test, y_train, y_test


def showGraph(test_data, test_labels, clf):
    # import some data to play with
    X = test_data[:, :2]  # we only take the first two features. We could
    # avoid this ugly slicing by using a two-dim dataset
    y = test_labels

    h = .02  # step size in the mesh

    # create a mesh to plot in
    x_min, x_max = X[:, 0].min() - 1, X[:, 0].max() + 1
    y_min, y_max = X[:, 1].min() - 1, X[:, 1].max() + 1
    xx, yy = np.meshgrid(np.arange(x_min, x_max, h),
                         np.arange(y_min, y_max, h))

    # plt.subplot(2, 2, 1)
    # plt.subplots_adjust(wspace=0.4, hspace=0.4)
    Z = clf.predict(np.c_[xx.ravel(), yy.ravel()])

    # Put the result into a color plot
    Z = Z.reshape(xx.shape)
    plt.contourf(xx, yy, Z)

    # Plot also the training points
    plt.scatter(X[:, 0], X[:, 1], c=y)
    plt.xlabel('A')
    plt.ylabel('B')
    plt.xlim(xx.min(), xx.max())
    plt.ylim(yy.min(), yy.max())
    plt.xticks(())
    plt.yticks(())
    plt.title("blah")

    plt.show()

    # import matplotlib.pyplot as plt
    #
    # colormap = np.array(['r', 'k'])
    # labs = [int(x) for x in l]
    # plt.scatter(data[:, [1]], data[:, [2]], c=colormap[labs], s=20)
    # plt.show()

"""
def svm_linear(Data):
    params = {
        'C': [0.1, 0.5, 1, 5, 10, 50, 100],
        'kernel': ['linear']
    }
    return Estimate(SVC(), params, Data)


def svm_polynomial(Data):
    params = {
        'C': [0.1, 1, 3],
        'degree': [4, 5, 6],
        'gamma': [0.1, 0.5],
        'kernel': ['poly']
    }
    return Estimate(SVC(), params, Data)


def svm_rbf(Data):
    params = {
        'C': [0.1, 0.5, 1, 5, 10, 50, 100],
        'gamma': [0.1, 0.5, 1, 3, 6, 10],
        'kernel': ['rbf']
    }
    return Estimate(SVC(), params, Data)


def logistic(Data):
    params = {
        'C': [0.1, 0.5, 1, 5, 10, 50, 100],
    }
    return Estimate(lr(), params, Data)


def knn(Data):
    params = {
        'n_neighbors': range(1, 51),
        'leaf_size': range(5, 65, 5),
    }
    return Estimate(KNN(), params, Data)


def decision_tree(Data):
    params = {
        'max_depth': range(1, 51),
        'min_samples_split': range(2, 11)
    }
    return Estimate(DTC(), params, Data)


def random_forest(Data):
    params = {
        'max_depth': range(1, 51),
        'min_samples_split': range(2, 11)
    }
    return Estimate(RFC(), params, Data)


def Estimate(Method, params, Data):
    clf = GridSearchCV(Method, params, n_jobs=-1)
    clf.fit(Data[0], Data[2])
    best_score = clf.best_score_
    test_score = clf.score(Data[1], Data[3])
    return best_score, test_score
"""

functions = [SVC, SVC, SVC, lr, KNN, DTC, RFC]

Methods = {'svm_linear': {'C': [0.1, 0.5, 1, 5, 10, 50, 100],
                          'kernel': ['linear']},
           'svm_polynomial': {'C': [0.1, 1, 3],
                              'degree': [4, 5, 6],
                              'gamma': [0.1, 0.5],
                              'kernel': ['poly']},
           'svm_rbf': {'C': [0.1, 0.5, 1, 5, 10, 50, 100],
                       'gamma': [0.1, 0.5, 1, 3, 6, 10],
                       'kernel': ['rbf']},
           'logistic': {'C': [0.1, 0.5, 1, 5, 10, 50, 100], },
           'knn': {'n_neighbors': range(1, 51),
                   'leaf_size': range(5, 65, 5), },
           'decision_tree': {'max_depth': range(1, 51),
                             'min_samples_split': range(2, 11)},
           'random_forest': {'max_depth': range(1, 51),
                             'min_samples_split': range(2, 11)}
           }


def main():
    Data, i = formulate_data('input3.csv'), 0
    # showGraph(data, labels)
    with open('Output3.csv', mode='w') as f:
        for method in Methods:
            clf = GridSearchCV(functions[i](), Methods[method], n_jobs=-1)
            clf.fit(Data[0], Data[2])
            best_score, test_score = clf.best_score_, clf.score(Data[1], Data[3])
            f.write(str(method) + ',' + str(best_score) + ',' + str(test_score)+'\n')
            i += 1


if __name__ == "__main__":
    main()
