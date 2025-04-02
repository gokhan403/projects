import pandas as pd
from matplotlib import pyplot as plt


df = pd.read_csv("data/CSV/combined_data.csv")
pd.set_option("display.max.rows", 150)

df["PacketSize"] = (df["totalSourceBytes"] + df["totalDestinationBytes"]) / 1048576

normal_data = df[df["Label"] == "Normal"]
attack_data = df[df["Label"] == "Attack"]

plt.figure(figsize=(10, 6))
plt.plot(normal_data["PacketSize"], alpha=1.0, label="Normal", color="blue")
plt.plot(attack_data["PacketSize"], alpha=1.0, label="Saldırı", color="orange")
plt.title("Normal ve Saldırı Verilerinin Boyutlarının Dağılımı")
plt.xlabel("Veri Örneği")
plt.ylabel("Veri Boyutu (megabayt)")
plt.legend()
plt.grid()
plt.ticklabel_format(style="plain", axis="both", useOffset=False)
plt.show()

"""
plt.bar([0, 1], normal_sizes, width=0.3, label="Normal", color="blue")
plt.bar([0.3, 1.3], attack_sizes, width=0.3, label="Attack", color="orange")

plt.xticks([0.15, 1.15], categories)
plt.ylabel("Veri Boyutu")
plt.title("Normal ve Saldırı Verilerinin En Küçük ve En Büyük Boyutları")
plt.legend(["Normal", "Saldırı"])
plt.yscale("log")
plt.show()
"""
"""
attack = df[df["Label"] == "Attack"]

attack.value_counts("appName").plot(kind="bar", color="orange")
plt.subplots_adjust(bottom=0.4)
plt.title("Saldırı Verilerinin Protokollere Göre Dağılımı")
plt.xlabel("Protokol Adı")
#plt.ylabel("Sayısı")
plt.xlim(0,40)
plt.show()
"""
"""
labels = ["Normal", "Saldırı"]
colors = ["blue", "orange"]

df.value_counts("Label").plot(kind="pie", labels=labels, colors=colors, autopct="%1.1f%%", startangle=90)
plt.title("Normal ve Saldırı Verilerinin Oranı", pad=20)
plt.axis("equal")
plt.ylabel("")
plt.show()
"""

"""
normal_samples = df[df["Label"] == "Normal"]
attack_samples = df[df["Label"] == "Attack"]

normal_total_size = normal_samples["totalDestinationBytes"].sum() + normal_samples["totalSourceBytes"].sum() / 2002747
attack_total_size = attack_samples["totalDestinationBytes"].sum() + attack_samples["totalSourceBytes"].sum() / 68910

sizes = [normal_total_size, attack_total_size]
labels = ["Normal", "Saldırı"]
colors = ["blue", "orange"]

plt.pie(sizes, labels=labels, colors=colors, autopct="%1.1f%%", startangle=90)
plt.title("Normal ve Saldırı Verilerinin Ortalama Boyut Farkı")
plt.axis("equal")
plt.show()
"""

"""
colors = ["orange", "blue"]
result = df.groupby(["appName", "Label"]).size().reset_index(name="Packet_Count")
pivot_result = result.pivot(index="appName", columns="Label", values="Packet_Count").fillna(0)
pivot_result["Total"] = pivot_result.sum(axis=1)
pivot_result = pivot_result.sort_values(by="Total", ascending=False)
pivot_result = pivot_result.drop(columns="Total")

pivot_result.plot(kind="bar", title="Normal ve Saldırı Verilerinin Protokollere Göre Dağılımı", color=colors)
plt.legend(["Saldırı", "Normal"])
plt.subplots_adjust(bottom=0.4)
plt.xlabel("Protokol Adı")
plt.xlim(0, 40)
plt.show()
"""

"""
df.value_counts("appName").plot(kind="bar")
plt.subplots_adjust(bottom=0.4)
plt.title("Verilerin Protokollere Göre Dağılımı")
plt.xlabel("Protokol Adı")
#plt.ylabel("Sayısı")
plt.xlim(0,40)
plt.show()
"""
