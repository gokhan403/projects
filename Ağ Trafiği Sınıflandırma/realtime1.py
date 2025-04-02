import pandas as pd
import numpy as np
from scapy.all import *
import joblib
from sklearn.utils import shuffle
from sklearn.ensemble import RandomForestClassifier

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

realtime_df = pd.DataFrame()
realtime_encoded_df = pd.DataFrame()

def process_packet(packet):
    columns_of_df = ["appName", "sourceTCPFlagsDescription", "destinationTCPFlagsDescription",
                     "source", "protocolName", "destination", "direction", "totalSourceBytes",
                     "totalDestinationBytes", "totalSourcePackets", "totalDestinationPackets",
                     "sourcePort", "destinationPort"]
    realtime_df = pd.DataFrame(columns=columns_of_df)

    realtime_df["appName"] = packet.layers()
    realtime_df["sourceTCPFlagsDescription"] = ""
    realtime_df["destinationTCPFlagsDescription"] = ""
    realtime_df["source"] = 0
    realtime_df["protocolName"] = ""
    realtime_df["destination"] = 0
    realtime_df["direction"] = packet.direction
    realtime_df["totalSourceBytes"] = len(packet)
    realtime_df["totalDestinationBytes"] = len(packet)
    realtime_df["totalSourcePackets"] = 1
    realtime_df["totalDestinationPackets"] = 1
    realtime_df["sourcePort"] = 0
    realtime_df["destinationPort"] = 0
    realtime_df["Label"] = object()

    realtime_encoded_df = pd.get_dummies(realtime_df, columns=["appName", "sourceTCPFlagsDescription", "destinationTCPFlagsDescription",
                                             "protocolName", "direction"])

    expected_columns = encoded_df.columns
    for col in expected_columns:
        if col not in realtime_encoded_df:
            realtime_encoded_df[col] = False

    realtime_encoded_df = realtime_encoded_df[expected_columns]

    # print(realtime_encoded_df.info())
    # print(realtime_encoded_df.shape)
    # print(encoded_df.info())
    # print(encoded_df.shape)
    # print(encoded_df.select_dtypes(include=["object"]).columns)


if __name__ == "__main__":
    pkt_list = sniff(prn=process_packet, count=10)

    model = joblib.load("network_classifier.joblib")
    predictions = model.predict(realtime_encoded_df)
    print(predictions)
