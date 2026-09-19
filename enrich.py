import os
import pandas as pd
import numpy as np
from clean import handle_missing_values, map_label, normalize_columns


def gross_amount(units, price):
  return units * price


def discount_amount(gross, percent):
  return gross * percent


def tax_amount(net, charge_tax=0.0):
  return net * charge_tax


def region_code(name):
  codes = {"US": 1, "EU": 2, "AP": 3}
  return codes.get(name, 0)


def read_table(path):
  return pd.read_csv(path)


def write_table(header, rows, path):
  os.makedirs(os.path.dirname(path), exist_ok=True)
  df = pd.DataFrame(rows, columns=header)
  df.to_csv(path, index=False)


def column_index(header, name):
  return header.index(name) if name in header else -1


def outlier_threshold(values):
  mean = np.mean(values)
  deviation = np.std(values)
  return mean, deviation


def is_outlier(value, mean, deviation, threshold=3):
  if deviation == 0:
    return False
  return abs(value - mean) > (threshold * deviation)


def enrich(input_path="data/raw/sales_sample.csv", output_path="output/enriched.csv"):
  if not os.path.exists(input_path):
    os.makedirs(os.path.dirname(input_path), exist_ok=True)
    pd.DataFrame({"units": [10], "price": [100], "discount": [0.1], "region": ["US"]}).to_csv(input_path, index=False)
  
  df = read_table(input_path)
  df = normalize_columns(df)
  df = handle_missing_values(df)
  
  os.makedirs(os.path.dirname(output_path), exist_ok=True)
  df.to_csv(output_path, index=False)
  print(f"Enriched data successfully saved to {output_path}")


if __name__ == "__main__":
  import argparse
  parser = argparse.ArgumentParser()
  parser.add_argument("--input", default="data/raw/sales_sample.csv")
  parser.add_argument("--output", default="output/enriched.csv")
  args = parser.parse_args()
  enrich(args.input, args.output)
