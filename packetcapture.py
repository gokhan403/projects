from scapy.all import sniff
from scapy.layers.inet import IP, TCP, UDP
from scapy.utils import PcapWriter
from collections import defaultdict, deque
from alert_system import IDSAlerts
from signature_based import *
import threading
import numpy as np
import pandas as pd
import joblib
import time
import psutil
import socket

class PacketCapture:
    def __init__(self, pcap_file="capture.pcap"):
        self.packet_queue = deque(maxlen=10000)
        self.stop_capture = threading.Event()
        self.capture_file = PcapWriter(pcap_file, append=False, sync=True)
        self.batch_lock = threading.Lock()

    def packet_callback(self, packet):
        if IP in packet:
            self.capture_file.write(packet)

            with self.batch_lock:
                self.packet_queue.append(packet)

    def start_capture(self):
        def capture_thread():
            sniff(prn=self.packet_callback, store=0, stop_filter=lambda _: self.stop_capture.is_set())

        self.capture_thread = threading.Thread(target=capture_thread)
        self.capture_thread.start()

    def stop(self):
        self.stop_capture.set()
        self.capture_thread.join()
        self.capture_file.close()

    def get_batch(self):
        with self.batch_lock:
            batch = list(self.packet_queue)
            self.packet_queue = deque(maxlen=10000)
            return batch

