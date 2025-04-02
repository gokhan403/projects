import numpy as np
import matplotlib.pyplot as plt
import math
from sklearn.model_selection import KFold
import scipy.io
from LDA import *
from sklearn.metrics import confusion_matrix, accuracy_score, precision_score, recall_score, f1_score
import seaborn as sns

##################################################
# IKI SINIFLI SINIFLANDIRMA PROBLEMI
##################################################
# veriyi yukle
data = scipy.io.loadmat('C:\\Users\\User\\Desktop\\ödev4\\data2.mat')
# Veri gorselleme amacli grafikleri  cizdir
features = np.asarray(data['features'])
labels = np.asarray(data['classes'])
data_zeros_mask = np.where(labels==0)
data_zeros = features[data_zeros_mask[0],:]
plt.plot(data_zeros[:,0], data_zeros[:,1], 'mo')
data_ones_mask = np.where(labels==1)
data_ones = features[data_ones_mask[0],:]
plt.plot(data_ones[:,0], data_ones[:,1], 'gx')
plt.xlabel('Ozellik 1')
plt.ylabel('Ozellik 2')
plt.show(block=True)

# veri kumesini duzenle ve normallestir
points = []
for i in range(features.shape[0]):
    points.append((features[i,:][:],labels[i,0]))


def sigmoid(z):
    return 1 / (1 + np.exp(-z))


def F(w, x_data, y_data, sigmoid):
    return -1 * (sum(y * math.log(sigmoid(w.dot(x)) + 1e-15) +
                                  (1 - y) * (math.log(1 - sigmoid(w.dot(x)) + 1e-15))
                                  for x, y in zip(x_data, y_data))) / len(x_data)


def dF(w, x_data, y_data, sigmoid):
    return sum((sigmoid(w.dot(x)) - y)*x for x, y in zip(x_data, y_data))/(len(x_data))


def gradientDescent(F, dF, d, x_data, y_data, sigmoid):
    w = np.zeros(d)  # initialization
    alpha = 0.0001

    for t in range(100):
        value = F(w, x_data, y_data, sigmoid)
        gradient = dF(w, x_data, y_data, sigmoid)
        w = w - alpha * gradient
        print('Iteration {}: w = {}, F(w) = {} '.format(t, w, value))

    return w


# Veriyi 5 kat capraz gecerleme ile parcalayarak modelleri egit
points = np.asarray(points, dtype='object')
kf = KFold(n_splits=5, random_state=None, shuffle=True)
for train_index, test_index in kf.split(points):
    print("TRAIN:", train_index, "TEST:", test_index)
    X_train, X_test = points[train_index,0], points[test_index,0]
    y_train, y_test = points[train_index,1], points[test_index,1]
    # myLogisticRegression()
    gd_train_theta = gradientDescent(F, dF, 2, X_train, y_train, sigmoid)
    w0 = 0.02
    w1, w2 = gd_train_theta[0], gd_train_theta[1]

    gd_predictions = []
    for j in range(len(X_test)):
        gd_predictions.append(sigmoid(np.dot(gd_train_theta, X_test[j])))

    lr_predictions = []
    for k in range(len(gd_predictions)):
        if gd_predictions[k] >= 0.495:
            lr_predictions.append(1)
        else:
            lr_predictions.append(0)

    print(lr_predictions)
    print(y_test)

    y_test = np.array(y_test, dtype=np.int64)
    lr_predictions = np.array(lr_predictions, dtype=np.int64)
    conf_matrix = confusion_matrix(y_test, lr_predictions)
    accuracy = accuracy_score(y_test, lr_predictions)
    precision = precision_score(y_test, lr_predictions, zero_division=True)
    recall = recall_score(y_test, lr_predictions)
    f1 = f1_score(y_test, lr_predictions)

    print("Accuracy: {}, Precision: {}, Recall: {}, F1_Score: {}".format(accuracy, precision, recall, f1))

    # karmaşa matrisleri
    plt.figure(figsize=(8, 6))
    sns.heatmap(conf_matrix, annot=True, fmt="d", cmap="Blues",
                xticklabels=['0', '1'],
                yticklabels=['0', '1'])
    plt.xlabel("Tahmin")
    plt.ylabel("Gerçek")
    plt.title("Karmaşa Matrisi")
    plt.show()

    # karar sınırı
    plt.figure(figsize=(8, 6))
    plt.scatter(data_zeros[:, 0], data_zeros[:, 1], c='red', label='Class 0')
    plt.scatter(data_ones[:, 0], data_ones[:, 1], c='green', label='Class 1')

    x_values = np.linspace(min(features[:, 0]), max(features[:, 0]), 100)

    y_values = -(w0 / w2) - (w1 / w2) * x_values

    plt.plot(x_values, y_values, label='Decision Boundary', color='k')

    plt.xlabel('Ozellik 1')
    plt.ylabel('Ozellik 2')
    plt.legend()
    plt.show()
