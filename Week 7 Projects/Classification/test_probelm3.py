import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import GridSearchCV, train_test_split
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier as RFC
from sklearn.linear_model import LogisticRegression as lr
from sklearn.neighbors import KNeighborsClassifier as KNN
from sklearn.tree import DecisionTreeClassifier as DTC


def formulate_data(file):
    Data = np.loadtxt(file, delimiter=',', skiprows=1)
    x_train, x_test, y_train, y_test = train_test_split(Data[:, [0, 1]], Data[:, [2]].flatten(),
                                                        test_size=0.4, random_state=42)
    return x_train, x_test, y_train, y_test


Names = {}

Methods = ['svm_linear']


def main():
    Data, i = formulate_data('input3.csv'), 0
    # showGraph(data, labels)
    with open('Output3.csv', mode='w') as f:
        funcs = {SVC: {
            'C': [0.1, 0.5, 1, 5, 10, 50, 100],
            'kernel': ['linear']}}
        for fn in funcs:
            clf = GridSearchCV(fn(), funcs[fn], n_jobs=-1)
            clf.fit(Data[0], Data[2])
            best_score, test_score = clf.best_score_, clf.score(Data[1], Data[3])
            f.write(str(Methods[i]) + ',' + str(best_score) + ',' + str(test_score))
            i += 1


if __name__ == "__main__":
    main()
