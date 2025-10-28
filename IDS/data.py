import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.inspection import permutation_importance
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OrdinalEncoder
from matplotlib import pyplot as plt

feature_names = ["srcip", "sport", "dstip", "dsport", "proto", "state", "dur", "sbytes", "dbytes", "sttl", "dttl",
                 "sloss", "dloss", "service", "Sload", "Dload", "Spkts", "Dpkts", "swin", "dwin", "stcpb", "dtcpb",
                 "smeansz", "dmeansz", "trans_depth", "res_bdy_len", "Sjit", "Djit", "Stime", "Ltime", "Sintpkt",
                 "Dintpkt", "tcprtt", "synack", "ackdat", "is_sm_ips_ports", "ct_state_ttl", "ct_flw_http_mthd",
                 "is_ftp_login", "ct_ftp_cmd", "ct_srv_src", "ct_srv_dst", "ct_dst_ltm", "ct_src_ ltm", "ct_src_dport_ltm",
                 "ct_dst_sport_ltm", "ct_dst_src_ltm", "attack_cat", "Label"]

features_to_extract = ["dsport", "sttl", "dbytes", "smeansz", "sbytes", "service", "dmeansz", "sport","Spkts",
                       "stcpb", "dtcpb", "dttl", "Dpkts", "Sload", "Dload", "dur"]

columns_to_encode = ["srcip", "dstip", "proto", "state", "service", "ct_flw_http_mthd", "is_ftp_login", "ct_ftp_cmd"]
encoded = ["srcip_encoded", "dstip_encoded", "dsport_encoded", "proto_encoded", "state_encoded", "service_encoded", "ct_ftp_cmd_encoded", "attack_cat_encoded"]

df = pd.read_csv("veri/UNSW-NB15/UNSW-NB15_3.csv")

print(df.info())
print(df.value_counts("Label"))

"""
# özellik önemi hesabı
#df = df.fillna("")
df = df.drop(columns=["ct_flw_http_mthd", "is_ftp_login"])

encoder = OrdinalEncoder(handle_unknown="use_encoded_value", unknown_value=-1)
encoder.fit(df[columns_to_encode])

df[encoded] = encoder.transform(df[columns_to_encode])
df = df.drop(columns=columns_to_encode)

print(df.info())

y = df["attack_cat_encoded"]
X = df.drop(columns=["attack_cat_encoded"], axis=1)
model = RandomForestClassifier(random_state=42)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
model.fit(X_train, y_train)

result = permutation_importance(model, X_test, y_test, n_repeats=10, random_state=42)
perm_importance = pd.DataFrame({"Feature": X.columns, "Importance": result.importances_mean}).sort_values("Importance", ascending=False)

print(perm_importance)
"""

