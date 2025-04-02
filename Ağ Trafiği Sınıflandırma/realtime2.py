import pandas as pd
import numpy as np
import pyshark
import joblib
from sklearn.preprocessing import OneHotEncoder


columns_of_df = ["totalSourceBytes",
                     "totalDestinationBytes", "totalDestinationPackets", "totalSourcePackets",
                     "sourcePort", "destinationPort"]
df = pd.DataFrame(columns=columns_of_df)

# appName = []
# sourceTCPFlagsDescription = []
# destinationTCPFlagsDescription = []
# source = []
# protocolName = []
# destination = []
#direction = []
totalSourceBytes = []
totalDestinationBytes = []
totalSourcePackets = []
totalDestinationPackets = []
sourcePort = []
destinationPort = []

capture = pyshark.LiveCapture(display_filter="ip")

for packet in capture.sniff_continuously(packet_count=100):
    print(packet.ip.src)
    print(packet.highest_layer)


    # appName.append(packet.highest_layer)
    # sourceTCPFlagsDescription.append("")
    # destinationTCPFlagsDescription.append("")
    # source.append(packet.ip.src)
    # protocolName.append(packet.transport_layer)
    # destination.append(packet.ip.dst)
    """
    if packet.ip.src.startswith('192.168.'):
        if packet.ip.dst.startswith('192.168.'):
            direction.append("L2L")
        else:
            direction.append("L2R")
    else:
        if packet.ip.dst.startswith('192.168.'):
            direction.append("R2L")
        else:
            direction.append("R2R")
    """
    totalSourceBytes.append(int(packet.length))
    totalDestinationBytes.append(0)
    totalSourcePackets.append(1)
    totalDestinationPackets.append(1)
    sourcePort.append(packet[packet.transport_layer].srcport)
    destinationPort.append(packet[packet.transport_layer].dstport)

# df["appName"] = appName
# df["sourceTCPFlagsDescription"] = sourceTCPFlagsDescription
# df["destinationTCPFlagsDescription"] = destinationTCPFlagsDescription
# df["source"] = source
# df["protocolName"] = protocolName
# df["destination"] = destination
#df["direction"] = direction
df["totalSourceBytes"] = totalSourceBytes
df["totalDestinationBytes"] = totalDestinationBytes
df["totalDestinationPackets"] = totalDestinationPackets
df["totalSourcePackets"] = totalSourcePackets
df["sourcePort"] = sourcePort
df["destinationPort"] = destinationPort
# print(df)
# print(df.info())
# print(df.shape)

# encoder = OneHotEncoder(sparse=False, handle_unknown="ignore")
# encoded_data = encoder.fit_transform(df[["direction"]])
# encoded_df = pd.DataFrame(encoded_data, columns=encoder.get_feature_names_out(["direction"]))
# df = df.drop(columns=["direction"], axis=1)
# df = pd.concat([df, encoded_df], axis=1)

model = joblib.load("lasttry.joblib")
predictions = model.predict(df)
print(predictions)
