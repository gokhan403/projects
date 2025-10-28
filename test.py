from scapy.all import *
from sklearn.metrics import classification_report
from packetcapture import *
from signature_based import *

flow_labels = {}
packets = []

attacker_ip = "192.168.1.100"
victim_ip = "192.168.1.200"

# normal
for i in range(5):
    pkt = IP(src="192.168.1.10", dst="192.168.1.20") / TCP(sport=12345+i, dport=80, flags="PA") / Raw(load="GET / HTTP/1.1\r\n")
    packets.append(pkt)
    flow_labels[("192.168.1.10", 12345+i, "192.168.1.20", 80)] = "Normal"

# fuzzer
for i in range(10):
    pkt = (IP(src=attacker_ip, dst=victim_ip)/UDP(sport=int(RandShort()), dport=int(RandShort())))/Raw(load=os.urandom(1400))
    send(pkt)
    packets.append(pkt)
    flow_labels[(pkt[IP].src, pkt[UDP].sport, pkt[IP].dst, pkt[UDP].dport)] = "Fuzzer"
    time.sleep(0.01)

#analysis
for _ in range(10):
    pkt_analysis = IP(src=attacker_ip, dst=victim_ip, ttl=1)/TCP(sport=4444, dport=80, seq=123456)/Raw(load="A"*2000)
    send(pkt_analysis)
    packets.append(pkt_analysis)
    flow_labels[(pkt_analysis[IP].src, pkt_analysis[TCP].sport, pkt_analysis[IP].dst, pkt_analysis[TCP].dport)] = "Analiz"

# backdoor
for _ in range(5):
    pkt_backdoor = IP(src=attacker_ip, dst=victim_ip)/TCP(sport=6666, dport=4444)/Raw(load="BackdoorAccess")
    send(pkt_backdoor)
    packets.append(pkt_backdoor)
    flow_labels[(pkt_backdoor[IP].src, pkt_backdoor[TCP].sport, pkt_backdoor[IP].dst, pkt_backdoor[TCP].dport)] = "Arka Kapı"

# dos
for _ in range(20):
    pkt = IP(src=attacker_ip, dst=victim_ip)/UDP(sport=int(RandShort()), dport=80)/Raw(load="X"*1400)
    send(pkt)
    packets.append(pkt)
    flow_labels[(pkt[IP].src, pkt[UDP].sport, pkt[IP].dst, pkt[UDP].dport)] = "Hizmet Reddi"
    time.sleep(0.01)

# exploits
exploit_payload = "EXPLOIT" + "A"*1400
for _ in range(10):
    pkt_exploits = IP(src=attacker_ip, dst=victim_ip)/TCP(sport=135, dport=139)/Raw(load=exploit_payload)
    send(pkt_exploits)
    packets.append(pkt_exploits)
    flow_labels[(pkt_exploits[IP].src, pkt_exploits[TCP].sport, pkt_exploits[IP].dst, pkt_exploits[TCP].dport)] = "Sömürme"

# generic
for _ in range(5):
    pkt_generic = IP(src=attacker_ip, dst=victim_ip)/TCP(sport=12345, dport=443)/Raw(load=os.urandom(1500))
    send(pkt_generic)
    packets.append(pkt_generic)
    flow_labels[(pkt_generic[IP].src, pkt_generic[TCP].sport, pkt_generic[IP].dst, pkt_generic[TCP].dport)] = "Genel"

# recon
for port in range(20, 30):
    pkt = IP(src=attacker_ip, dst=victim_ip)/TCP(sport=int(RandShort()), dport=port)/Raw(load="SYN")
    send(pkt)
    packets.append(pkt)
    flow_labels[(pkt[IP].src, pkt[TCP].sport, pkt[IP].dst, pkt[TCP].dport)] = "Keşif"
    time.sleep(0.05)

# shellcode
for _ in range(5):
    pkt_shellcode = IP(src=attacker_ip, dst=victim_ip)/TCP(sport=31337, dport=8080)/Raw(load="\x90"*100 + "SHELL")
    send(pkt_shellcode)
    packets.append(pkt_shellcode)
    flow_labels[(pkt_shellcode[IP].src, pkt_shellcode[TCP].sport, pkt_shellcode[IP].dst, pkt_shellcode[TCP].dport)] = "Kabuk Kodu"

# worm
for i in range(5):
    pkt = IP(src=attacker_ip, dst=victim_ip)/TCP(sport=int(RandShort()), dport=1000+i)/Raw(load="WORM"*300)
    send(pkt)
    packets.append(pkt)
    flow_labels[(pkt[IP].src, pkt[TCP].sport, pkt[IP].dst, pkt[TCP].dport)] = "Solucan"
    time.sleep(0.05)
"""
anomaly_pred = {"['Normal']": 'Normal', "[' Fuzzers ']": 'Fuzzer', "['DoS']": 'Hizmet Reddi',
                    "['Analysis']": 'Analiz', "['Backdoor']": 'Arka Kapı', "[' Shellcode ']": 'Kabuk Kodu',
                    "[' Reconnaissance ']": 'Keşif', "['Exploits']": 'Sömürme', "['Worms']": 'Solucan',
                    "['Generic']": 'Genel'}
columns_to_encode = ["srcip", "dstip", "proto", "service"]
predictions_anomaly = []
predictions_signature = []

model = joblib.load("random_forest.pkl")
encoder = joblib.load("encoder.pkl")

analyzer = TrafficAnalyzer()

length = len(predictions_signature)


for pkt in packets:
    features = analyzer.analyze_packet(pkt)
    sample_df = pd.DataFrame([features])

    for attack_type, detect_function in signature_database.items():
        if detect_function(sample_df):
            predictions_signature.append(attack_type)
            break

    if length < len(predictions_signature):
        length = len(predictions_signature)
    elif length == len(predictions_signature):
        predictions_signature.append("Normal")
        length = len(predictions_signature)


    encoded_sample = pd.DataFrame(encoder.transform(sample_df[columns_to_encode]),
                                  columns=encoder.get_feature_names_out(columns_to_encode),
                                  index=sample_df.index)
    final_sample = pd.concat([sample_df.drop(columns=columns_to_encode), encoded_sample], axis=1)

    pred = model.predict(final_sample)
    predictions_anomaly.append(pred[0])

    time.sleep(0.01)


y_true = []
y_pred_anomaly = []
y_pred_signature = []
for flow, label in flow_labels.items():
    y_true.append(label)

for i in range(len(predictions_anomaly)):
    y_pred_anomaly.append(predictions_anomaly[i])

for i in range(len(predictions_signature)):
    y_pred_signature.append(predictions_signature[i])


print(classification_report(y_true, y_pred_anomaly))
print(classification_report(y_true, y_pred_signature))
"""