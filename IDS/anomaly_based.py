import pandas as pd
from time import time
from datetime import timedelta
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split, RandomizedSearchCV, StratifiedKFold
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from sklearn.preprocessing import OneHotEncoder
import joblib
import numpy as np

def evaluation(Y_actuals, Y_predictions, average):
    accuracy = accuracy_score(Y_actuals, Y_predictions)
    precision = precision_score(Y_actuals, Y_predictions, average="weighted", zero_division=False)
    recall = recall_score(Y_actuals, Y_predictions, average="weighted")
    f1 = f1_score(Y_actuals, Y_predictions, average="weighted")
    print("Doğruluk: ", accuracy)
    print("Kesinlik: ", precision)
    print("Duyarlılık: ", recall)
    print("F1: ", f1)

if __name__ == "__main__":
    df = pd.read_csv("veri/UNSW-NB15/UNSW-NB15_3_with_names.csv")
    #df = df.fillna("")
    #df1 = df.drop(columns=["ct_flw_http_mthd", "is_ftp_login", "Unnamed: 0"]) # 2 özellik çıktı 2 etiket çıktı 45 özellik
    #columns_to_encode1 = ["srcip", "dstip", "proto", "state", "service", "ct_ftp_cmd"]
    df2 = df.drop(columns=["Unnamed: 0", "state", "sloss", "dloss", "trans_depth", "res_bdy_len", "tcprtt", "synack",
                           "ackdat", "ct_state_ttl", "ct_flw_http_mthd","is_ftp_login", "ct_ftp_cmd", "ct_srv_src",
                           "ct_srv_dst", "ct_dst_ltm", "ct_src_ ltm", "ct_src_dport_ltm", "ct_dst_sport_ltm",
                           "ct_dst_src_ltm"]) # 19 özellik çıktı 2 etiket çıktı 28 özellik kaldı
    columns_to_encode2 = ["srcip", "dstip", "proto", "service"]

    #y1 = df1[["attack_cat"]]
    #X1 = df1.drop(columns=["attack_cat", "Label"])
    y2 = df2[["attack_cat"]]
    X2 = df2.drop(columns=["attack_cat", "Label"])

    #X1_train, X1_temp, y1_train, y1_temp = train_test_split(X1, y1, test_size=0.4, stratify=y1)
    #X1_val, X1_test, y1_val, y1_test = train_test_split(X1_temp, y1_temp, test_size=0.75, stratify=y1_temp)
    X2_temp, X2_test, y2_temp, y2_test = train_test_split(X2, y2, test_size=0.2, stratify=y2)
    #X2_val, X2_test, y2_val, y2_test = train_test_split(X2_temp, y2_temp, test_size=0.75, stratify=y2_temp)

    #feature_encoder1 = OneHotEncoder(handle_unknown="ignore", sparse_output=False)
    feature_encoder2 = OneHotEncoder(handle_unknown="ignore", sparse_output=False)
    #feature_encoder1.fit(X1_train[columns_to_encode1])
    feature_encoder2.fit(X2_temp[columns_to_encode2])

    #X1_train_encoded = pd.DataFrame(feature_encoder1.transform(X1_train[columns_to_encode1]),
     #                              columns=feature_encoder1.get_feature_names_out(columns_to_encode1),
      #                             index=X1_train.index)
    #X1_val_encoded = pd.DataFrame(feature_encoder1.transform(X1_val[columns_to_encode1]),
     #                            columns=feature_encoder1.get_feature_names_out(columns_to_encode1),
      #                           index=X1_val.index)
    #X1_test_encoded = pd.DataFrame(feature_encoder1.transform(X1_test[columns_to_encode1]),
     #                             columns=feature_encoder1.get_feature_names_out(columns_to_encode1),
      #                            index=X1_test.index)

    X2_temp_encoded = pd.DataFrame(feature_encoder2.transform(X2_temp[columns_to_encode2]),
                                    columns=feature_encoder2.get_feature_names_out(columns_to_encode2),
                                    index=X2_temp.index)
    #X2_val_encoded = pd.DataFrame(feature_encoder2.transform(X2_val[columns_to_encode2]),
     #                             columns=feature_encoder2.get_feature_names_out(columns_to_encode2),
      #                            index=X2_val.index)
    X2_test_encoded = pd.DataFrame(feature_encoder2.transform(X2_test[columns_to_encode2]),
                                   columns=feature_encoder2.get_feature_names_out(columns_to_encode2),
                                   index=X2_test.index)

    joblib.dump(feature_encoder2, "encoder.pkl")

    #X1_train_final = pd.concat([X1_train.drop(columns=columns_to_encode1), X1_train_encoded], axis=1)
    #X1_val_final = pd.concat([X1_val.drop(columns=columns_to_encode1), X1_val_encoded], axis=1)
    #X1_test_final = pd.concat([X1_test.drop(columns=columns_to_encode1), X1_test_encoded], axis=1)

    X2_temp_final = pd.concat([X2_temp.drop(columns=columns_to_encode2), X2_temp_encoded], axis=1)
    #X2_val_final = pd.concat([X2_val.drop(columns=columns_to_encode2), X2_val_encoded], axis=1)
    X2_test_final = pd.concat([X2_test.drop(columns=columns_to_encode2), X2_test_encoded], axis=1)

    rf_model = RandomForestClassifier(n_jobs=-1, n_estimators=300, max_depth=20, min_samples_split=5)

    """
    param_dist = {
        "n_estimators": [50, 300],
        "min_samples_split": [5, 7, 15],
    }

    random_search = RandomizedSearchCV(
        rf_model,
        param_distributions=param_dist,
        n_iter=5,
        scoring='accuracy',
        cv=3,
        n_jobs=-1,
        random_state=42
    )
    
    random_search.fit(X_train_final, y_train.values.ravel())
    print("Best params:", random_search.best_params_)
    print("Best score:", random_search.best_score_)
    """
    """
    # 46 özellik
    print("Tüm özelliklerle random forest model performansı:")
    start_time = time()
    rf_model.fit(X1_train_final, y1_train.values.ravel())
    predictions = rf_model.predict(X1_test_final)
    evaluation(y1_test, predictions, average="weighted")
    print("Çalışma süresi: ", str(timedelta(seconds=time() - start_time)))

    # 27 özellik
    print("Azaltılmış özelliklerle random forest model performansı:")
    start_time = time()
    rf_model.fit(X2_train_final, y2_train.values.ravel())
    predictions = rf_model.predict(X2_test_final)
    evaluation(y2_test, predictions, average="weighted")
    print("Çalışma süresi: ", str(timedelta(seconds=time() - start_time)))
    """

    skf = StratifiedKFold(n_splits=5)
    rf_scores = {"doğruluk": [], "kesinlik": [], "duyarlılık": [], "f1": []}
    average = "weighted"
    rf_pred, best_rf_pred = None, None
    best_rf_accuracy = None
    best_rf_test = None
    i = 0
    skf_start = time()
    for train_index, test_index in skf.split(X2_temp_final, y2_temp):
        X_train, X_test = X2_temp_final.iloc[train_index], X2_temp_final.iloc[test_index]
        y_train, y_test = y2_temp.iloc[train_index], y2_temp.iloc[test_index]

        rf_model.fit(X_train, y_train.values.ravel())
        predictions = rf_model.predict(X_test)

        rf_accuracy = accuracy_score(y_test, predictions)
        rf_precision = precision_score(y_test, predictions, average=average, zero_division=False)
        rf_recall = recall_score(y_test, predictions, average=average)
        rf_f1 = f1_score(y_test, predictions, average=average)

        rf_scores["doğruluk"].append(rf_accuracy)
        rf_scores["kesinlik"].append(rf_precision)
        rf_scores["duyarlılık"].append(rf_recall)
        rf_scores["f1"].append(rf_f1)

        if best_rf_accuracy is None:
            best_rf_accuracy = rf_scores["doğruluk"][i]
            best_rf_pred = rf_pred
            best_rf_test = y_test
        elif best_rf_accuracy < rf_scores["doğruluk"][i]:
            best_rf_accuracy = rf_scores["doğruluk"][i]
            best_rf_pred = rf_pred
            best_rf_test = y_test

        i += 1

    for metric, values in rf_scores.items():
        print(f"Random Forest ortalama {metric} skoru: {np.mean(values)}")
        print("SKF süresi: ", str(timedelta(seconds=time() - skf_start)))

    print("Random Forest:")
    start_time = time()
    rf_model.fit(X2_temp_final, y2_temp.values.ravel())
    predictions = rf_model.predict(X2_test_final)
    evaluation(y2_test, predictions, average="weighted")
    print("Çalışma süresi: ", str(timedelta(seconds=time() - start_time)))

    joblib.dump(rf_model, "random_forest.pkl")