"""
# paket başına gönderilen ortalama bayt
df["mean_byte_per_packet"] = (df["smeansz"] + df["dmeansz"])

label_map = {
    'Normal': 'Normal Trafik',
    ' Fuzzers ': 'Fuzzer',
    'DoS': 'Hizmet Reddi',
    'Analysis': 'Analiz',
    'Backdoor': 'Arka Kapı',
    ' Shellcode ': 'Kabuk Kodu',
    ' Reconnaissance ': 'Keşif',
    'Exploits': 'Sömürme',
    'Worms': 'Solucanlar',
    'Generic': 'Genel Saldırılar'
}

size_distribution = df.groupby("attack_cat")["mean_byte_per_packet"].agg(["mean"])
size_distribution.reset_index(inplace=True)
size_distribution["attack_cat"] = size_distribution["attack_cat"].map(label_map)


x = range(len(size_distribution["attack_cat"]))
width = 0.0

plt.bar(x, size_distribution["mean"], color="salmon")
#plt.bar([i + width for i in x], size_distribution["mean"], width, label="Ortalama", color="salmon")
#plt.bar([i + 2*width for i in x], size_distribution["max"], width, label="Maksimum", color="lightgreen")

plt.xticks([i for i in x], size_distribution["attack_cat"], rotation=45)
plt.xlabel("Kategoriler")
plt.ylabel("Paket Başına Ortalama Bayt (Log ölçekli)")
plt.yscale("log")
plt.title("Kategorilere Göre Paket Başına Gönderilen Ortalama Bayt")
plt.grid(axis="y", linestyle="--", alpha=0.7)
plt.tight_layout()
plt.show()
"""
"""
# kategorilere göre paket boyutları
df["PacketSize"] = (df["sbytes"] + df["dbytes"]) / 1048576

label_map = {
    'Normal': 'Normal Trafik',
    ' Fuzzers ': 'Fuzzer',
    'DoS': 'Hizmet Reddi',
    'Analysis': 'Analiz',
    'Backdoor': 'Arka Kapı',
    ' Shellcode ': 'Kabuk Kodu',
    ' Reconnaissance ': 'Keşif',
    'Exploits': 'Sömürme',
    'Worms': 'Solucanlar',
    'Generic': 'Genel Saldırılar'
}

size_distribution = df.groupby("attack_cat")["PacketSize"].agg(["min", "mean", "max"])
size_distribution.reset_index(inplace=True)
size_distribution["attack_cat"] = size_distribution["attack_cat"].map(label_map)

plt.figure(figsize=(14, 7))

x = range(len(size_distribution["attack_cat"]))
width = 0.25

plt.bar(x, size_distribution["min"], width, label="Minimum", color="skyblue")
plt.bar([i + width for i in x], size_distribution["mean"], width, label="Ortalama", color="salmon")
plt.bar([i + 2*width for i in x], size_distribution["max"], width, label="Maksimum", color="lightgreen")

plt.xticks([i + width for i in x], size_distribution["attack_cat"], rotation=45)
plt.xlabel("Kategoriler")
plt.ylabel("Paket Boyutu (Megabayt (Log ölçekli))")
plt.yscale("log")
plt.title("Veri Boyutları")
plt.legend()
plt.grid(axis="y", linestyle="--", alpha=0.7)
plt.tight_layout()
plt.show()
"""
"""
# saldırı verilerinin portlara göre dağılımı
attack_count = df.where(df["attack_cat"] != "Normal")

service_label_map = {
    'dns': 'DNS',
    '-': 'Muhtelif',
    'http': 'HTTP',
    'ftp-data': 'FTP-Data',
    'smtp': 'SMTP',
    'ftp': 'FTP',
    'ssh': 'SSH',
    'pop3': 'POP3',
    'dhcp': 'DHCP',
    'ssl': 'SSL',
    'snmp': 'SNMP',
    'radius': "Radius",
    'irc': 'IRC'
}

attack_label_map = {
    'Normal': 'Normal Trafik',
    ' Fuzzers ': 'Fuzzer',
    'DoS': 'Hizmet Reddi',
    'Analysis': 'Analiz',
    'Backdoor': 'Arka Kapı',
    ' Shellcode ': 'Kabuk Kodu',
    ' Reconnaissance ': 'Keşif',
    'Exploits': 'Sömürme',
    'Worms': 'Solucanlar',
    'Generic': 'Genel Saldırılar'
}

attack_count["service"] = attack_count["service"].map(service_label_map)
attack_count["attack_cat"] = attack_count["attack_cat"].map(attack_label_map)

service_attack_count = attack_count.groupby(["service", "attack_cat"]).size().unstack()

service_attack_count.plot(kind="bar", colormap="tab20")
plt.subplots_adjust(bottom=0.3)
plt.title("Saldırı Verilerinin Uygulama Katmanı Protokollerine Göre Dağılımı")
plt.xlabel("Protokoller")
plt.ylabel("Saldırı Sayısı (Log Ölçekli)")
plt.yscale("log")
plt.legend(title='Saldırı Kategorileri')
plt.tight_layout()
plt.show()
"""
"""
# port/uygulama katmanı protokolü dağılımı
service_count = df.value_counts("service")

label_map = {
    'dns': 'DNS',
    '-': 'Muhtelif',
    'http': 'HTTP',
    'ftp-data': 'FTP-Data',
    'smtp': 'SMTP',
    'ftp': 'FTP',
    'ssh': 'SSH',
    'pop3': 'POP3',
    'dhcp': 'DHCP',
    'ssl': 'SSL',
    'snmp': 'SNMP',
    'radius': "Radius",
    'irc': 'IRC'
}

service_count.index = [label_map.get(label, label) for label in service_count.index]

service_count.plot(kind="bar", color="steelblue")
plt.subplots_adjust(bottom=0.3)
plt.title("Verilerin Uygulama Katmanı Protokollerine Göre Dağılımı")
plt.xlabel("Protokoller")
#plt.ylabel("Sayısı")
#plt.xlim(0,40)
plt.show()
"""
"""
# saldırı verilerinin dağılımı
attack_count = df.value_counts("attack_cat")

label_map = {
    'Normal': 'Normal Trafik',
    ' Fuzzers ': 'Fuzzer',
    'DoS': 'Hizmet Reddi',
    'Analysis': 'Analiz',
    'Backdoor': 'Arka Kapı',
    ' Shellcode ': 'Kabuk Kodu',
    ' Reconnaissance ': 'Keşif',
    'Exploits': 'Sömürme',
    'Worms': 'Solucanlar',
    'Generic': 'Genel Saldırılar'
}

attack_count.index = [label_map.get(label, label) for label in attack_count.index]

colors = ["blue" if label == "Normal Trafik" else "orange" for label in attack_count.index]

attack_count.plot(kind="bar", color=colors)
plt.subplots_adjust(bottom=0.4)
plt.title("Saldırı Tiplerinin Veri Seti İçinde Dağılımı")
#plt.xlabel("Protokol Adı")
#plt.ylabel("Sayısı")
#plt.xlim(0,40)
plt.show()
"""
