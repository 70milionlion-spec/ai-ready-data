import pandas as pd


def load_csv(file_path):
    return pd.read_csv(file_path)


def map_label(label):
    labels = {
        0: "low",
        1: "medium",
        2: "high",
        3: "critical",
    }
    return labels.get(label, "unknown")
def handle_missing_values(data):
    return data.fillna(0)