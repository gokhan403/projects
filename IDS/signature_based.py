def detect_fuzzer(features):
    if features["Sload"].iloc[0] > 10000000 and features["Spkts"].iloc[0] > 50:
        return True

    return False

def detect_dos(features):
    if (features["Spkts"].iloc[0] + features["Dpkts"].iloc[0]) / (0.1 + features["dur"].iloc[0]) > 10000:
        return True

    return False

def detect_analysis(features):
    if (features["dsport"].iloc[0] in [80, 443] and features["proto"].iloc[0] in ["icmp", "tcp"] and
            (features["Spkts"].iloc[0] + features["Dpkts"].iloc[0]) / (0.1 + features["dur"].iloc[0]) > 250):
        return True

    return False

def detect_backdoor(features):
    if features["service"].iloc[0] == "-" and features["Sjit"].iloc[0] + features["Djit"].iloc[0] > 5000:
        return True

    return False

def detect_shellcode(features):
    if (features["service"].iloc[0] == "-" and
            (features["sbytes"].iloc[0] + features["dbytes"].iloc[0]) / (0.1 + features["dur"].iloc[0]) > 524288):
        return True

    return False

def detect_recon(features):
    if (features["service"].iloc[0] in ["dns", "http", "snmp", "smtp", "-"] and
            features["sport"].iloc[0] > 1023 > features["dsport"].iloc[0] and
            features["Sintpkt"].iloc[0] < 500 and features["Spkts"].iloc[0] / (0.1 + features["dur"].iloc[0]) > 50):
        return True

    return False

def detect_exploit(features):
    if (features["Sintpkt"].iloc[0] < 500 and
            (features["sbytes"].iloc[0] + features["dbytes"].iloc[0]) / (0.1 + features["dur"].iloc[0]) > 102400):
        return True

    return False

def detect_worm(features):
    if (features["service"].iloc[0] in ["http", "-"] and
            (features["Spkts"].iloc[0] + features["Dpkts"].iloc[0]) / (0.1 + features["dur"].iloc[0]) > 500):
        return True

    return False

def detect_generic(features):
    if (features["sttl"].iloc[0] > 255 and features["proto"].iloc[0] != "tcp" and
            features["smeansz"].iloc[0] + features["dmeansz"].iloc[0] < 100):
        return True

    return False


signature_database = {"Fuzzer": detect_fuzzer, "Hizmet Reddi": detect_dos, "Analiz": detect_analysis,
                      "Arka Kapı": detect_backdoor, "Kabuk Kodu": detect_shellcode, "Keşif": detect_recon,
                      "Sömürme": detect_exploit, "Solucan": detect_worm, "Genel": detect_generic}
