import pandas as pd
from time import time
from datetime import timedelta
import numpy as np
from sklearn.ensemble import RandomForestClassifier, ExtraTreesClassifier
from sklearn.model_selection import train_test_split, StratifiedKFold
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay
from sklearn.utils import shuffle
from joblib import dump
import matplotlib.pyplot as plt
import gc
import warnings

warnings.filterwarnings("ignore", category=FutureWarning)

# değerlendirme fonksiyonu, eğitilmiş modelin accuracy, precision
# recall ve f1 skorlarını hesaplar
def evaluation(Y_actuals, Y_predictions, pos_label):
    accuracy = accuracy_score(Y_actuals, Y_predictions)
    precision = precision_score(Y_actuals, Y_predictions, pos_label=pos_label)
    recall = recall_score(Y_actuals, Y_predictions, pos_label=pos_label)
    f1 = f1_score(Y_actuals, Y_predictions, pos_label=pos_label)
    print("Doğruluk: ", accuracy)
    print("Kesinlik: ", precision)
    print("Duyarlılık: ", recall)
    print("F1: ", f1)

# Random Forest modelinin eğitilmesi ve test edilmesi
def random_forest(X_train, Y_train, X_test, Y_test, model):
    start_time = time()
    model.fit(X_train, Y_train)
    Y_predictions = model.predict(X_test)
    evaluation(Y_test, Y_predictions, pos_label="Normal")
    print("Çalışma süresi: ", str(timedelta(seconds=time()-start_time)))
    return Y_predictions

# Extra Trees modelinin eğitilmesi ve test edilmesi
def extra_tree(X_train, Y_train, X_test, Y_test, model):
    start_time = time()
    model.fit(X_train, Y_train)
    Y_predictions = model.predict(X_test)
    evaluation(Y_test, Y_predictions, pos_label="Normal")
    print("Çalışma süresi: ", str(timedelta(seconds=time()-start_time)))
    return Y_predictions


if __name__ == "__main__":
    # veri okunur ve modeller oluşturulur
    df = pd.read_csv("data/CSV/combined_data.csv")
    rf = RandomForestClassifier(criterion="gini", n_jobs=-1, max_depth=26, n_estimators=70)
    et = ExtraTreesClassifier(criterion="gini", n_jobs=-1, max_depth=26, n_estimators=70)

    # veri ön işlem aşamaları, veri küçültülür önemsiz özellikler çıkarılır
    normal_samples = df[df["Label"] == "Normal"].sample(n=40000, random_state=42)
    attack_samples = df[df["Label"] == "Attack"].sample(n=40000, random_state=42)

    processed_df = pd.concat([normal_samples, attack_samples])
    processed_df = processed_df.drop(columns=["generated", "startDateTime", "stopDateTime",
                                              "destinationPayloadAsBase64", "sourcePayloadAsUTF",
                                              "destinationPayloadAsUTF", "sourcePayloadAsBase64",
                                              ])
    processed_df = processed_df.fillna("")
    processed_df = shuffle(processed_df, random_state=42).reset_index(drop=True)
    columns_to_encode = ["appName", "sourceTCPFlagsDescription", "destinationTCPFlagsDescription",
                                              "source", "protocolName", "destination", "direction"]

    # kategoriksel veriler sayısal olarak kodlanır
    encoded_df = pd.get_dummies(processed_df, columns=columns_to_encode)

    y = encoded_df["Label"]
    X = encoded_df.drop(columns=["Label"])

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, stratify=y)
    del X, y
    gc.collect()
    rf_pred = random_forest(X_train, y_train, X_test, y_test, rf)
    print("\n")
    et_pred = extra_tree(X_train, y_train, X_test, y_test, et)

    """
    skf = StratifiedKFold(n_splits=5)
    rf_scores = {"doğruluk": [], "kesinlik": [], "duyarlılık": [], "f1": []}
    et_scores = {"doğruluk": [], "kesinlik": [], "duyarlılık": [], "f1": []}
    pos_label = "Normal"
    rf_pred, et_pred, best_rf_pred, best_et_pred = None, None, None, None
    best_rf_accuracy, best_et_accuracy = None, None
    y_test, best_rf_test, best_et_test = None, None, None
    i = 0
    for train_index, test_index in skf.split(X, y):
        X_train, X_test = X.iloc[train_index], X.iloc[test_index]
        y_train, y_test = y.iloc[train_index], y.iloc[test_index]
        rf_pred = random_forest(X_train, y_train, X_test, y_test, rf)

        rf_accuracy = accuracy_score(y_test, rf_pred)
        rf_precision = precision_score(y_test, rf_pred, pos_label=pos_label)
        rf_recall = recall_score(y_test, rf_pred, pos_label=pos_label)
        rf_f1 = f1_score(y_test, rf_pred, pos_label=pos_label)

        rf_scores["doğruluk"].append(rf_accuracy)
        rf_scores["kesinlik"].append(rf_precision)
        rf_scores["duyarlılık"].append(rf_recall)
        rf_scores["f1"].append(rf_f1)

        print("\n")
        et_pred = extra_tree(X_train, y_train, X_test, y_test, et)
        print("\n")

        et_accuracy = accuracy_score(y_test, et_pred)
        et_precision = precision_score(y_test, et_pred, pos_label=pos_label)
        et_recall = recall_score(y_test, et_pred, pos_label=pos_label)
        et_f1 = f1_score(y_test, et_pred, pos_label=pos_label)

        et_scores["doğruluk"].append(et_accuracy)
        et_scores["kesinlik"].append(et_precision)
        et_scores["duyarlılık"].append(et_recall)
        et_scores["f1"].append(et_f1)

        if best_rf_accuracy is None:
            best_rf_accuracy = rf_scores["doğruluk"][i]
            best_rf_pred = rf_pred
            best_rf_test = y_test
        elif best_rf_accuracy < rf_scores["doğruluk"][i]:
            best_rf_accuracy = rf_scores["doğruluk"][i]
            best_rf_pred = rf_pred
            best_rf_test = y_test

        if best_et_accuracy is None:
            best_et_accuracy = et_scores["doğruluk"][i]
            best_et_pred = et_pred
            best_et_test = y_test
        elif best_et_accuracy < et_scores["doğruluk"][i]:
            best_et_accuracy = et_scores["doğruluk"][i]
            best_et_pred = et_pred
            best_et_test = y_test

        i += 1


    dump(rf, "network_classifier.joblib")

    for metric, values in rf_scores.items():
        print(f"Random Forest ortalama {metric} skoru: {np.mean(values)}")
    for metric, values in et_scores.items():
        print(f"Extra Trees ortalama {metric} skoru: {np.mean(values)}")


    # tahminlerin gerçek etiketlere göre dağılımını veren karışıklık matrisleri
    cf_matrix = confusion_matrix(best_rf_test, best_rf_pred)
    disp = ConfusionMatrixDisplay(confusion_matrix=cf_matrix, display_labels=["Saldırı", "Normal"])
    disp.plot(cmap="Blues", values_format="d")
    disp.ax_.set_xlabel("Tahmin")
    disp.ax_.set_ylabel("Gerçek")
    plt.show()

    cf_matrix = confusion_matrix(best_et_test, best_et_pred)
    disp = ConfusionMatrixDisplay(confusion_matrix=cf_matrix, display_labels=["Saldırı", "Normal"])
    disp.plot(cmap="Blues", values_format="d")
    disp.ax_.set_xlabel("Tahmin")
    disp.ax_.set_ylabel("Gerçek")
    plt.show()
    """
