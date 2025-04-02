import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d
import pandas as pd
import math
from sklearn.model_selection import KFold
from sklearn.metrics import mean_squared_error


data = pd.read_csv('C:\\Users\\User\\Desktop\\ödev4\\data1.txt')
f1 = data.RUZGAR
f2 = data.SICAKLIK
target = data.YANMIS_ALAN

# veri kumesini duzenle ve normallestir
points = []
for i in range(f1.shape[0]):
    points.append((data.values[i, 1:-1], data.values[i, 0]))


def F(w, x_data, y_data):
    return sum((w.dot(x)-y)**2 for x, y in zip(x_data, y_data))/(2*len(x_data))


def dF(w, x_data, y_data):
    return sum((w.dot(x)-y)*x for x, y in zip(x_data, y_data))/(len(x_data))


def regularization_dF(w, x_data, y_data):
    return sum((w.dot(x)-y)*x for x, y in zip(x_data, y_data))


###########################################
# Algorithms
def gradientDescent(F, dF, d, x_data, y_data):
    w = np.zeros(d)  # initialization
    alpha = 0.0001

    for t in range(100):
        value = F(w, x_data, y_data)
        gradient = dF(w, x_data, y_data)
        w = w - alpha * gradient
        print('Iteration {}: w = {}, F(w) = {} '.format(t, w, value))

    return w


def regularization_gradientDescent(F, regularization_dF, d, x_data, y_data):
    w = np.zeros(d)  # initialization
    alpha = 0.0001
    reg_term = 100.24

    for t in range(100):
        value = F(w, x_data, y_data)
        gradient = regularization_dF(w, x_data, y_data)
        w = w * (1 - ((alpha * reg_term)/len(x_data))) - ((alpha/len(x_data)) * gradient)
        print('Iteration {}: w = {}, F(w) = {} '.format(t, w, value))

    return w


def regression_experiments(points):
    # Veriyi 5 kat capraz gecerleme ile parcalayarak modelleri egit
    points = np.asarray(points, dtype='object')
    kf = KFold(n_splits=5, random_state=None, shuffle=False)
    count = 1
    for train_index, test_index in kf.split(points):
        print("TRAIN:", train_index, "TEST:", test_index)
        X_train, X_test = points[train_index, 0], points[test_index, 0]
        y_train, y_test = points[train_index, 1], points[test_index, 1]
        # 3 ayri ogrenme modelini egit ve test et
        gd_training_theta = gradientDescent(F, dF, 3, X_train, y_train)
        rgd_training_theta = regularization_gradientDescent(F, regularization_dF, 3, X_train, y_train)

        gd_predictions = []
        rgd_predictions = []
        for j in range(len(X_test)):
            gd_predictions.append(gd_training_theta[0] +
                                  gd_training_theta[1]*X_test[j][1] + gd_training_theta[2]*X_test[j][2])
            rgd_predictions.append(rgd_training_theta[0] +
                                  rgd_training_theta[1]*X_test[j][1] + rgd_training_theta[2]*X_test[j][2])

        gd_mse = mean_squared_error(y_test, gd_predictions)
        rgd_mse = mean_squared_error(y_test, rgd_predictions)
        print("{}. kat başarı oranı: {}".format(count, gd_mse))
        print("{}. kat başarı oranı: {}".format(count, rgd_mse))
        count += 1


##################################################
# COK DEGISKENLI REGRESYON PROBLEMI
##################################################
if __name__ == "__main__":
    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')
    ax.plot3D(f1, f2, target, 'rx')
    ax.set_xlabel('Ruzgar')
    ax.set_ylabel('Sicaklik')
    ax.set_zlabel('Yanmis Orman Alani')
    # c=target, cmap='Greens' cmap='viridis', linewidth=0.5)
    # show it
    plt.show(block=True)

    regression_experiments(points)