class TrafficAnalyzer:
    def __init__(self):
        self.flow_stats = defaultdict(lambda: {"packet_count": 0, "byte_count": 0, "ttl": 0, "tcpseq": 0, "window": 0,
                                               "packet_start:": 0, "packet_end": 0, "intpkt": 0, "jitter": 0})
        self.packet_time = defaultdict(lambda: {"start_time": None, "finish_time": None})
        self.stop_event = threading.Event()

    def start_analysis(self):
        self.analysis_thread = threading.Thread(target=self.analyze_packet, daemon=True)
        self.analysis_thread.start()

    def stop(self):
        self.stop_event.set()
        self.analysis_thread.join()

    def analyze_packet(self, packet):
        if TCP in packet:
            srcip = packet[IP].src
            dstip = packet[IP].dst
            sport = packet[TCP].sport
            dport = packet[TCP].dport

            flow_key = (srcip, dstip, sport, dport)
            reverse_key = (dstip, srcip, dport, sport)

            src_stats = self.flow_stats[flow_key]
            dst_stats = self.flow_stats[reverse_key]
            time_stats = self.packet_time[flow_key]
            current_time = packet.time

            if packet[IP].src == flow_key[0]:
                src_stats["packet_start"] = current_time
                src_stats["packet_count"] += 1
                src_stats["byte_count"] += len(packet)
                src_stats["ttl"] = packet[IP].ttl
                src_stats["tcpseq"] = packet[TCP].seq
                src_stats["window"] = packet[TCP].window

                jitter = src_stats["intpkt"]

                if src_stats["packet_start"] != 0 and src_stats["packet_end"] != 0:
                    src_stats["intpkt"] = src_stats["packet_start"] - src_stats["packet_end"]

                src_stats["jitter"] = np.abs(jitter - src_stats["intpkt"]) / src_stats["packet_count"]

                src_stats["packet_end"] = packet.time

            elif packet[IP].src == reverse_key[0]:
                dst_stats["packet_start"] = current_time
                dst_stats["packet_count"] += 1
                dst_stats["byte_count"] += len(packet)
                dst_stats["ttl"] = packet[IP].ttl
                dst_stats["tcpseq"] = packet[TCP].seq
                dst_stats["window"] = packet[TCP].window

                jitter = dst_stats["intpkt"]

                if dst_stats["packet_start"] != 0 and dst_stats["packet_end"] != 0:
                    dst_stats["intpkt"] = dst_stats["packet_start"] - dst_stats["packet_end"]

                dst_stats["jitter"] = np.abs(jitter - dst_stats["intpkt"]) / dst_stats["packet_count"]

                dst_stats["packet_end"] = packet.time

            if not time_stats["start_time"]:
                time_stats["start_time"] = current_time

            time_stats["finish_time"] = packet.time

            return self.extract_features(packet, src_stats, dst_stats, time_stats, flow_key)

        elif UDP in packet:
            srcip = packet[IP].src
            dstip = packet[IP].dst
            sport = packet[UDP].sport
            dport = packet[UDP].dport

            flow_key = (srcip, dstip, sport, dport)
            reverse_key = (dstip, srcip, dport, sport)

            src_stats = self.flow_stats[flow_key]
            dst_stats = self.flow_stats[reverse_key]
            time_stats = self.packet_time[flow_key]
            current_time = packet.time

            if packet[IP].src == flow_key[0]:
                src_stats["packet_start"] = current_time
                src_stats["packet_count"] += 1
                src_stats["byte_count"] += len(packet)
                src_stats["ttl"] = packet[IP].ttl
                src_stats["tcpseq"] = 0
                src_stats["window"] = 0

                jitter = src_stats["intpkt"]

                if src_stats["packet_start"] != 0 and src_stats["packet_end"] != 0:
                    src_stats["intpkt"] = src_stats["packet_start"] - src_stats["packet_end"]

                src_stats["jitter"] = np.abs(jitter - src_stats["intpkt"]) / src_stats["packet_count"]

                src_stats["packet_end"] = packet.time

            elif packet[IP].src == reverse_key[0]:
                dst_stats["packet_start"] = current_time
                dst_stats["packet_count"] += 1
                dst_stats["byte_count"] += len(packet)
                dst_stats["ttl"] = packet[IP].ttl
                dst_stats["tcpseq"] = 0
                dst_stats["window"] = 0

                jitter = dst_stats["intpkt"]

                if dst_stats["packet_start"] != 0 and dst_stats["packet_end"] != 0:
                    dst_stats["intpkt"] = dst_stats["packet_start"] - dst_stats["packet_end"]

                dst_stats["jitter"] = np.abs(jitter - dst_stats["intpkt"]) / dst_stats["packet_count"]

                dst_stats["packet_end"] = packet.time

            if not time_stats["start_time"]:
                time_stats["start_time"] = current_time

            time_stats["finish_time"] = packet.time

            return self.extract_features(packet, src_stats, dst_stats, time_stats, flow_key)

        return None

    def get_service(self, packet):
        if UDP in packet or TCP in packet:
            sport = packet.sport
            dport = packet.dport

            common_ports = {
                80: 'http',
                443: 'https',
                20: 'ftp-data',
                21: 'ftp',
                22: 'ssh',
                23: 'telnet',
                25: 'smtp',
                53: 'dns',
                67: 'dhcp',
                110: 'pop3',
                143: 'imap',
                123: 'ntp',
                161: 'snmp',
                1812: 'radius',
                6667: 'irc'
            }

            return common_ports.get(dport) or common_ports.get(sport) or "-"

        return "-"

    def extract_features(self, packet, src_stats, dst_stats, time_stats, flow_key):
        transaction_protocols = {
            1: "icmp",
            2: "igmp",
            6: "tcp",
            17: "udp",
            41: "ipv6",
            89: "ospf",
        }

        duration = time_stats["finish_time"] - time_stats["start_time"]

        return {
            "srcip": flow_key[0],
            "sport": flow_key[2],
            "dstip": flow_key[1],
            "dsport": flow_key[3],
            "proto": transaction_protocols.get(packet[IP].proto, f"Unknown: {packet[IP].proto}"),
            "dur": duration,
            "sbytes": src_stats["byte_count"],
            "dbytes": dst_stats["byte_count"],
            "sttl": src_stats["ttl"],
            "dttl": dst_stats["ttl"],
            "service": self.get_service(packet),
            "Sload": src_stats["byte_count"] * 8 / duration if duration > 0.0 else 0.0,
            "Dload": dst_stats["byte_count"] * 8 / duration if duration > 0.0 else 0.0,
            "Spkts": src_stats["packet_count"],
            "Dpkts": dst_stats["packet_count"],
            "swin": src_stats["window"],
            "dwin": dst_stats["window"],
            "stcpb": src_stats["tcpseq"],
            "dtcpb": dst_stats["tcpseq"],
            "smeansz": round(src_stats["byte_count"] / src_stats["packet_count"] if src_stats["packet_count"] > 0 else 0),
            "dmeansz": round(dst_stats["byte_count"] / dst_stats["packet_count"] if dst_stats["packet_count"] > 0 else 0),
            "Sjit": float(src_stats["jitter"]) * 1000,
            "Djit": float(dst_stats["jitter"]) * 1000,
            "Stime": round(time_stats["start_time"]),
            "Ltime": round(time_stats["finish_time"]),
            "Sintpkt": src_stats["intpkt"] * 1000,
            "Dintpkt": dst_stats["intpkt"] * 1000,
            "is_sm_ips_ports": 1 if flow_key[0] == flow_key[1] and flow_key[2] == flow_key[3] else 0,
        }


