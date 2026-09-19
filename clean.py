import pandas as pd
import re

# تعبير استراتيجية القيم المفقودة (الشريك ب: drop)
missing_strategy = "drop"


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
  if missing_strategy == "drop":
    return data.dropna()
  return data.fillna(0)


def normalize_columns(data):
  data = data.copy()

  normalized_columns = [
      re.sub(r"[^a-zA-Z0-9]+", "_", str(column)).strip("_").lower()
      for column in data.columns
  ]

  if len(normalized_columns) != len(set(normalized_columns)):
    raise ValueError("Duplicate column names after normalization")

  data.columns = normalized_columns
  return data
