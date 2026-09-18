import pandas as pd
import re


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


def normalize_columns(data):
    data = data.copy()
    data.columns = [
        re.sub(r"[^a-zA-Z0-9]+", "_", str(column)).strip("_").lower()
        for column in data.columns
    ]
    return data