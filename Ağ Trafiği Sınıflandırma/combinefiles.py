import pandas as pd
from sklearn.utils import shuffle
import time
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

"""
df1 = pd.read_csv("data/CSV/TestbedSatJun12Flows.csv")
df2 = pd.read_csv("data/CSV/TestbedSunJun13Flows.csv")
df3 = pd.read_csv("data/CSV/TestbedMonJun14Flows.csv")
df4 = pd.read_csv("data/CSV/TestbedTueJun15Flows.csv")
df5 = pd.read_csv("data/CSV/TestbedWedJun16Flows.csv")
df6 = pd.read_csv("data/CSV/TestbedThuJun17Flows.csv")

combined1 = pd.concat([df1, df2])
combined2 = pd.concat([combined1, df3])
combined3 = pd.concat([combined2, df4])
combined4 = pd.concat([combined3, df5])
combined5 = pd.concat([combined4, df6])

combined5.to_csv("data/CSV/combined_data.csv", index=False)
"""
start_time = time.time()

# veri okunur
df = pd.read_csv("data/CSV/combined_data.csv")

# veri ön işlem aşamaları, veri küçültülür önemsiz özellikler çıkarılır
normal_samples = df[df["Label"] == "Normal"].sample(n=81090, random_state=42)
attack_samples = df[df["Label"] == "Attack"].sample(n=68910)
processed_df = pd.concat([normal_samples, attack_samples])
processed_df = processed_df.drop(columns=["generated", "startDateTime", "stopDateTime",
                                          "destinationPayloadAsBase64", "sourcePayloadAsUTF",
                                          "destinationPayloadAsUTF", "sourcePayloadAsBase64"])

# verideki boş değerler doldurulur, veri karıştırılır
# ve kategoriksel veriler kodlanır
processed_df = processed_df.fillna("")
processed_df = shuffle(processed_df, random_state=42).reset_index(drop=True)
print(processed_df.info())
columns_to_encode = ["appName", "sourceTCPFlagsDescription", "destinationTCPFlagsDescription",
                         "source", "protocolName", "destination", "direction"]
encoded_df = pd.get_dummies(processed_df, columns=columns_to_encode)


print(encoded_df.info())
print("elapsed time: ", (time.time() - start_time))