def get_process_info(features):
    try:
        local_ip = features["dstip"] if features["dstip"] in ["127.0.0.1", socket.gethostbyname(socket.gethostname())] \
            else features["srcip"]
        local_port = features["dsport"] if local_ip == features["dstip"] else features["sport"]

        for conn in psutil.net_connections(kind="all"):
            if conn.laddr.ip in [local_ip, "0.0.0.0"] and conn.laddr.port == local_port:
                proc = psutil.Process(conn.pid)
                return {"pid": conn.pid,
                        "name": proc.name(),
                        "exe": proc.exe(),
                        "memory_mb": proc.memory_info().rss / 1024 / 1024,
                        "cpu_percent": proc.cpu_percent(),
                        "status": proc.status()}

    except (psutil.NoSuchProcess, psutil.AccessDenied):
        pass

    return None


if __name__ == "__main__":
    alerts = IDSAlerts()
    alerts.root.after(100, alerts.start_monitor)

    pcap_path = "capture.pcap"
    columns_to_encode = ["srcip", "dstip", "proto", "service"]
    batch_duration = 10
    anomaly_pred = {"['Normal']": 'Normal', "[' Fuzzers ']": 'Fuzzer', "['DoS']": 'Hizmet Reddi',
                    "['Analysis']": 'Analiz', "['Backdoor']": 'Arka Kapı', "[' Shellcode ']": 'Kabuk Kodu',
                    "[' Reconnaissance ']": 'Keşif', "['Exploits']": 'Sömürme', "['Worms']": 'Solucanlar',
                    "['Generic']": 'Genel Saldırılar'}

    model = joblib.load("random_forest.pkl")
    encoder = joblib.load("encoder.pkl")

    capture = PacketCapture(pcap_file=pcap_path)
    analyzer = TrafficAnalyzer()

    capture.start_capture()
    analyzer.start_analysis()

    while True:
        time.sleep(batch_duration)
        packets = capture.get_batch()
        try:
            intrusions = []
            batch_info = {"pid": [], "name": [], "exe": [], "memory_mb": [],
                          "cpu_percent": [], "status": []}
            flow_features = []
            for pkt in packets:
                process_info = {}
                features = analyzer.analyze_packet(pkt)
                print(features)

                if features is None:
                    continue

                sample_df = pd.DataFrame([features])

                for attack_type, detect_function in signature_database.items():
                    if detect_function(sample_df):
                        print(f"{attack_type} saldırısı tespit edildi!")
                        process_info = get_process_info(features)
                        intrusions.append(f"{attack_type} (İmza Tabanlı)")
                        break

                encoded_sample = pd.DataFrame(encoder.transform(sample_df[columns_to_encode]),
                                              columns=encoder.get_feature_names_out(columns_to_encode),
                                              index=sample_df.index)
                final_sample = pd.concat([sample_df.drop(columns=columns_to_encode), encoded_sample], axis=1)

                pred = model.predict(final_sample)
                print(anomaly_pred[str(pred)])
                if anomaly_pred[str(pred)] != "Normal":
                    intrusions.append(f"{anomaly_pred[str(pred)]} (Anomali Tabanlı)")
                    process_info = get_process_info(features)

                if process_info:
                    print(f"Şüpheli paket işlemi -> Pid: {process_info['pid']}, Adı: {process_info['name']}, "
                          f"Exe: {process_info['exe']}, Hafıza kullanımı: {process_info['memory_mb']} mb, "
                          f"CPU kullanımı: {process_info['cpu_percent']}%, Durum: {process_info['status']}")
                    if process_info["pid"] not in batch_info["pid"]:
                        flow_features.append(features)
                        for key in batch_info:
                            batch_info[key].append(process_info[key])

            if intrusions:
                alerts.add_alert(intrusions, batch_info, flow_features)
        except KeyboardInterrupt:
            print("\nStopping...")
            capture.stop()
            analyzer.stop()
            break
