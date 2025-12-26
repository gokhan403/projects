import joblib
import pandas as pd
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay
from matplotlib import pyplot as plt

rf = joblib.load("random_forest.pkl")
encoder = joblib.load("encoder.pkl")
df = pd.read_csv("veri/UNSW-NB15/UNSW-NB15_3_with_names.csv")

print(rf.get_params())
print(rf.estimators_)
print(rf.n_features_in_)
print(rf.feature_names_in_)
print(rf.classes_)

labels = df[["attack_cat"]]
labels_array = labels.to_numpy()

df2 = df.drop(columns=["Unnamed: 0", "state", "sloss", "dloss", "trans_depth", "res_bdy_len", "tcprtt", "synack",
                           "ackdat", "ct_state_ttl", "ct_flw_http_mthd","is_ftp_login", "ct_ftp_cmd", "ct_srv_src",
                           "ct_srv_dst", "ct_dst_ltm", "ct_src_ ltm", "ct_src_dport_ltm", "ct_dst_sport_ltm",
                           "ct_dst_src_ltm", "attack_cat", "Label"]) # 19 özellik çıktı 2 etiket çıktı 28 özellik kaldı
columns_to_encode = ["srcip", "dstip", "proto", "service"]

df2_encoded = pd.DataFrame(encoder.transform(df2[columns_to_encode]),
                                    columns=encoder.get_feature_names_out(columns_to_encode),
                                    index=df2.index)
df2_encoded_final = pd.concat([df2.drop(columns=columns_to_encode), df2_encoded], axis=1)

predictions = rf.predict(df2_encoded_final)

#print(labels_array)
#print(predictions)
#print(df.value_counts("attack_cat"))

display_labels = ["Fuzzer", "Keşif", "Kabuk Kodu", "Analiz", "Arka Kapı", "Hizmet Reddi", "Sömürme",
                  "Genel Saldırı", "Normal", "Solucan"]

cf_matrix = confusion_matrix(labels, predictions)
disp = ConfusionMatrixDisplay(confusion_matrix=cf_matrix, display_labels=display_labels)
disp.plot(cmap="Blues", values_format="d", xticks_rotation="vertical")
disp.ax_.set_xlabel("Tahmin")
disp.ax_.set_ylabel("Gerçek")
plt.subplots_adjust(bottom=0.15)
plt.show()
